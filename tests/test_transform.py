from io import StringIO
from logging import Logger
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

import chess
import chess.pgn
from chess.pgn import Game

from src.transform import TransformUserData
from src.utils.config import Config


class TestTransformUserData(TestCase):
    def setUp(self) -> None:
        self.log = Logger("my_logger")
        self.config = Config("Ainceer", 1, 1)

        self.tud = TransformUserData(self.log, self.config)
        self.headers = {"UTCDate": "01-01-2020", "UTCTime": "12:00"}

    def test_generate_unique_id(self):
        expected = "1a125afa3405ba2ca623b491cfde45c3cbd0db03"
        actual = self.tud.generate_unique_id(
            self.config.username, self.headers["UTCDate"], self.headers["UTCTime"]
        )
        assert actual == expected

    @patch(
        "chess.pgn.read_game",
        return_value={"pgn": "e4e5"},
    )
    def test_read_chess_game_from_string(self, mock_read_game):
        expected = {"pgn": "e4e5"}
        test_input = {"pgn": "e4e5"}

        actual = self.tud.read_chess_game_from_string(test_input)

        assert actual == expected
