from Arrowhead.Orchestration.Orchestration import Orchestrator
from Arrowhead.EventHandler.EventHandler import EventHandler
from flaskapp import app

if __name__ == "__main__":
    eh = EventHandler.getInstance()
    eh.testConnection()
    eh.subscribe()
    print("Events Subscribed")
    app.run(debug=True, host="0.0.0.0", port=8910)
    eh.unsibscribe()
    print("Events Unsubscribed")
    # orch = Orchestrator()
    # orch.testConnection()
    # orch.orchestrate()
    #eh.unsibscribe()