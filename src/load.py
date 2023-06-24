import json
from dataclasses import dataclass

from google.cloud.storage import Client


@dataclass
class GCSLoader:
    @staticmethod
    def upload_blob(data, file_name: str, bucket: str, content_type: str) -> None:
        storage_client = Client()
        gcs_bucket = storage_client.get_bucket(bucket)
        blob = gcs_bucket.blob(file_name)
        blob.upload_from_string(data=json.dumps(data), content_type=content_type)
