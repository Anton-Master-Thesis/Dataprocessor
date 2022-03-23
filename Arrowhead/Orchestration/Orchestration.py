from requests_pkcs12 import post, get
import requests
import json
import os

basepath = os.path.abspath(os.path.dirname(__file__))

def orchestrate():
    config = loadConfig()

    orchConfig = config["orchestration"]

    adress = orchConfig["ip"] + ":" + str(orchConfig["port"]) + "/orchestrator/orchestration"

    payload = {}
    payload["requesterSystem"] = config["system"]
    payload["requestedService"] = config["requestedService"]
    payload["orchestrationFlags"] = config["orchestrationFlags"]

    print(json.dumps(payload))

    if orchConfig["secure"]:
        response = post("https://" + adress, pkcs12_filename=orchConfig["Cloud_cert"], pkcs12_password=orchConfig["cert_pass"], verify=False, json=payload)
    else :
        response = post("http://" + adress, json=payload)

    print(response.text)
    if response.status_code != requests.codes.ok:
        raise Exception(response.status_code, response.json())

def testConnection():
    config = loadConfig()

    orchConfig = config["orchestration"]

    adress = orchConfig["ip"] + ":" + str(orchConfig["port"]) + "/orchestrator/echo"
    if orchConfig["secure"]:
        response = get("https://" + adress, pkcs12_filename=orchConfig["Cloud_cert"], pkcs12_password=orchConfig["cert_pass"], verify=False)
    else:
        response = get("http://" + adress)

    if response.status_code != requests.codes.ok:
        return False
    
    return True

def loadConfig():
    orchConfigpath = os.path.abspath(os.path.join(basepath, "OrchestrationConfig.json"))
    with open(orchConfigpath, 'r') as f:
        configJson = json.load(f)
    return configJson