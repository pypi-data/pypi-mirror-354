import json
from amazon_sagemaker_sql_execution.utils.constants import UNKNOWN_METRIC_VALUE

SAGEMAKER_INTERNAL_METADATA_FILE = "/opt/.sagemakerinternal/internal-metadata.json"


class InternalMetadata:
    def __init__(
        self,
    ):
        internal_metadata = _get_internal_metadata_file()
        self.stage = internal_metadata.get("Stage", UNKNOWN_METRIC_VALUE)
        self.llds_endpoint = internal_metadata.get("LldsEndpoint", UNKNOWN_METRIC_VALUE)
        self.app_network_access_type = internal_metadata.get(
            "AppNetworkAccessType", UNKNOWN_METRIC_VALUE
        )


def _get_internal_metadata_file():
    try:
        with open(SAGEMAKER_INTERNAL_METADATA_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}
