# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
import logging
import os

import boto3
import botocore
import traceback
from functools import lru_cache

from amazon_sagemaker_sql_execution.utils.constants import (
    UNKNOWN_METRIC_VALUE,
    LOGGER_NAME,
    USE_DUALSTACK_ENDPOINT,
)
from amazon_sagemaker_sql_execution.utils.exception_utils import handle_endpoint_connection_error


@lru_cache(maxsize=1)
def get_aws_account_id(region_name):
    try:
        account_id = os.environ.get("AWS_ACCOUNT_ID")
        if account_id is None:
            # we are in standalone jupyterlab
            session = boto3.session.Session()
            cfg = botocore.client.Config(
                use_dualstack_endpoint=USE_DUALSTACK_ENDPOINT,
            )
            client = session.client(service_name="sts", region_name=region_name, config=cfg)
            return client.get_caller_identity()["Account"]
        return account_id
    except botocore.exceptions.EndpointConnectionError as error:
        handle_endpoint_connection_error(error)
    except Exception as e:
        logging.getLogger(LOGGER_NAME).error(f"Failed to get aws account id: {e}")
        return UNKNOWN_METRIC_VALUE
