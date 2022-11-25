from flask import Flask, request, jsonify

from semantic_steam_search.data import initialize_data
from semantic_steam_search.embeddings import initialize_embeddings
from semantic_steam_search.search import initialize_search, search

initialize_data()
initialize_embeddings()
initialize_search()

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search_endpoint():
    phrase = request.args.get('phrase', '')
    offset = request.args.get('offset', 0, type=int)
    count = request.args.get('count', 12, type=int)

    result = search(phrase=phrase, offset=offset, count=count)
    return jsonify(result)
