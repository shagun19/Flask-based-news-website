import json

from flask import Flask, jsonify, request
from newsapi import NewsApiClient

app = Flask(__name__)

newsapi = NewsApiClient(api_key='88f07e73d2474e64a2f2399a05e3c3ca')


@app.route('/google/news', methods=['GET'])
def get_top_headlines():
    top_headlines = newsapi.get_top_headlines(country='us')
    return top_headlines


@app.route('/google/source', methods=['GET'])
def get_top_headlines_by_source():
    source = request.args.get('source', default='cnn', type=str)
    top_headlines = newsapi.get_top_headlines(sources=source, page_size=30)
    return top_headlines


@app.route('/google/everything', methods=['GET'])
def get_articles_based_on_search_query():
    query = request.args.get('query', default='', type=str)
    start_date = request.args.get('start_date', default='', type=str)
    end_date = request.args.get('end_date', default='', type=str)
    source = request.args.get('sources', default='', type=str)
    try:
        articles = newsapi.get_everything(q=query, sources=source, from_param=start_date, to=end_date,
                                          sort_by="publishedAt", language='en')
        return articles
    except Exception as e:
        message = str(e)
        message = message.replace("'", "\"")
        message = json.loads(message)
        return message


@app.route('/google/findsource', methods=['GET'])
def get_sources_based_on_category():
    category = request.args.get('category', default='', type=str)
    if len(category) != 0:
        sources = newsapi.get_sources(category=category, country='us', language='en')
    else:
        sources = newsapi.get_sources()
    return sources


@app.route('/')
def index1():
    return app.send_static_file('indexFinal.html')


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)
