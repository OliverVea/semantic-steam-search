import logging
import os

from semantic_steam_search.shared import LOGGER_NAME

def initialize_logging():
    logger = logging.getLogger(LOGGER_NAME)
    loglevel = os.environ.get('LOG_LEVEL', logging.WARNING)
    logger.setLevel(loglevel)

    stream_handler = logging.StreamHandler()
    stream_handler.formatter = logging.Formatter('%(asctime)s [%(levelname)s] (%(module)s:%(lineno)d) %(message)s')
    stream_handler.setLevel(logging.INFO)

    logger.handlers = [ stream_handler ]