from flask import Flask, make_response, g, request, send_file, jsonify
from Domain.Nodes import Nodes
from Jobs.setupJobs import setupEvents
from Domain.httpClient import httpClient

# Instantiate the Flask app (must be before the endpoint functions)
app = Flask(__name__)
nodes = Nodes()

@app.route('/')
def greet():
    return make_response({'message': 'Hello World!'})

@app.route('/election',  methods=['GET'])
async def election():
    await httpClient().election()
    return make_response("200", 200)

@app.route('/startElection',  methods=['GET'])
def startElectionCommand():
    Nodes().amountMessages = Nodes().amountMessages + 1
    if not Nodes()._down:
        if not Nodes().isElecting():
            Nodes().raiseElectionFlag()
            senderId = request.json['sender_j']
            if Nodes().getSelfId() > senderId:
                return make_response("200", 200)
            else:
                return make_response("500", 500)
        else:
            return make_response("500", 500)
    else:
        return make_response("500", 500)

@app.route('/newCoordinator', methods=['POST'])
def updateCoordinator():
    Nodes().amountMessages = Nodes().amountMessages + 1
    if Nodes()._down:
        return make_response("500", 500)
    else:
        if Nodes().isElecting():
            Nodes().lowerElectionFlag()
            senderId = request.json['sender_j']
            nodes.setCoordinator(senderId)
        else:
            return make_response("500", 500)
        return make_response("200", 200)

@app.route('/takeover', methods=['POST'])
def takeover():
    Nodes().amountMessages = Nodes().amountMessages + 1
    if not Nodes()._down:
        httpClient().checkHigherOrBecomeCoordinator()
        return make_response("200", 200)
    else:
        return make_response("500", 500)

import requests
@app.route('/getAmountMessages', methods=['GET'])
def getAmountMessages():
    if(Nodes().getSelfId() == 1):
        nodes = Nodes().getFriendsNodesList()
        messagesDict = dict()
        messagesDict[1] = Nodes().amountMessages
        for node in nodes:
            endpoint = httpClient().getEndpoint(node)
            r = requests.get(f'{endpoint}/getAmountMessages', timeout=10)
            messagesDict[node] = int(r.text)

        return make_response(messagesDict, 200)
    else:
        return make_response(str(Nodes().amountMessages), 200)

def setupNode():
    #Setup scheduled jobs
    me = Nodes().getSelfId()
    totalNodes = os.getenv('NO_NODES')
    Nodes().generateFriendsNodesList(me, int(totalNodes))
    
    countingMessages = True
    #if(not countingMessages):
        #setupEvents()
        

if __name__ == "__main__":
    import os
    # Start the Flask app (must be after the endpoint functions)
    print(f'There is in total {os.environ.get("NO_NODES")} nodes', flush=True)
    
    setupNode()

    me = Nodes().getSelfId()

    app.run(host="0.0.0.0", port=5000)






    
    




