import asyncio

import aiohttp

import time

async def close_survey(author, questionid, CONNECTED_NODE_ADDRESS):

    post_object = {

        'type' : 'close',

        'content' : {

            'questionid': questionid,

            'author': author + ':5000',

            'timestamp': time.time()

        }

    }

    # Submit a transaction

    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    async with aiohttp.ClientSession() as session:

        async with session.post(new_tx_address, json=post_object, headers={'Content-type': 'application/json'}) as response:

            print(response.status)

async def count_down_opening_time(opening_time, author, questionid, CONNECTED_NODE_ADDRESS):

    await asyncio.sleep(opening_time)

    await close_survey(author, questionid, CONNECTED_NODE_ADDRESS)

