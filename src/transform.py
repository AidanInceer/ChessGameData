import hashlib
from dataclasses import dataclass
from io import StringIO

import chess
import chess.pgn

from src.utils.config import Config
from src.utils.logger import Logger


@dataclass
class TransformUserData:
    logger: Logger
    config: Config

    def create_gcs_dict_object(self, game_num, game_pgn):
        pgn = StringIO(game_pgn["pgn"])
        game = chess.pgn.read_game(pgn)

        headers = dict(game.headers)

        game_id = self.generate_unique_id(
            self.config.username, headers["UTCDate"], headers["UTCTime"]
        )
        metadata = {
            "game_id": game_id,
            "username": self.config.username,
            "depth": self.config.depth,
            "pgn": game_pgn["pgn"],
            "game_num": game_num,
        }

        game_data = metadata | headers

        file_name = f"{game_id}.json"
        return (game_data, file_name)

    @staticmethod
    def generate_unique_id(username: str, game_date: str, game_time: str):
        base_id = username + game_date + game_time
        return hashlib.sha1(base_id.encode())
