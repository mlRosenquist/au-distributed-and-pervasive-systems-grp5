from flask import Flask, make_response, g, request, send_file, jsonify
from Domain.Nodes import Nodes
from Jobs.setupJobs import setupEvents

# Instantiate the Flask app (must be before the endpoint functions)
app = Flask(__name__)
nodes = Nodes()

@app.route('/')
def greet():
    return make_response({'message': 'Hello World!'})

@app.route('/areYouThere',  methods=['GET'])
def areYouThereCommand():
    if nodes.isState(nodes.states.down):
        return make_response(200)
    else:
        return make_response(500)

@app.route('/election', methods=['POST'])
def electionCommand():
    return make_response({'message': 'election!'})

@app.route('/halt', methods=['POST'])
def haltCommand():
    return make_response({'message': 'halt!'})

@app.route('/newCoordinator', methods=['POST'])
def updateLeader():
    newLeaderArgs = request.args['newleader']
    return make_response({'message': f'{newLeaderArgs}'})

def setupNode():
    #Setup scheduled jobs
    setupEvents()

if __name__ == "__main__":
    # Start the Flask app (must be after the endpoint functions)
    app.run(debug=True, host="0.0.0.0", port=5000)
    setupNode()




    
    




