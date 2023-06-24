from dataclasses import dataclass

import flask

from src.utils.config import Config
from src.utils.exceptions import InvalidRequestArgument
from src.utils.logger import Logger


@dataclass
class Parser:
    request: flask.Request
    logger: Logger

    def parse_request(self):
        """Parses the request to the cloud function

        Returns:
            (tuple): cleaned username, games to fetch and engine depth.
        """
        try:
            username = self.request.args.get("username")
            games = int(self.request.args.get("games"))
            depth = int(self.request.args.get("depth"))

        except InvalidRequestArgument:
            self.logger.error(
                "Invalid arguments passed to the request"
                ", please re-trigger the cloud function"
                "with valid arguments."
            )

        return Config(username, games, depth)
