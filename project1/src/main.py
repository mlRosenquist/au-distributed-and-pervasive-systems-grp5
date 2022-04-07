from distutils.log import debug
from http.client import HTTP_PORT
from flask import Flask, make_response, g, request, send_file, jsonify
from Domain.Nodes import Nodes
from Jobs.setupJobs import setupEvents
from multiprocessing.connection import wait
import os, time
from Domain.httpClient import httpClient
import asyncio
import requests
import threading

# Instantiate the Flask app (must be before the endpoint functions)
app = Flask(__name__)
nodes = Nodes()


@app.route('/')
def greet():
    return make_response({'message': 'Hello World!'})

@app.route('/election',  methods=['GET'])
async def election():
    Nodes().amountMessages = Nodes().amountMessages + 1
    
    await httpClient().election()
    # Attempt of doing asynchronous communicate
    #t = threading.Thread(name="dada", target=httpClient().electionSync)
    #t.start()
    return make_response("OK", 200)

@app.route('/areYouThere',  methods=['GET'])
async def areYouThereCommand():
    Nodes().amountMessages = Nodes().amountMessages + 1
    if nodes.isState(nodes.states.down):
        print('I am down, sending 500')
        return make_response("500", 500)
    else:
        print('I am not down, sending 200')
        return make_response("200", 200)

@app.route('/areYouNormal', methods=['GET'])
def areYouNormal():
    Nodes().amountMessages = Nodes().amountMessages + 1
    if nodes.isState(nodes.states.normal):
        return make_response("200", 200)
    else:
        return make_response("500", 500)

@app.route('/halt', methods=['POST'])
def haltCommand():
    Nodes().amountMessages = Nodes().amountMessages + 1
    if nodes.isState(nodes.states.down):
        return make_response("500", 500)
    else:
        nodes.setState(nodes.states.election)
        jsonContent = request.json
        nodes.setHaltedBy(jsonContent['sender_j'])
        return make_response("200", 200)

@app.route('/newCoordinator', methods=['POST'])
def updateCoordinator():
    Nodes().amountMessages = Nodes().amountMessages + 1
    if nodes.isState(nodes.states.down):
        return make_response("500", 500)
    else:
        senderId = request.json['sender_j']
        if nodes.getHaltedBy() == senderId and nodes.isState(nodes.states.election):
            nodes.setCoordinator(senderId)
            nodes.setState(nodes.states.reorganizing)
        return make_response("200", 200)

@app.route('/ready', methods=['POST'])
def ready():
    Nodes().amountMessages = Nodes().amountMessages + 1
    senderId = request.json['sender_j']
    taskDescription = request.json['work_x']
    if nodes.isState(nodes.states.down):
        return make_response("500", 500)
    elif nodes.isState(nodes.states.reorganizing) and nodes.getCoordinator() == senderId:
        nodes.setState(nodes.states.normal)
        nodes.setTask(taskDescription)
    return make_response("200", 200)

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
    if(not countingMessages):
        setupEvents()
        

if __name__ == "__main__":
    # Start the Flask app (must be after the endpoint functions)
    print(f'There is in total {os.environ.get("NO_NODES")} nodes', flush=True)
    
    setupNode()

    me = Nodes().getSelfId()
    # if(me == 1):
    #     time.sleep(10)
    #     httpClient().election()  

    app.run(host="0.0.0.0", port=5000)
  




    
    




