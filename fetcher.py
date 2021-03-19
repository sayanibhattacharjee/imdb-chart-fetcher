from flask import Flask
from bs4 import BeautifulSoup
import requests
import sys
from flask import jsonify

from scraper import ImdbSpider

app = Flask(__name__)

@app.route('/')
def main():
    # chart_url = sys.argv[1]
    # items_count = sys.argv[2]

    print("hi")
    url = 'https://www.imdb.com/india/top-rated-indian-movies'
    res =  ImdbSpider(url)
    r = res.parse()
    # res = jsonify(res)
    print("res", r)
    return 'watch movies'

