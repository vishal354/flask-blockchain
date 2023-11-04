from flask import Flask, jsonify, render_template, request
import requests
import sys

# Initialise the port and app
app = Flask(__name__)
port = sys.argv[1]
selfAddress = f'http://localhost:{port}'

nodes = []

# Create route for the home page
@app.route('/', methods = ['GET'])
def home():
    data = "Home Page"
    return render_template('home.html', nodes=nodes)

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
    data = {
        "newNodeUrl": newNodeUrl
    }

    # Add this node to all the nodes in the network
    for node in nodes:
        address = f'{node}/connect/register'
        response = requests.post(address, json=data)
        if response.status_code == 200:
            print(f'Connected Successfully with node {node}')
        else:
            print(f"Could not register to node {node}")

    print("self node register")
    # Add this node to self
    if data['newNodeUrl'] not in nodes and data['newNodeUrl'] != selfAddress:
        nodes.append(data['newNodeUrl'])
    else:
        print(f'{node} is already added or this is address of self node.')

    # Now add all the existing nodes to the new node
    bulkRegisterUrl = f'{newNodeUrl}/connect/bulk-register'
    data = {
        "nodes": nodes + [selfAddress]
    }
    response = requests.post(bulkRegisterUrl, json=data)
    if response.status_code == 200:
        print("Successfully added a new node")
    return render_template('port.html', port=port, nodes=nodes)

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
    return data

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