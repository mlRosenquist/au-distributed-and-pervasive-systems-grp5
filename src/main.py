from flask import Flask, make_response, g, request, send_file
from Jobs.setupJobs import setupEvents

# Instantiate the Flask app (must be before the endpoint functions)
app = Flask(__name__)

@app.route('/')
def Greet():
    return make_response({'message': 'Hello World!'})

def setupNode():
    #Setup scheduled jobs
    setupEvents()


    # Start the Flask app (must be after the endpoint functions)
    host_local_computer = "localhost" # Listen for connections on the local computer
    host_local_network = "0.0.0.0" # Listen for connections on the local network
    app.run(host=host_local_network if False else host_local_computer, port=9000)


setupNode()