# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import random
import string
import redshift_connector
from redshift_connector import InterfaceError

from amazon_sagemaker_sql_execution.exceptions import (
    SQLExecutionError,
    ConnectionExpireFault,
    ConnectionCreationError,
    CredentialsExpiredError,
)
from amazon_sagemaker_sql_execution.redshift.models import (
    RedshiftSQLConnectionProperties,
    RedshiftSQLExecutionResponse,
    RedshiftSQLQueryParameters,
)

from amazon_sagemaker_sql_execution.models.sql_execution import (
    SQLExecutionRequest,
)

from amazon_sagemaker_sql_execution.connection import SQLConnection
from amazon_sagemaker_sql_execution.utils.metrics.service_metrics import add_metrics
from amazon_sagemaker_sql_execution.utils.constants import MetricsConstants

IDLE_CONNECTION_ERROR_MESSAGE = "This issue could be due to a stale or inactive connection. Try reloading the SQL extension to establish a fresh connection via the command: %reload_ext amazon_sagemaker_sql_magic"


class RedshiftSQLConnection(SQLConnection):
    def log_source(self):
        return self.__class__.__name__

    @staticmethod
    def engine_type():
        return "REDSHIFT"

    def __init__(self, connection_props: RedshiftSQLConnectionProperties):
        super().__init__(connection_props)
        try:
            connection_dict = self._connection_props.to_dict()

            # short-term workaround for HULK before db_user change is deployed
            # TODO - remove this after db_user is deployed.
            if connection_dict.get("iam") and not connection_dict.get("db_user"):
                connection_dict["db_user"] = "dbuser_" + "".join(
                    random.choices(string.ascii_uppercase, k=8)
                )

            # Redshift does not take in autocommit as a constructor parameter. So, remove it from the connection dict
            # props. By default, set auto-commit to true to mimick Redshift QueryEditorV2 experience
            # https://github.com/aws/amazon-redshift-python-driver/blame/e457b2e55241094a661d437377fb02689d2ceb5c/redshift_connector/core.py#L59
            # TODO: Remove when Redshift accepts autocommit as a connection parameter
            autocommit = connection_dict.pop("autocommit", "True").lower() == "true"

            self.connection = redshift_connector.connect(**connection_dict)
            self.connection.autocommit = autocommit

        except Exception as e:
            self.error(
                f"Could not create connection using params: {connection_props} due to: {str(e)}"
            )
            raise ConnectionCreationError(e) from e

    @add_metrics(MetricsConstants.SQL_QUERY_EXECUTE_OPERATION)
    def execute(self, execution_request: SQLExecutionRequest) -> RedshiftSQLExecutionResponse:
        self.metrics_context.set_dimensions(
            [
                {
                    MetricsConstants.OPERATION_DIMENSION_NAME: MetricsConstants.SQL_QUERY_EXECUTE_OPERATION,
                    MetricsConstants.CONNECTION_TYPE_DIMENSION_NAME: self.engine_type(),
                }
            ]
        )

        cursor = None
        res_cursor = None

        try:
            cursor = self.connection.cursor()

            # Convert to RedshiftSQLQueryParameters and back to handle database specific inconsistencies
            execution_params = RedshiftSQLQueryParameters(execution_request.queryParams).to_dict()

            # Redshift expects sql in `operation` param:
            # https://github.com/aws/amazon-redshift-python-driver/blob/2898d86de9bb6be1e3def88e15c78c9ea767ec52/redshift_connector/cursor.py#L191
            execution_params["operation"] = execution_request.query
            res_cursor = cursor.execute(**execution_params)

            # In the case of SQL statements other than SELECT/SHOW, call to `cursor.fetchall()` will error out and
            # `cursor.truncated_row_desc()` will return an empty list
            # https://github.com/aws/amazon-redshift-python-driver/issues/201
            if len(res_cursor.truncated_row_desc()) == 0:
                data = ()
                cursor_desc = []
            else:
                data = res_cursor.fetchall()
                cursor_desc = res_cursor.description

            res_cursor.close()
            cursor.close()

            return RedshiftSQLExecutionResponse(data=data, cursor_desc=cursor_desc)

        except Exception as e:
            self.error(f"Error while executing query {e}")
            if (
                isinstance(e, InterfaceError)
                and e.args[0].get("M") == "IAM Authentication token has expired"
            ):
                raise CredentialsExpiredError(e)

            # In case of error, Redshift requires manual rollback.
            self.connection.rollback() if self.connection else None
            res_cursor.close() if res_cursor else None
            cursor.close() if cursor else None

            # Errors below are caused by leaving notebook idle for a long time and reloading
            # extension is needed in this case.
            # TODO: Work with Redshift engineers to root cause if the issue happens again.
            # Related TT: https://t.corp.amazon.com/V1405374185
            if str(e).startswith("EOF occurred in violation of protocol"):
                # This error is generated from ssl.py
                raise ConnectionExpireFault(IDLE_CONNECTION_ERROR_MESSAGE)

            if isinstance(e, IndexError) and str(e).startswith("tuple index out of range"):
                # This error is most likely generated from redshift_connector/cursor.py
                raise ConnectionExpireFault("{}. {}".format(e, IDLE_CONNECTION_ERROR_MESSAGE))

            if "NFTSetupSessionStateOnRestore" in str(e):
                # This is another possible error from expired connection
                raise ConnectionExpireFault("{}. {}".format(e, IDLE_CONNECTION_ERROR_MESSAGE))

            raise SQLExecutionError(e) from e

    @add_metrics(MetricsConstants.SQL_CLOSE_CONNECTION_OPERATION)
    def close(self):
        self.metrics_context.set_dimensions(
            [
                {
                    MetricsConstants.OPERATION_DIMENSION_NAME: MetricsConstants.SQL_CLOSE_CONNECTION_OPERATION,
                    MetricsConstants.CONNECTION_TYPE_DIMENSION_NAME: self.engine_type(),
                }
            ]
        )
        if self.connection is not None:
            self.connection.close()
