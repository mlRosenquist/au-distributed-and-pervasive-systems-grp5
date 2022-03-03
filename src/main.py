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

@app.route('/startElection',  methods=['GET'])
def startElectionCommand():
    if not Nodes()._down:
        Nodes().raiseElectionFlag()
        senderId = request.json['sender_j']
        if Nodes().getSelfId() > senderId:
            return make_response("200", 200)
        else:
            return make_response("500", 500)
    else:
        return make_response("500", 500)

@app.route('/newCoordinator', methods=['POST'])
def updateCoordinator():
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
    if not Nodes()._down:
        httpClient().checkHigherOrBecomeCoordinator()
        return make_response("200", 200)
    else:
        return make_response("500", 500)

def setupNode():
    #Setup scheduled jobs
    setupEvents()

if __name__ == "__main__":
    # Start the Flask app (must be after the endpoint functions)
    #app.run(debug=True, host="0.0.0.0", port=5000)
    setupNode()
    app.run(host="0.0.0.0", port=5000)




    
    




