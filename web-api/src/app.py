import json

import flask
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient()
db = client['twitter-data']


@app.route("/hashtag", methods=['GET'])
def hashtags():
    COLLECTION = 'hashtag'
    col = db[COLLECTION]
    return flask.Response(response=list(col.find()),
                          status=200,
                          mimetype='application/json')


@app.route("/hashtag_per_source", methods=['GET'])
def hashtags_per_source():
    COLLECTION = 'hashtag-per-source'
    col = db[COLLECTION]
    return flask.Response(response=list(col.find()),
                          status=200,
                          mimetype='application/json')


@app.route("/hashtag_per_lang", methods=['GET'])
def hashtags_per_lang():
    COLLECTION = 'hashtag-per-lang'
    col = db[COLLECTION]
    return flask.Response(response=list(col.find()),
                          status=200,
                          mimetype='application/json')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
