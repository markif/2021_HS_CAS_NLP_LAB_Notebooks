#!/usr/bin/python3

# python3 -m pip install Flask flask-cors fhnw-nlp-utils
# see https://github.com/inception-project/inception-external-recommender for inception integration
# you might need to make this file executable by `sudo chmod +x rest_server.py`
import json
import logging
import flask
from flask import request, abort, jsonify
from flask_cors import cross_origin
import pandas as pd

from fhnw.nlp.utils.storage import download
from fhnw.nlp.utils.storage import load_pickle

logging.basicConfig(level=logging.INFO)

app = flask.Flask(__name__)

# re-download the latest version of the classifier from storage
# this allows for releasing new versions by simply replacing the file on the storage
# but you need to be careful since this also easily allows a potential intruder to replace the file (which the effect that you execute the intruder's code)
app.logger.info("Download sentiment classifier...")
download("https://drive.google.com/uc?id=1fHyebcXVvD1YlnrzQPLu8MTpurJB-X64", "classifier/sentiment_classifier.pgz", re_download=True)
sentiment_classifier = load_pickle("classifier/sentiment_classifier.pgz")
app.logger.info("Sentiment classifier created.")
port=5000

@app.route("/api/v1/sentiment", methods=["POST"])
@cross_origin()
def api_sentiment():
    data = None
    
    if request.content_type == "application/json":
        jsn = request.get_json()
        if isinstance(jsn, list):
            data = pd.DataFrame(jsn, columns =["text_original"])
    elif request.content_type == "text/plain":
        text = request.get_data(as_text=True)
        data = pd.DataFrame([text], columns =["text_original"])

    if data is not None:
        sentiments = sentiment_classifier.predict(data)
        return jsonify(sentiments.tolist())
    else:
        abort(400, description="Request did not contain JSON array nor text")

app.run('0.0.0.0', port=port, debug=False)
