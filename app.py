from flask import Flask, request
from main import find_words
import re 

app = Flask(__name__)

@app.route("/")
def index():
    with open('static/index.html') as f:
        return f.read()

wonly = re.compile(r'[^a-z]')

@app.route('/search')
def search():
    greens = {}
    yellows = {}
    grays = []

    for i in range(1, 6):
        g = request.args.get(f'g{i}').lower()
        y = request.args.get(f'y{i}').lower()

        g = wonly.sub(g, '')
        y = wonly.sub(y, '')

        greens[i-1] = g 
        yellows[i-1] = y 
    
    grays = request.args.get('grays').lower()
    grays = wonly.sub(grays, '')
    # print(greens, yellows, grays)

    return '<br>'.join(find_words(greens, yellows, grays))
