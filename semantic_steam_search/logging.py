import logging

from semantic_steam_search.shared import LOGGER_NAME

def initialize_logging():
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.formatter = logging.Formatter('%(asctime)s [%(levelname)s] (%(module)s:%(lineno)d) %(message)s')
    stream_handler.setLevel(logging.INFO)

    logger.handlers = [ stream_handler ]