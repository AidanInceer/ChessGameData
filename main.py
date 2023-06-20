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
    games = int(request.args.get("games"))
    
    
    urls = chessdotcom.get_player_game_archives(username).json
    url = urls["archives"][-1]
    response = requests.get(url)
    data = response.json()
    
    for num, game_pgn in enumerate(data["games"][-games::]):
        pgn = StringIO(game_pgn["pgn"])
        game = chess.pgn.read_game(pgn)
        headers = dict(game.headers)
        time_control = headers['TimeControl']
        game_data = {
            "username":username,
            "game_num":num,
            "pgn":pgn,
            "headers":headers
        }
        blob_name = upload_blob(data=game_data, blob_name=f"{username}-{time_control}-{num}.json")
    return f"File uploaded to {blob_name}."

def upload_blob(data, blob_name: str) -> str:

    storage_client = storage.Client()
    bucket = storage_client.get_bucket("chess-json-data")
    blob = bucket.blob(blob_name)

    blob.upload_from_string(data=json.dumps(data),content_type='application/json')

    
    return blob_name




# Run to test Locally
# if __name__ == '__main__':
#     chessgamedata("Ainceer")
