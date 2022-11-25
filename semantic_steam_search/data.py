import os 
import zipfile
import logging

from semantic_steam_search.shared import *

logger = logging.getLogger('semantic_steam_search')

def initialize_data(kaggle_user: str | None = None, kaggle_key: str | None = None):
    if os.path.isfile(GAMES_FILE):
        logger.info('Found existing data file. Skipping.')
        return

    if kaggle_user: os.environ['KAGGLE_USERNAME'] = kaggle_user
    if kaggle_key: os.environ['KAGGLE_KEY'] = kaggle_key

    logger.info('Getting dataset from kaggle with user %s.', kaggle_user)

    from kaggle.api.kaggle_api_extended import KaggleApi

    api = KaggleApi()
    api.authenticate()

    api.dataset_download_file(GAMES_DATASET, GAMES_FILENAME, DATA_ROOT)
    zip_file = GAMES_FILE + '.zip'

    logger.info('Got dataset. Extracting.')

    with zipfile.ZipFile(zip_file, 'r') as f:
        f.extract(GAMES_FILENAME, DATA_ROOT)
    os.remove(zip_file)

    logger.info('Extracted dataset successfully.')
