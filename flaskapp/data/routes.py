from flaskapp import app
from flask import request
from Arrowhead.EventHandler.EventHandler import EventHandler

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

import json

def verify(request_payload):
    systemName = request_payload["metaData"]["systemName"]
    eh = EventHandler.getInstance()
    publishersServices = eh.getPublishers()
    for service, publishers in publishersServices.items():
        for publisher in publishers:
            if systemName == publisher["provider"]["systemName"]:
                p_metaData = publisher["provider"]["metadata"]
                e = p_metaData["pub_key_e"]
                n = p_metaData["pub_key_n"]
                e = int(e)
                n = int(n)
                public_num = rsa.RSAPublicNumbers(e,n)
                public_key = public_num.public_key()

    if public_key:
        payload = json.loads(request_payload["payload"])
        data = payload["data"]
        message = json.dumps(data).encode("utf-8")
        signature = bytes.fromhex(payload["signature"])
        public_key.verify(signature, message, padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())





@app.route("/")
def index():
    return "Test"

@app.route("/test/data", methods=["POST"])
def testData():
    request_payload = request.get_json()
    verify(request_payload)
    data = json.loads(request_payload["payload"])
    print(request_payload)
    return ("ok", 200)

@app.route("/test/data2", methods=["POST"])
def testData2():
    print("got data2")
    request_payload = request.get_json()
    data = json.loads(request_payload["payload"])
    print(data)
    return ("ok", 200)