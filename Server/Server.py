from fastapi import FastAPI, HTTPException

import requests

import time

import asyncio

app = FastAPI()

blockchain = Blockchain()

class Blockchain:

    def __init__(self):

        self.chain = []

        self.unconfirmed_transactions = []

    def add_new_transaction(self, tx_data):

        self.unconfirmed_transactions.append(tx_data)

    def proof_of_work(self, block):

        # Implementation of proof of work algorithm

        pass

    def add_block(self, block, proof):

        # Add the newly mined block to the chain

        pass

@app.post("/block")

async def create_block(type: str, content: str):

    tx_data = {'type': type, 'content': content, 'timestamp': time.time()}

    blockchain.add_new_transaction(tx_data)

    url = f"http://{ordererIP}:{ordererPort}/broadcast_transaction"

    response = requests.post(url, json=tx_data)

    return {'message': 'Success'}

async def check_chain():

    while True:

        url = f"http://{ordererIP}:{ordererPort}/chain"

        response = requests.get(url)

        chain = response.json()['chain']

        longest_chain = Blockchain.fromList(chain)

        if len(blockchain.chain) < len(longest_chain.chain) and blockchain.check_chain_validity(longest_chain.chain):

            # Recompute open_surveys

            longest_chain.open_surveys = {}

            for block in longest_chain.chain:

                if not compute_open_surveys(block, longest_chain.open_surveys, longest_chain.chain_code):

                    raise HTTPException(status_code=400, detail="Invalid Blockchain")

            blockchain = longest_chain

        await asyncio.sleep(10)

@app.get("/consensus")

async def consensus():

    try:

        await check_chain()

    except HTTPException as e:

        return e.detail

    return {'length': len(blockchain.chain), 'chain': blockchain.chain}

@app.get("/open_surveys")

async def open_surveys():

    surveys = [survey for survey in blockchain.open_surveys.values()]

    return {'length': len(blockchain.open_surveys), 'surveys': surveys}

@app.get("/mine")

async def mine():

    if not blockchain.unconfirmed_transactions:

        return {'message': 'None transactions 0x001'}

    last_block = blockchain.last_block

    new_block = Block(index=last_block.index + 1, transactions=[], timestamp=time.time(), previous_hash=last_block.hash)

    for transaction in blockchain.unconfirmed_transactions:

        # Validate transaction

        if not validate_transaction(transaction):

            continue

        new_block.transactions.append(transaction)

    blockchain.unconfirmed_transactions = []

    if len(new_block.transactions) == 0:

        return {'message': 'None transactions 0x002'}

    proof = blockchain.proof_of_work(new_block)

    blockchain.add_block(new_block, proof)

    # Announce it to the network

    url = f"http://{ordererIP}:{ordererPort}/broadcast_block"

    response = requests.post(url, json=new_block.__dict__)

    result = new_block.index

    if not result:

        return {'message': 'None transactions to mine'}

    return {'message': f'Block {result} has been mined'}

