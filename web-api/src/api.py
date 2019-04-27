import json
import os

import flask
from flask import Flask
from pymongo import MongoClient

HOST = os.environ.get('MONGODB_HOST')

app = Flask(__name__)

client = MongoClient(host=HOST)
db = client['twitter-data']


@app.route("/hashtag", methods=['GET'])
def hashtags():
    col = db['hashtag']
    return flask.Response(
        response=json.dumps(
            list(col.find({}, {'_id': False}).sort([('_id', 1)]).limit(1))[0],
            indent=4
        ),
        status=200,
        mimetype='application/json'
    )


@app.route("/hashtag_per_source", methods=['GET'])
def hashtags_per_source():
    col = db['hashtag-per-source']
    return flask.Response(
        response=json.dumps(
            list(col.find({}, {'_id': False}).sort([('_id', 1)]).limit(1))[0],
            indent=4
        ),
        status=200,
        mimetype='application/json')


@app.route("/hashtag_per_lang", methods=['GET'])
def hashtags_per_lang():
    col = db['hashtag-per-lang']
    return flask.Response(
        response=json.dumps(
            list(col.find({}, {'_id': False}).sort([('_id', 1)]).limit(1))[0],
            indent=4
        ),
        status=200,
        mimetype='application/json'
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0')
