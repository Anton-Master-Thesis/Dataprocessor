from Arrowhead.Orchestration.Orchestration import orchestrate, testConnection
from flaskapp import app
from Arrowhead.Orchestration import *

if __name__ == "__main__":
    #app.run(debug=True, host="0.0.0.0")
    if not testConnection():
        raise Exception("Unable to connect to orchestrator")
    orchestrate()