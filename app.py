from flask import Flask, jsonify, render_template, request
import requests
import sys
from node import *

# Initialise the port and app
app = Flask(__name__)
port = sys.argv[1]
selfAddress = f'http://localhost:{port}'
maintainNetworkNodes(selfAddress)
print("D--",distinctNodes,"  Nodes--",networkNodes,"  active--",activeNodes)

nodes = []

# Create route for the home page
@app.route('/', methods = ['GET'])
def home():
    data ={"distinctNodes":distinctNodes,
           "networkNodes":networkNodes,
           "activeNodes":activeNodes}
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
    maintainNetworkNodes(newNodeUrl)
    print("D--",distinctNodes,"  Nodes--",networkNodes,"  active--",activeNodes)
    data = {
        "newNodeUrl": newNodeUrl
    }

    if newNodeUrl not in nodes and newNodeUrl != selfAddress:
        nodes.append(data['newNodeUrl'])
    # else:
    #     print(f'{node} is already added or this is address of self node.')

    # Add this node to all the nodes in the network
    for node in nodes:
        address = f'{node}/connect/register'
        response = requests.post(address, json=data)
        if response.status_code == 200:
            print(f'Connected Successfully with node {node}')
        else:
            print(f"Could not register to node {node}")
   

    # Now add all the existing nodes to the new node
    bulkRegisterUrl = f'{newNodeUrl}/connect/bulk-register'
    data = {
        "nodes": nodes + [selfAddress]
    }
    response = requests.post(bulkRegisterUrl, json=data)
    if response.status_code == 200:
        print("Successfully added a new node")
    return render_template('port.html', port=port, nodes=nodes)

@app.route('/connect/connect2', methods=['POST', 'GET'])
def connect2():
    pass


# Add one node to the current node as a neighbour
@app.route('/connect/register',  methods = ["GET", "POST"])
def register():
    data = request.json
    print(data)

    if data['newNodeUrl'] not in nodes and data['newNodeUrl'] != selfAddress:
        nodes.append(data['newNodeUrl'])
    else:
        print('This node is already added or this is address of self node.')
    print(nodes)

    data = {
        'status': "SUCCESS",
        'nodeAddress': selfAddress
    }
    return jsonify(data)

# Return status ACTIVE if the node is running
@app.route('/activeStatus', methods=['GET'])
def activeStatus():
    data = {
        'status': 'ACTIVE',
        'address': selfAddress
    }
    return jsonify(data)


# Add all the nodes in the network returned by the initial node we connected to
@app.route('/connect/bulk-register', methods = ['GET', 'POST'])
def bulkRegister():
    data = request.json
    for node in data['nodes']:
        if node not in nodes and node != selfAddress:
            nodes.append(node)
        else:
            print(f'{node} is already added or this is address of self node.')
    
    return {
        'status': "SUCCESS",
        'nodes': nodes
    }

@app.route('/doctor/register', methods = ['GET', 'POST'])
def registerDoctor():
    return render_template('doctor_register.html')


if __name__ == "__main__":
    app.run(port=port, debug=True)
    # run_app_on_port(port)