import json
import logging
import threading
import time
from sentence_transformers import SentenceTransformer, util
import torch
import pickle

from semantic_steam_search.shared import *

logger = logging.getLogger(LOGGER_NAME)

corpus = None
corpus_embeddings = None
embedder = None

initialized = False
initialized_lock = threading.Lock()

def is_initialized() -> bool:
    global initialized
    initialized_lock.acquire()
    result = bool(initialized)
    initialized_lock.release()
    return result

def set_initialized(value: bool):
    global initialized
    initialized_lock.acquire()
    initialized = bool(value)
    initialized_lock.release()

def initialize_search():
    global corpus, corpus_embeddings, embedder, initialized
    logger.info('Loading corpus')
    
    with open(GAMES_FILE, 'r') as f:
        corpus_data = json.load(f)
    corpus = list(corpus_data.values())

    logger.info('Loading embeddings')
    with open(EMBEDDINGS_FILE, 'rb') as f:
        corpus_embeddings = pickle.load(f)

    logger.info('Loading embedder')
    embedder = SentenceTransformer(TRANSFORMER)

    set_initialized(True)


def search(phrase: str, offset: int, count: int) -> dict:
    start = time.time()
    logger.info(f'Getting search results for phrase \'{phrase}\'.')

    logger.info('Calculating query embedding')
    query_embedding = embedder.encode(phrase, convert_to_tensor=True)

    logger.info('Calculating cosine similarity.')
    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]

    logger.info(f'Finding top {count} results with offset {offset}.')
    scores, indices = torch.topk(cos_scores, k=(count + offset))
    scores, indices = scores[offset:], indices[offset:]

    duration_ms = (time.time()-start) * 1000
    logger.info(f'Finished search request in {duration_ms:.1f}ms.')

    return {
        'hits': [corpus[i] for i in indices],
        'current': len(indices),
        'total': len(corpus)
    }
