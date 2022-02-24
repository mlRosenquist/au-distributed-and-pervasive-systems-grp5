from multiprocessing.connection import wait
import os, time
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

@app.route('/areYouThere',  methods=['GET'])
def areYouThereCommand():
    if nodes.isState(nodes.states.down):
        return make_response(500)
    else:
        print('I am not down, sending 200')
        return make_response(200)

@app.route('/areYouNormal', methods=['GET'])
def areYouNormal():
    if nodes.isState(nodes.states.normal):
        return make_response(200)
    else:
        return make_response(500)

@app.route('/halt', methods=['POST'])
def haltCommand():
    if nodes.isState(nodes.states.down):
        return make_response(500)
    else:
        nodes.setState(nodes.states.election)
        jsonContent = request.json()
        nodes.setHaltedBy(jsonContent['sender_j'])
        return make_response(200)

@app.route('/newCoordinator', methods=['POST'])
def updateCoordinator():
    if nodes.isState(nodes.states.down):
        return make_response(500)
    else:
        senderId = request.json()['sender_j']
        if nodes.getHaltedBy() == senderId and nodes.isState(nodes.states.election):
            nodes.setCoordinator(senderId)
            nodes.setState(nodes.states.reorganizing)
        return make_response(200)

@app.route('/ready', methods=['POST'])
def ready():
    senderId = request.json()['sender_j']
    taskDescription = request.json()['work_x']
    if nodes.isState(nodes.states.down):
        return make_response(500)
    elif nodes.isState(nodes.states.reorganizing) and nodes.getCoordinator() == senderId:
        nodes.setState(nodes.states.normal)
        nodes.setTask(taskDescription)
    return make_response(200)

def setupNode():
    #Setup scheduled jobs
    me = Nodes().getSelfId()
    totalNodes = os.getenv('NO_NODES')
    if __debug__:
        totalNodes = 7
    Nodes().generateFriendsNodesList(me, totalNodes)
    setupEvents()
        

if __name__ == "__main__":
    # Start the Flask app (must be after the endpoint functions)
    #app.run(debug=True, host="0.0.0.0", port=5000)
    setupNode()

    me = Nodes().getSelfId()
    print(me)
    if(me == 1):
        time.sleep(10)
        httpClient().election()  

    app.run(host="0.0.0.0", port=5000)
  




    
    




