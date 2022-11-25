from semantic_steam_search.data import initialize_data
from semantic_steam_search.embeddings import initialize_embeddings
from semantic_steam_search.logging import initialize_logging
from semantic_steam_search.search import initialize_search, search

import threading

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
    initialize_data()
    initialize_embeddings()
    initialize_search()
