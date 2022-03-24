from Arrowhead.Orchestration.Orchestration import Orchestrator
from Arrowhead import SystemConfig
from requests_pkcs12 import get, post
import urllib3
import warnings
import requests
import json


class EventHandler:
    def __init__(self):
        orch = Orchestrator()
        orch.testConnection()
        orchResp = orch.orchestrate()
        if len(orchResp["response"]) > 1:
            # filter which event subscribe service to use
            # Currently using first
            self.ehDesc = orchResp["response"][0]
            pass
        elif len(orchResp["response"]) == 1:
            self.ehDesc = orchResp["response"][0]
        else:
            raise Exception("Could not find EventHandler")

    def testConnection(self):
        security = self.ehDesc["secure"]
        ehSystem = self.ehDesc["provider"]

        systemConfig = SystemConfig.loadConfig()
        certConfig = systemConfig["cert"]

        adress = ehSystem["address"] + ":" + str(ehSystem["port"]) + "/eventhandler/echo"

        if security.lower() == "certificate":
             # Need to disable warning because AH main cert is not trusted
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            # Need to not verify cert because AH main cert is not trusted (verify=False)
            response = get("https://" + adress, pkcs12_filename=certConfig["cloud_cert"], pkcs12_password=certConfig["cert_pass"], verify=False)
            # Reset warnings in case we need to verify other requests
            warnings.resetwarnings()
        elif security.lower() == "not_secure":
            response = get("http://" + adress)

        if response.status_code != requests.codes.ok:
            raise Exception(response.status_code, response.text)
        
        print(response.status_code)