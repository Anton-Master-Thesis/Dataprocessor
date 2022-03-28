# Dataprocessor
mockup of a generic data processor which connect to the arrowhead framework using python and flask

## Setup
create a folder venv

> mkdir venv

install venv via the command

> py -3 -m venv venv

activate the virtual environment

linux

> . venv/Script/activate

windows 

> venv/Script/activate

install required libraries

> pip install -r requirements.txt

run the project

> python run.py

## Configuration
There are several configuration/description files.
These determine what is sent to the core systems.

In the Arrowhead folder there is the SystemConfig.json file.
This specifies where the system is located and which certificate to use. It is important that the host and port coincides with the flaskapp. (Note, the certificate "common name" need to be the same as the systemName).

In the Arrowhead/EvenHandler/Subscriptions folder there are several json files. 
These files describes which events the system should subscribe to and which url paths the data will be sent to.
If new files are added they need to adhere to the json schema located in the same folder.

In the Arrowhead/Orchestration folder there is a OrchestrationConfig.json file.
This file describes where the orchestrator is hosted and if it is secure or not.

In the Arrowhead/Orchestration/Services folder there are several json files.
These files describe which services the system will consume.
Currently it only need to consume the subscription related services from the EventHandler but more can be added.

## Structure
### Arrowhead
In the arrowhead folder all things arrowhead are located.
The system config describes the system for use in Arrowhead.

#### EventHandler
This folder contains everything related to the EventHandler.
The file "EventHandler.py" contains a class "EventHandler" which orchestrates and subscribes to the subscriptions defined in the "Subscriptions" folder.
This is done dynamically when the EventHandler class is instanciated.

#### Orchestration
This folder contains everything related to the orchestration process.
The file "Orchestrator.py" contains the class "Orchestrator" which can orchestrate the services described in the Services folder. This is done dynamically and is done every time the orchestrate method is called.

### flaskapp
The flask app folder contains everything related to the http server and providing services.

In the data folder there is a route.py file which contains all endpoint provided by the system.