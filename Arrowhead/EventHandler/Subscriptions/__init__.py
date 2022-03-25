import json
import os
import glob

class SubscriptionManager:
    subscriptions = {}

    @staticmethod
    def loadSubscriptions():
        path = basepath = os.path.abspath(os.path.dirname(__file__))
        subspath = glob.glob(path + "/*.json")
        cleanSubsPath = []
        for sub in subspath:
            if ".schema." not in sub:
                cleanSubsPath.append(sub)
        for sub in cleanSubsPath:
            with open(sub, 'r') as f:
                SubscriptionManager.subscriptions[os.path.basename(sub)] = (json.load(f))