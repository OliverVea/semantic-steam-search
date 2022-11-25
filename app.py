from semantic_steam_search import start_initialization
from semantic_steam_search.search import is_initialized, search
from semantic_steam_search.shared import clamp
from flask import Flask, render_template, request, jsonify

# Spins up a background thread for initialization.
# Will set semantic_steam_search.search.initialized=True when finished.
start_initialization() 
                        
app = Flask(__name__)

@app.route('/api/search', methods=['GET'])
def search_endpoint() -> tuple[str, int]:
    if not is_initialized():
        return 'Search engine has not finished initialization. Please try again later.', 503

    phrase = request.args.get('phrase', '')
    phrase = phrase.replace('+', ' ')
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

@app.route('/api/healthcheck')
def healthcheck_endpoint() -> tuple[str, int]:
    return ('Healthy', 200) if is_initialized() else ('Initializing', 500)
