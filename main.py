from io import StringIO

import chess
import chess.pgn
import chessdotcom
import pandas as pd
import requests


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
    print(username)

    urls = chessdotcom.get_player_game_archives(username).json
    url = urls["archives"][-1]
    print(url)

    response = requests.get(url)
    data = response.json()
    games_list = []
    for game_num, game_pgn in enumerate(data["games"][-10:-1]):
        game_pgn = StringIO(game_pgn["pgn"])

        game = chess.pgn.read_game(game_pgn)
        headers = dict(game.headers)
        headers["GameNumber"] = game_num
        games_list.append(headers)

    df = pd.DataFrame(games_list)
    print(df)

    return "SUCCESS"


# if __name__ == '__main__':
#     get_games("Ainceer")
