
import json
from google.cloud import storage

def upload_blob(data, blob_name):
    """_summary_

    Args:
        data (_type_): _description_
        blob_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket("chess-json-data")
    blob = bucket.blob(blob_name)

    blob.upload_from_string(data=json.dumps(data),content_type='application/json')

    
    return blob_name