from semantic_steam_search import start_initialization
from semantic_steam_search.search import SearchRequest, is_initialized, search
from semantic_steam_search.shared import BASE_URL, clamp
from flask import Flask, render_template, request, jsonify

# Spins up a background thread for initialization.
# Will set semantic_steam_search.search.initialized=True when finished.
start_initialization() 
                        
app = Flask(__name__)


def get_link(phrase: str, offset: int) -> str:
    url = f'{BASE_URL}'
    arguments = []

    if phrase: arguments.append(f'phrase={phrase}')
    if offset: arguments.append(f'offset={offset}')
    if len(arguments) > 0: url += '?' + '&'.join(arguments)

    return url


@app.route('/')
def index_endpoint():
    products = []
    search_request = search_request_from_query_params()
    if is_initialized():
        try:
            result = search(search_request)
            products = result['hits']
        
        except Exception:
            pass

    return render_template('index.html', 
        products=products, 
        url=BASE_URL,
        phrase=search_request.phrase,
        current_page = (search_request.offset // search_request.results) + 1,
        next_link=get_link(search_request.phrase, search_request.offset + search_request.results),
        previous_link=get_link(search_request.phrase, search_request.offset - search_request.results),
        include_previous = search_request.offset >= search_request.results)

@app.route('/api/search', methods=['GET'])
def search_endpoint() -> tuple[str, int]:
    if not is_initialized():
        return 'Search engine has not finished initialization. Please try again later.', 503

    try:
        search_request = search_request_from_query_params()
        result = search(search_request)
        return jsonify(result)
    
    except Exception:
        return 'An error occured. Please try again later.', 500

@app.route('/api/healthcheck')
def healthcheck_endpoint() -> tuple[str, int]:
    return ('Healthy', 200) if is_initialized() else ('Initializing', 500)



def search_request_from_query_params():    
    phrase = request.args.get('phrase', '')
    phrase = phrase.replace('+', ' ')
    
    offset = request.args.get('offset', 0, type=int)
    offset = max(0, offset)

    count = request.args.get('count', 12, type=int)
    count = clamp(0, count, 100)

    return SearchRequest(phrase, offset, count)
