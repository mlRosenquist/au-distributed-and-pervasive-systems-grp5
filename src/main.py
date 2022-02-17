from flask import Flask, make_response, g, request, send_file
from Domain.Nodes import Nodes
from Jobs.setupJobs import setupEvents

# Instantiate the Flask app (must be before the endpoint functions)
app = Flask(__name__)

@app.route('/')
def greet():
    return make_response({'message': 'Hello World!'})

@app.route('/areYouThere',  methods=['GET'])
def areYouThereCommand():
    return make_response({'message': 'areYouTHere!'})

@app.route('/election')
def electionCommand():
    return make_response({'message': 'election!'})

@app.route('/halt')
def haltCommand():
    return make_response({'message': 'halt!'})

@app.route('/leader/update')
def updateLeader():
    newLeaderArgs = request.args['newleader']
    return make_response({'message': f'{newLeaderArgs}'})


def setupNode():
    #Setup scheduled jobs
    setupEvents()


    # Start the Flask app (must be after the endpoint functions)
    host_local_computer = "localhost" # Listen for connections on the local computer
    host_local_network = "0.0.0.0" # Listen for connections on the local network
    app.run(host=host_local_network if False else host_local_computer, port=9000)


setupNode()

