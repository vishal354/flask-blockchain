from flask import Flask, jsonify, render_template, request
import requests
import sys
from node import *
from util import CLIENT as client

# Initialise the port and app
app = Flask(__name__)
port = sys.argv[1]
selfAddress = f'http://localhost:{port}'

# Create route for the home page
@app.route('/', methods = ['GET'])
def home():
    data =networkNodes
    return render_template('home.html', data=data)

# Chose the node where you want to connect
@app.route('/connect', methods = ['GET'])
def displayConnectPage():
    print("This is working")
    return render_template('connect.html')

# Try to connect a node to another node in the network
# Only a node in the blockchain network can invite a new node
@app.route('/connect/connect', methods=['POST', 'GET'])
def connect():
    port = request.form.get('port', type=int)
    newNodeUrl = f'http://localhost:{port}'
    response = requests.get(newNodeUrl)
    if newNodeUrl!=selfAddress:
        data = {
            "newNodeUrl": newNodeUrl
        }
        for node in networkNodes:
            address = f'{node}/connect/register'
            response = requests.post(address, json=data)
            if response.status_code == 200:
                print(f'Connected Successfully with node {node}')

        # Now add all the existing nodes to the new node
        bulkRegisterUrl = f'{newNodeUrl}/connect/bulk-register'
        data = {
            "nodes": list(networkNodes) + [selfAddress]
        }
        response = requests.post(bulkRegisterUrl, json=data)
        if response.status_code == 200:
            print("Successfully added a new node")
        maintainNetworkNodes(newNodeUrl)
        print(f"selfAddress:{selfAddress} , networkNodes: {networkNodes}")
    return render_template('port.html', port=port, nodes=networkNodes)

# Add one node to the current node as a neighbour
@app.route('/connect/register',  methods = ["GET", "POST"])
def register():
    data = request.json
    print(data)
    maintainNetworkNodes(data['newNodeUrl'])
    print(f"selfAddress:{selfAddress} , networkNodes: {networkNodes}")

    data = {
        'status': "SUCCESS",
        'nodeAddress': selfAddress
    }
    return jsonify(data)

# Return status ACTIVE if the node is running
@app.route('/activeStatus', methods=['GET'])
def activeStatus():
    maintainActiveNodes()
    print(activeNodes)
    data = {
        'status': 'ACTIVE',
        'selfAddress': selfAddress,
        'activeNodes':activeNodes
    }
    return jsonify(data)

# Add all the nodes in the network returned by the initial node we connected to
@app.route('/connect/bulk-register', methods = ['GET', 'POST'])
def bulkRegister():
    data = request.json
    for node in data['nodes']:
        maintainNetworkNodes(node)
    print(f"selfAddress:{selfAddress} , networkNodes: {networkNodes}")
    return {
        "status": "SUCCESS"
    }

# @app.route('/doctor/register', methods = ['GET', 'POST'])
# def registerDoctor():
#     return render_template('doctor_register.html')

# @app.route('/process_form', methods=['POST'])
# def process_form():
#     name = request.form.get('name')
#     email = request.form.get('email')
#     # You can now use the 'name' and 'email' variables for further processing.
#     # For example, you can store the data in a database, perform some logic, or render a response page.
#     return f"Received data: Name - {name}, Email - {email}"

if __name__ == "__main__":
    app.run(port=port, debug=True)