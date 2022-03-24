from Arrowhead.Orchestration.Orchestration import Orchestrator
from Arrowhead.EventHandler.EventHandler import EventHandler
from flaskapp import app

if __name__ == "__main__":
    #app.run(debug=True, host="0.0.0.0")
    # orch = Orchestrator()
    # orch.testConnection()
    # orch.orchestrate()
    eh = EventHandler()
    eh.testConnection()
    eh.subscribe()