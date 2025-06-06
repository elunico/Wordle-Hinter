from flask import Flask, request, jsonify
from main import find_words
import re 
import os 


app = Flask(__name__)

@app.route("/")
def index():
    with open('static/index.html') as f:
        return f.read()

wonly = re.compile(r'[^a-z]+')

@app.route('/search')
def search():
    greens = {}
    yellows = {}
    grays = []

    for i in range(1, 6):
        greens[i-1] = wonly.sub('', request.args.get(f'g{i}').lower())
        yellows[i-1] = wonly.sub('', request.args.get(f'y{i}').lower())
    
    grays = wonly.sub('', request.args.get('grays').lower())

    words = list(find_words(greens, yellows, grays))
    print(f'Request to {request.remote_addr} with {len(words)} words.')

    return jsonify( {'words': words})

if __name__ == '__main__':
    from waitress import serve
    port = int(os.environ['PORT']) if 'PORT' in os.environ else 5005
    serve(app, host="0.0.0.0", port=port)
    print(f'Serving on localhost: {port}' )
