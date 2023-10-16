import requests
distinctNodes=set()
networkNodes={}
activeNodes=set()

def maintainNetworkNodes(nodeAddress):
    global distinctNodes
    global nodes
    global activeNodes
    distinctNodes.add(nodeAddress)
    activeNodes.add(nodeAddress)
    if nodeAddress not in networkNodes:
        networkNodes[nodeAddress]=[]
    print(networkNodes)
    for i in distinctNodes:
        if i!=nodeAddress:
            networkNodes[nodeAddress].append(i)
    print(networkNodes)
    for i in networkNodes:
        if i!=nodeAddress:
            networkNodes[i].append(nodeAddress)
    print("3-",networkNodes)

def maintainActiveNodes():
    global activeNodes
    global distinctNodes
    for i in distinctNodes:
        response = requests.get(i)
        if response.status_code != 200:
            activeNodes.discard(i)
            
    


