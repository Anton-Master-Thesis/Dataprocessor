from asyncio.windows_events import NULL
from requests_pkcs12 import post, get
import urllib3
import warnings
import requests
import json
import os

# Starts the orchestration process
# Raises Exception if the http resonse code from the orchestrator is not 2xx or 3xx
def orchestrate():
    config = con.loadConfig()
    orchConfig = config["orchestrationConfig"]
    orchRequest = config["orchestrationRequest"]

    # build the adress to request
    adress = orchConfig["ip"] + ":" + str(orchConfig["port"]) + "/orchestrator/orchestration"

    # build the orchestration request payload
    payload = {}
    payload["requesterSystem"] = orchRequest["system"]
    payload["requestedService"] = orchRequest["requestedService"]
    payload["orchestrationFlags"] = orchRequest["orchestrationFlags"]

    # check if we need to use http or https
    if orchConfig["secure"]:
        # Need to disable warning because AH main cert is not trusted
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # Need to not verify cert because AH main cert is not trusted (verify=False)
        response = post("https://" + adress, pkcs12_filename=orchConfig["Cloud_cert"], pkcs12_password=orchConfig["cert_pass"], verify=False, json=payload)
        # Reset warnings in case we need to verify other requests
        warnings.resetwarnings()
    else :
        response = post("http://" + adress, json=payload)

    # Check if request was successful
    if response.status_code != requests.codes.ok:
        raise Exception(response.status_code, response.json())

    return response.json()

# Tests the connection via the /echo endpoint of the orchestrator
# Raises exception if connection could not be established
def testConnection():
    config = con.loadConfig()

    orchConfig = config["orchestrationConfig"]

    adress = orchConfig["ip"] + ":" + str(orchConfig["port"]) + "/orchestrator/echo"
    if orchConfig["secure"]:
         # Need to disable warning because AH main cert is not trusted
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # Need to not verify cert because AH main cert is not trusted (verify=False)
        response = get("https://" + adress, pkcs12_filename=orchConfig["Cloud_cert"], pkcs12_password=orchConfig["cert_pass"], verify=False)
        # Reset warnings in case we need to verify other requests
        warnings.resetwarnings()
    else:
        response = get("http://" + adress)

    # Check if request was successful
    if response.status_code != requests.codes.ok:
        raise Exception(response.status_code, "Unable to connect to the orchestrator")

class Config:
    orchestrationConfig = {}
    basepath = os.path.abspath(os.path.dirname(__file__))
    # Load the orchestration configuration file which describes which service to connect to and where/how to contact the orchestrator
    def loadConfig(self):
        if not self.orchestrationConfig:
            orchConfigpath = os.path.abspath(os.path.join(self.basepath, "OrchestrationConfig.json"))
            with open(orchConfigpath, 'r') as f:
                self.orchestrationConfig = json.load(f)
        return self.orchestrationConfig

con = Config()