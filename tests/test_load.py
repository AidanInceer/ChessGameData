from io import StringIO
from logging import Logger
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

import chess
import chess.pgn
from chess.pgn import Game

from src.load import GCSLoader
from src.utils.config import Config


class TestGCSLoader(TestCase):
    ...
