from flask import Flask

app = Flask(__name__)


@app.route("/hashtags")
def hashtags():
    return "Hashtag"


@app.route("/hashtags_per_source")
def hashtags_per_source():
    return "Hashtag per source"


@app.route("/hashtags_per_lang")
def hashtags_per_lang():
    return "Hashtag per lang"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
