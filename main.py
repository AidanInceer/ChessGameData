import flask

from src.extract import ExtractGameData
from src.load import GCSLoader
from src.transform import TransformUserData
from src.utils.logger import create_logger
from src.utils.request_parser import Parser

BUCKET: str = "chess-json-data"
CONTENT_TYPE: str = "application/json"


def extract_game_data(request: flask.Request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        ...
    """

    # setup environment:
    logger = create_logger()
    config = Parser(request, logger).parse_request()

    # Extract games data
    extractor = ExtractGameData(logger, config)
    data = extractor.extract_user_games()

    # Clean and Transform the extracted games.
    # - pgn is a file format used in chess to store move and game information.
    for game_num, game_pgn in enumerate(data):
        tud = TransformUserData(logger, config)
        data, file_name = tud.create_gcs_dict_object(game_num, game_pgn)

        # Upload json file to gcs bucket.
        GCSLoader.upload_blob(data, file_name, BUCKET, CONTENT_TYPE)

    return f"All files successfully uploaded to bucket ({BUCKET})"
