from ast import Import
from flaskapp import app
from flask import request
import json

@app.route("/")
def index():
    return "Test"

@app.route("/test/data", methods=["POST"])
def testData():
    request_payload = request.get_json()
    data = json.loads(request_payload["payload"])
    print(data)
    return ("ok", 200)

@app.route("/test/data2", methods=["POST"])
def testData2():
    print("got data2")
    return ("ok", 200)