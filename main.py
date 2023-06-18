from io import StringIO

import json
import chess
import chess.pgn
import chessdotcom
import requests

from google.cloud import storage

def extract_game_data(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        ...
    """

    username = request.args.get("username")
    urls = chessdotcom.get_player_game_archives(username).json
    url = urls["archives"][-1]

    response = requests.get(url)
    data = response.json()
    for num, game_pgn in enumerate(data["games"][-20:-1]):
        pgn = StringIO(game_pgn["pgn"])
        game = chess.pgn.read_game(pgn)
        headers = dict(game.headers)
        time_control = headers['TimeControl']
        blob_name = upload_blob(data=headers, blob_name=f"{username}-{time_control}-{num}.json")
    return f"File uploaded to {blob_name}."

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




# Run to test Locally
# if __name__ == '__main__':
#     chessgamedata("Ainceer")
