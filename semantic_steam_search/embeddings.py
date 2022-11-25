from sentence_transformers import SentenceTransformer
import json
import pickle
import logging

from semantic_steam_search.shared import *

logger = logging.getLogger(LOGGER_NAME)

BATCH_SIZE = 16

def initialize_embeddings():
    if os.path.isfile(EMBEDDINGS_FILE):
        logger.info('Found existing embeddings file. Skipping.')
        return

    embedder = SentenceTransformer(TRANSFORMER)

    logger.info('Calculating embeddings with transformer: \'%s\'.', TRANSFORMER)

    logger.info('Loading games from \'%s\'.', GAMES_FILENAME)
    with open(GAMES_FILE, 'r') as f:
        games = json.load(f)

    def get_corpus_text(game: dict) -> str:
        fields = [game['name'], game['short_description'], game['genre']]
        return ' '.join(fields)

    logger.info('Transforming data to text corpus.')
    corpus = [get_corpus_text(game) for game in games.values()]

    logger.info('Calculating embeddings. This might take some time.')
    corpus_embeddings = embedder.encode(corpus, show_progress_bar=True, convert_to_tensor=True, batch_size=BATCH_SIZE)
    
    logger.info('Saving embeddings to \'%s\'.', EMBEDDINGS_FILENAME)
    with open(EMBEDDINGS_FILE, 'wb') as f:
        pickle.dump(corpus_embeddings, f)

    logger.info('Embeddings saved successfully!')
