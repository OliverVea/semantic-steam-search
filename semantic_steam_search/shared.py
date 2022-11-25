import configparser
import os
import semantic_steam_search

MODULE_ROOT = os.path.dirname(os.path.abspath(semantic_steam_search.__file__))
DATA_ROOT = os.environ.get('DATA_ROOT', os.path.join(MODULE_ROOT, 'data'))

CONFIG_FILE = os.path.join(MODULE_ROOT, '../config.ini')

GAMES_DATASET = 'tristan581/all-55000-games-on-steam-november-2022'
GAMES_FILENAME = 'steam_games.json'
GAMES_FILE = os.path.join(DATA_ROOT, GAMES_FILENAME)

EMBEDDINGS_FILENAME = 'embeddings.pickle'
EMBEDDINGS_FILE = os.path.join(DATA_ROOT, EMBEDDINGS_FILENAME)

LOGGER_NAME = 'semantic_steam_search'

config_parser = configparser.ConfigParser()
config_parser.read(CONFIG_FILE)
TRANSFORMER = config_parser.get('data', 'transformer')

def clamp(minimum, value, maximum):
    return min(max(value, minimum), maximum)