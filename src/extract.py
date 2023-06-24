import json
from dataclasses import dataclass

import chessdotcom
import requests

from src.utils.config import Config
from src.utils.logger import Logger


@dataclass
class ExtractGameData:
    logger: Logger
    config: Config

    def extract_user_games(self) -> list:
        urls = chessdotcom.get_player_game_archives(self.config.username).json

        # Add additional functionality which varies the numer of urls collected based on
        # the number of games played in that month/url and the amount of games the user
        #  has requested.
        url = urls["archives"][-1]
        response = requests.get(url)
        return response.json()["games"][-self.config.games : :]
