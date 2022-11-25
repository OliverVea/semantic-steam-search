from semantic_steam_search.shared import *

from semantic_steam_search.data import initialize_data
from semantic_steam_search.embeddings import initialize_embeddings
from semantic_steam_search.logging import initialize_logging
from semantic_steam_search.search import initialize_search

import logging
import threading

logger = logging.getLogger(LOGGER_NAME)

thread = None

initialize_logging()

def start_initialization():
    global thread
    if thread: return
    thread = threading.Thread(target=initialization_target)
    thread.start()

def initialization_target():
    global thread
    initialize()
    thread = None

def initialize():
    logger.info('Starting initialization.')
    try:
        initialize_data()
        initialize_embeddings()
        initialize_search()
        logger.info('Finished initialization successfully!')
    except Exception as e:
        logger.error('Got error while initializing:\n%s', str(e))
