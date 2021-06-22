from flask import Flask, render_template, request
from dialogue_manager import *
from flask_restful import reqparse, abort, Api, Resource
import pickle
import numpy as np


app = Flask(__name__)
dialogue_manager = DialogueManager()


@app.route("/")
def home():
    return render_template("index.html")

#parser = reqparse.RequestParser()
#parser.add_argument('query')
#@app.route("/api/",methods=['POST'])
@app.route("/get")
def get_bot_response():
    #args = parser.parse_args()
    #userText = args['query']
    userText = request.args.get('msg')
    return str(dialogue_manager.generate_answer(userText))
# Run Program


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(80))
