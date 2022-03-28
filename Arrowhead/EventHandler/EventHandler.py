from Arrowhead.EventHandler.Subscriptions import SubscriptionManager
from Arrowhead.Orchestration.Orchestration import Orchestrator
from Arrowhead.Orchestration.Services import ServiceManager
from Arrowhead import SystemConfig
from requests_pkcs12 import get, post, delete
import urllib3
import warnings
import requests

import json

class EventHandler:
    def __init__(self):
        orch = Orchestrator()
        orch.testConnection()
        orchServices = orch.orchestrate()
        self.ehServices = {}
        for key in ServiceManager.services.keys():
            if key not in orchServices.keys():
                raise Exception("Unable to orchestrate required services")
        
        # Pick the first option for each service
        # More rigorous selection can be implemented
        for service, orchResponse in orchServices.items():
            self.ehServices[service] = orchResponse["response"][0]
            


    def testConnection(self):
        ehDesc = self.ehServices["event-subscribe"]
        security = ehDesc["secure"]
        ehSystem = ehDesc["provider"]

        systemConfig = SystemConfig.loadConfig()
        certConfig = systemConfig["cert"]

        address = ehSystem["address"] + ":" + str(ehSystem["port"]) + "/eventhandler/echo"

        if security.lower() == "certificate":
             # Need to disable warning because AH main cert is not trusted
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            # Need to not verify cert because AH main cert is not trusted (verify=False)
            response = get("https://" + address, pkcs12_filename=certConfig["cloud_cert"], pkcs12_password=certConfig["cert_pass"], verify=False)
            # Reset warnings in case we need to verify other requests
            warnings.resetwarnings()
        elif security.lower() == "not_secure":
            response = get("http://" + address)

        if response.status_code != requests.codes.ok:
            raise Exception(response.status_code, response.text)

    def subscribe(self):
        SubscriptionManager.loadSubscriptions()
        ehDesc = self.ehServices["event-subscribe"]
        
        security = ehDesc["secure"]
        ehSystem = ehDesc["provider"]

        systemConfig = SystemConfig.loadConfig()
        certConfig = systemConfig["cert"]

        address = ehSystem["address"] + ":" + str(ehSystem["port"]) + ehDesc["serviceUri"]

        failedSubscriptions = {}

        for file, sub in SubscriptionManager.subscriptions.items():
            payload = {}

            payload["eventType"] = sub["eventType"]
            try:
                payload["filterMetaData"] = sub["filterMetaData"]
                payload["matchMetaData"] = True
            except:
                payload["matchMetaData"] = False

            payload["notifyUri"] = sub["notifyUri"]

            try:
                payload["sources"] = sub["sources"]
            except:
                pass
            
            payload["subscriberSystem"] = systemConfig["system"]
            print(json.dumps(payload))

            if security.lower() == "certificate":
                # Need to disable warning because AH main cert is not trusted
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                # Need to not verify cert because AH main cert is not trusted (verify=False)
                response = post("https://" + address, pkcs12_filename=certConfig["cloud_cert"], pkcs12_password=certConfig["cert_pass"], verify=False, json=payload)
                # Reset warnings in case we need to verify other requests
                warnings.resetwarnings()
            elif security.lower() == "not_secure":
                response = post("http://" + address, json=payload)

            if response.status_code != requests.codes.ok:
                failedSubscriptions[file] = response.text
        
        if failedSubscriptions:
            raise Exception("Some subscriptions could not be completed", failedSubscriptions)

    def unsibscribe(self):
        systemConfig = SystemConfig.system
        ehDesc = self.ehServices["event-unsubscribe"]

        security = ehDesc["secure"]
        ehSystem = ehDesc["provider"]

        certConfig = systemConfig["cert"]


        baseaddress = ehSystem["address"] + ":" + str(ehSystem["port"]) + ehDesc["serviceUri"]

        failedUnSub = {}

        for file, sub in SubscriptionManager.subscriptions.items():
            address = baseaddress + "?address=" + systemConfig["system"]["address"] 
            address += "&port=" + str(systemConfig["system"]["port"]) 
            address += "&system_name=" + systemConfig["system"]["systemName"]
            address += "&event_type=" + sub["eventType"]


            if security.lower() == "certificate":
                # Need to disable warning because AH main cert is not trusted
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                # Need to not verify cert because AH main cert is not trusted (verify=False)
                response = delete("https://" + address, pkcs12_filename=certConfig["cloud_cert"], pkcs12_password=certConfig["cert_pass"], verify=False)
                # Reset warnings in case we need to verify other requests
                warnings.resetwarnings()
            elif security.lower() == "not_secure":
                response = delete("http://" + address)
            
            if response.status_code != requests.codes.ok:
                failedUnSub[file] = response.text

        if failedUnSub:
            raise Exception("Some unsubscriptions could not be completed", failedUnSub)