from flask import Flask, request, jsonify
from main import find_words
import re
import os

with open("/usr/share/dict/words", "r") as f:
    all_words = [i.lower() for i in f.read().splitlines()
                 if len(i) == 5 and "'" not in i]
    all_words_set = set(all_words)

wonly = re.compile(r'[^a-z]+')


def get_arg_or(arg_name, deflt):
    return got if (got := request.args.get(arg_name)) is not None else deflt


def valid_request(req):
    return all((f'g{i}' in req.args) and (f'y{i}' in req.args) for i in range(1, 6)) and 'grays' in req.args


app = Flask(__name__)


@app.route("/")
def index():
    with open('static/index.html') as f:
        return f.read()


@app.route('/search')
def search():
    if not valid_request(request):
        return jsonify({'status': 400, 'result': 'Invalid Request'}), 400

    greens = {}
    yellows = {}
    grays = []

    for i in range(1, 6):
        greens[i-1] = wonly.sub('', get_arg_or(f'g{i}', '').lower())
        yellows[i-1] = wonly.sub('', get_arg_or(f'y{i}', '').lower())

    grays = wonly.sub('', get_arg_or('grays', '').lower())

    words = list(find_words(greens, yellows, grays, all_words))
    print(f'Request to {request.remote_addr} with {len(words)} words.')

    return jsonify({'status': 200, 'result': {'words': words,  'count': len(words)}}), 200


@app.route('/exists')
def exists():
    word = get_arg_or('word', '')
    if ',' in word:
        words = word.split(',')
    else:
        words = [word]

    words = [wonly.sub('', word) for word in words]
    result = {word: word in all_words_set for word in words}
    return jsonify({'status': 200, 'result': result}), 200


if __name__ == '__main__':
    from waitress import serve
    port = int(os.environ['PORT']) if 'PORT' in os.environ else 5005
    print(f'Serving on localhost: {port}')
    serve(app, host="0.0.0.0", port=port)
