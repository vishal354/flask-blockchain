import requests
networkNodes=set()
activeNodes=set()

def maintainNetworkNodes(nodeAddress):
    global networkNodes
    global activeNodes
    networkNodes.add(nodeAddress)
    activeNodes.add(nodeAddress)
    print(f" networkNodes: {networkNodes}")

def maintainActiveNodes():
    global activeNodes
    global networkNodes
    for i in networkNodes:
        activeNodes.add(i)
    for i in networkNodes:
        response = requests.get(i)
        if response.status_code != 200:
            activeNodes.discard(i)