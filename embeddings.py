from sentence_transformers import SentenceTransformer
import json
import pickle

embedder = SentenceTransformer('all-MiniLM-L6-v2')

print('Loading games')
with open('steam_games.json', 'r') as f:
    games = json.load(f)

# Corpus with example sentences
print('Loading corpus')

def get_corpus_text(game: dict) -> str:
    fields = [game['name'], game['short_description'], game['genre']]
    #fields += game['tags'].keys()
    #fields += game['categories']
    return ' '.join(fields)

corpus = [get_corpus_text(game) for game in games.values()]

print('Saving corpus')
with open('corpus.pickle', 'wb') as f:
    pickle.dump(corpus, f)

print('Calculating embeddings')
corpus_embeddings = embedder.encode(corpus, show_progress_bar=True, convert_to_tensor=True, batch_size=128)

print('Saving embeddings')
with open('embeddings.pickle', 'wb') as f:
    pickle.dump(corpus_embeddings, f)

print('Done!')
