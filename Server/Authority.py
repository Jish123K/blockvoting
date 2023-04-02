from typing import Dict, List

from fastapi import FastAPI, Request, HTTPException

from pydantic import BaseModel

import requests

app = FastAPI()

orderer = '0.0.0.0'

# the address to other participating members of the network

peers = set()

# list grouped peers

groups = {}

# list permission for each group

# O : Open | C : Close | V : Vote

permission = { 'admin' : 'OCVSE', 'peer' : 'OCVSE', 'guest' : 'V' }

groups[request.client.host + ':5000'] = 'admin'

class Node(BaseModel):

    ipaddress: str

    port: int

class Permission(BaseModel):

    peer: str

    action: str

@app.post('/add_node')

async def validate_connection(node: Node):

    request_addr = request.client.host

    peers.add(f"{request_addr}:{node.port}")

    # add some role with node in here

    # set permission for node 

    if f"{request_addr}:{node.port}" not in groups:

        groups[f"{request_addr}:{node.port}"] = 'peer'

    url = f"http://{orderer}:5002/add_node"

    response = requests.post(url, json={'ipaddress': request_addr, 'port': node.port})

    if response.status_code >= 400:

        raise HTTPException(status_code=400, detail="Error to connect to orderer")

    return {"msg": "Success"}

@app.post('/validate_permission')

async def validate_permission(permission: Permission):

    node = permission.peer

    action = permission.action

    if node not in groups:

        groups[node] = 'guest'

    if action[0].upper() in permission[groups[node]]:

        return {'decision': 'accept'}

    else:

        return {'decision': 'reject'}

if __name__ == '__main__':

    import uvicorn

    parser = ArgumentParser()

    parser.add_argument('-p', '--port', default=5001, type=int, help='port to listen on')

    parser.add_argument('--orderer', default='0.0.0.0', type=str, help='port to listen on')

    args = parser.parse_args()

    port = args.port

    orderer = args.orderer

    print('My ip address : ' + request.client.host)

    uvicorn.run(app, host='0.0.0.0', port=port)

