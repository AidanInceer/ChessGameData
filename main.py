from io import StringIO

import chess
import chess.pgn
import chessdotcom
import pandas as pd
import requests
import json
from google.cloud import storage


def chessgamedata(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    username = request.args.get("username")
    urls = chessdotcom.get_player_game_archives(username).json
    url = urls["archives"][-1]

    response = requests.get(url)
    data = response.json()
    for game_pgn in data["games"][-1]:
        pgn = StringIO(game_pgn["pgn"])
        game = chess.pgn.read_game(pgn)
        headers = dict(game.headers)

    blob_name = upload_blob(data=headers, blob_name="")
    return f"File uploaded to {blob_name}."


def upload_blob(data, blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket("chess-json-data")
    blob = bucket.blob(blob_name)

    blob.upload_from_string(data=json.dumps(data),content_type='application/json')

    
    return blob_name



# if __name__ == '__main__':
#     chessgamedata("Ainceer")
