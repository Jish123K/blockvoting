from typing import List

from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

from aiohttp import ClientSession

app = FastAPI()

class Transaction(BaseModel):

    sender: str

    recipient: str

    amount: float

class Block(BaseModel):

    index: int

    timestamp: float

    transactions: List[Transaction]

    proof: int

    previous_hash: str

class Blockchain:

    def __init__(self):

        self.chain = []

        self.current_transactions = []

        # Create the genesis block

        self.new_block(proof=100, previous_hash='1')

    def new_block(self, proof: int, previous_hash: str) -> Block:

        block = Block(

            index=len(self.chain) + 1,

            timestamp=time(),

            transactions=self.current_transactions,

            proof=proof,

            previous_hash=previous_hash

        )

        self.current_transactions = []

        self.chain.append(block)

        return block

    def new_transaction(self, sender: str, recipient: str, amount: float) -> int:

        self.current_transactions.append(Transaction(sender=sender, recipient=recipient, amount=amount))

        return self.last_block.index + 1

    @property

    def last_block(self) -> Block:

        return self.chain[-1]

    def proof_of_work(self, last_proof: int) -> int:

        proof = 0

        while self.valid_proof(last_proof, proof) is False:

            proof += 1

        return proof

    @staticmethod

    def valid_proof(last_proof: int, proof: int) -> bool:

        guess = f'{last_proof}{proof}'.encode()

        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:4] == "0000"

    def validate_chain(self, chain: List[Block]) -> bool:

        last_block = chain[0]

        current_index = 1

        while current_index < len(chain):

            block = chain[current_index]

            if block.previous_hash != self.hash(last_block):

                return False

            if not self.valid_proof(last_block.proof, block.proof):

                return False

            last_block = block

            current_index += 1

        return True

    @staticmethod

    def hash(block: Block) -> str:

        block_string = json.dumps(block.dict(), sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()

blockchain = Blockchain()

# the address to other participating members of the network

peers = set()

# endpoint to add new peers to the network.

@app.post('/add_node')

async def register_new_peers(ipaddress: str, port: int):

    node = f"{ipaddress}:{port}"

    peers.add(node)

    return {"message": "New node added", "node": node}

async def broadcast_block(block: Block):

    async with ClientSession() as session:

        for peer in peers:

            try:

                async with session.post(f"http://{peer}/add_block", json=block.dict()) as response:

                    if response.status != 201:

                        print(f"Unable to broadcast block to {peer}: {response.status}")

            except (ClientConnectorError, ClientOSError):

                print(f"Unable to connect to {peer}")

async def broadcast_transaction(transaction: Transaction):

    async with ClientSession() as session:

        for peer in peers:

            try:

                async with session.post(f"http://{peer}/add_transaction", json=transaction.dict()) as response:

                    if response.status != 201:

                        print(f"Unable to broadcast transaction to {peer}: {response
async def broadcast_transaction(transaction: Transaction):

async with ClientSession() as session:

for peer in peers:

try:

async with session.post(f"http://{peer}/add_transaction", json=transaction.dict()) as response:

if response.status != 201:

print(f"Unable to broadcast transaction to {peer}: {response.status}")

except (ClientConnectorError, ClientOSError):

print(f"Unable to connect to {peer}")

endpoint to add a new transaction to the current block

@app.post('/add_transaction')

async def add_transaction(transaction: Transaction):

index = blockchain.new_transaction(transaction.sender, transaction.recipient, transaction.amount)

await broadcast_transaction(transaction)

return {"message": f"Transaction will be added to Block {index}"}

endpoint to return the node's copy of the chain

@app.get('/chain')

async def get_chain():

return {"chain": blockchain.chain, "length": len(blockchain.chain)}

endpoint to mine a new block

@app.post('/mine')

async def mine():

last_block = blockchain.last_block

last_proof = last_block.proof

proof = blockchain.proof_of_work(last_proof)

python

Copy code

# reward for mining the block

blockchain.new_transaction(

    sender="0",

    recipient="node",

    amount=1.0

)

previous_hash = blockchain.hash(last_block)

block = blockchain.new_block(proof, previous_hash)

await broadcast_block(block)

return {"message": "New Block Forged", "block": block.dict()}

endpoint to add a block to the chain

@app.post('/add_block')

async def add_block(block: Block):

if block.index == len(blockchain.chain) + 1 and block.previous_hash == blockchain.hash(blockchain.last_block):

blockchain.chain.append(block)

return {"message": "Block added to chain", "block": block.dict()}

raise HTTPException(status_code=400, detail="Invalid block")

if name == 'main':

import uvicorn

uvicorn.run(app, host='0.0.0.0', port=8000)


