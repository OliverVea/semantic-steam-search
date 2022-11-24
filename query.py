import json
from sentence_transformers import SentenceTransformer, util
import torch
import pickle

embedder = SentenceTransformer('all-MiniLM-L6-v2')

query = 'co-op multiplayer dungeon crawler'
k = 10

print('Loading corpus')
with open('steam_games.json', 'r') as f:
    corpus_data = json.load(f)
corpus = list(corpus_data.values())

print('Loading embeddings')
with open('embeddings.pickle', 'rb') as f:
    corpus_embeddings = pickle.load(f)

print('Calculating query embedding')
query_embedding = embedder.encode(query, convert_to_tensor=True)

print('Calculating cosine similarity.')
cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]

print(f'Finding top {k} results')
top_results = torch.topk(cos_scores, k=k)

print(f"""
======================

Query: {query}

Top {k} search results:""")

for score, idx in zip(top_results[0], top_results[1]):
    print(f'- {corpus[idx]["name"]}: {corpus[idx]["short_description"]} ({(score*100):.1f}%)')


