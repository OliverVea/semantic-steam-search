from flask import Flask, request, jsonify
from semantic_steam_search import start_initialization
from semantic_steam_search.search import search, initialized
from semantic_steam_search.shared import clamp

# Just to make super sure no nested thread spawning shenanigans happens.
if __name__ == '__main__':
    # Spins up a background thread for initialization.
    # Will set semantic_steam_search.search.initialized=True when finished.
    start_initialization() 
                        
app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search_endpoint():
    if not initialized:
        return 'Search engine has not finished initialization. Please try again later.', 503

    phrase = request.args.get('phrase', '')
    if len(phrase) == 0:
        return 'A search phrase with a non-zero length must be provided.', 400
    
    offset = request.args.get('offset', 0, type=int)
    offset = max(0, offset)

    count = request.args.get('count', 12, type=int)
    count = clamp(0, count, 100)

    try:
        result = search(phrase=phrase, offset=offset, count=count)
        return jsonify(result)
    
    except Exception:
        return 'An error occured. Please try again later.', 500

@app.route('/healthcheck')
def healthcheck_endpoint():
    return 200 if initialized else 500
