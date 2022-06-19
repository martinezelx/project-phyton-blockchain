import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse
from flask_ngrok import run_with_ngrok


# 1 - build the blockchain main class.
class Blockchain:

    def __init__(self):
        """ Constructor of class. """

        self.chain = []  # list of chains
        self.txs = []  # list of transactions
        self.create_block(proof=1, previous_hash='0')  # call create_block function for create a genesis block
        self.nodes = set()  # collections of nodes

    def create_block(self, proof, previous_hash):
        """ Function to create a block when the mine is ready.

              Arguments:
                - proof: actual block nonce.
                - previous_hash: previous block hash.

              Returns:
                - block: new created block.
          """

        # data structure for block
        block = {'index': len(self.chain) + 1,  # chain length +1
                 'timestamp': str(datetime.datetime.now()),  # timestamp cast to string
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.txs}

        self.txs = []  # empty list of tx when a block is mined

        self.chain.append(block)  # add block in list of chains

        return block  # returns data object block

    def get_previous_block(self):
        """ Function to return last value from the chain list.

          Returns:
            - return last block of blockchain.
        """

        return self.chain[-1]

    def get_proof_of_work(self, previous_proof):
        """ Function to resolve the cripto puzzle and returns a new Proof of Work (PoW).

          Arguments:
            - previous_proof: previous block nonce.

          Returns:
            - new_proof: return new nonce resolve with PoW.
        """

        new_proof = 1
        check_proof = False

        while check_proof is False:

            # no symmetric operation (x**2-y**2) for calculate a hexadecimal hash
            hash_operation = hashlib.sha256(
                str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()

            # check 4 zeros in firsts positions
            if hash_operation[:4] == '0000':
                check_proof = True  # break loop
            else:
                new_proof += 1  # increase variable

        return new_proof

    def calculate_block_hash(self, block):
        """ Function for calculate hash from a block.

            Arguments:
                - block: identify block of blockchain.

            Returns:
                - hash_block: returns hash of the block.
        """

        # json cast and sorting of block
        encoded_block = json.dumps(block, sort_keys=True).encode()

        # return the cast object block encoded in sha256
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        """ Function to validate chain.

            Arguments:
                - chain: blockchain that contents all data for txs.

            Returns:
                - True/False: boolean (True = valid, False = invalid).
        """

        previous_block = chain[0]
        block_index = 1

        # loop the list of chains
        while block_index < len(chain):

            # current block of iteration
            current_block = chain[block_index]

            # check hash of current block is not the same of previous block hash
            if current_block['previous_hash'] != self.calculate_block_hash(previous_block):
                return False  # break loop and chain is not valid

            previous_proof = previous_block['proof']
            actual_proof = current_block['proof']

            hash_operation = hashlib.sha256(str(actual_proof ** 2 - previous_proof ** 2).encode()).hexdigest()

            if hash_operation[:4] != '0000':
                return False

            # overwrite block
            previous_block = current_block
            # increase count variables
            block_index += 1

        return True

    def add_tx(self, sender, receiver, amount):
        """ Function to create and add transaction.
            Arguments:
                - sender: person who makes the tx.
                - receiver: person who receives the tx.
                - amount: amount of cryptocurrencies sent.

            Returns:
                - return of the superior index to the last block.
        """

        # data structure for transaction
        tx = {'sender': sender,
              'receiver': receiver,
              'amount': amount}

        # add to txs list
        self.txs.append(tx)

        # get previous index to increase
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    def add_node(self, address):
        """ Function to add a node in collection nodes.

            Arguments:
            - address: address of new node.
        """

        # parsed url - netloc='127.0.0.1:5000'
        parsed_url = urlparse(address)
        # add to collection of nodes
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        """ Validate actual chain and replace for the longest, if is valid. """

        # collections of nodes are the network
        network = self.nodes

        # longest chain
        longest_chain = None

        # initialize maximum length
        max_length = len(self.chain)

        # iterate nodes for localize the longest chain
        for node in network:

            # call to /get_chain
            response = requests.get(f'http://{node}/get_chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # validate actual chain and length
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain

        if longest_chain:  # is not none

            # replace for the longest chain
            self.chain = longest_chain

            return True  # chain is update

        return False  # chain is not update


# 2 - interact with blockchain, mine, obtain info and checks health.
# create web app for interact
app = Flask(__name__)
run_with_ngrok(app)

# create direction of node 5000 (local)
node_address = str(uuid4()).replace('-', '')

# create instance of objet Blockchain.class
blockchain = Blockchain()


@app.route('/mine_block', methods=['GET'])
def mine_block():
    """ Function to mine a new block. """

    # get all data
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.get_proof_of_work(previous_proof)
    previous_hash = blockchain.calculate_block_hash(previous_block)

    # before create a block, the recompense must have to send to miner
    blockchain.add_tx(sender=node_address, receiver="Martinez", amount=10)

    # generate the block object
    block = blockchain.create_block(proof, previous_hash)

    # object for show in response
    response = {'message': 'Congrats for the new block bro!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}

    return jsonify(response), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
    """ Function to obtain all blocks of blockchain. """

    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}

    return jsonify(response), 200


@app.route('/is_valid', methods=['GET'])
def is_valid():
    """ Function to check the validation of chain. """

    # call to function to check the validation of chain
    valid_chain = blockchain.is_chain_valid(blockchain.chain)

    if valid_chain:
        response = {'message': 'OK 200 - blockchain is valid :)'}
        return jsonify(response), 200
    else:
        response = {'message': 'ERROR 500 - blockchain not valid :('}
        return jsonify(response), 500


@app.route('/add_tx', methods=['POST'])
def add_tx():
    """ Function to add transaction in blockchain. """

    # variable to get the request
    json_request = request.get_json()

    tx_keys = ['sender', 'receiver', 'amount']

    if not all(key in json_request for key in tx_keys):
        return 'Error 400 - sender, receiver or amount are empty', 400  # bad request

    index = blockchain.add_tx(json_request['sender'], json_request['receiver'], json_request['amount'])

    response = {'message': f'Transaction add to block with index:{index}'}

    return jsonify(response), 201  # created


# 3 - decentralise the blockchain.
@app.route('/connect_node', methods=['POST'])
def connect_node():
    """ Connect new nodes. """

    # variable to get the request
    json_request = request.get_json()

    nodes = json_request.get('nodes')

    if nodes is None:
        return 'Nodes are empty', 400  # bad request

    for node in nodes:
        blockchain.add_node(node)

    response = {'message': f'Nodes add to blockchain: {nodes}',
                'total_nodes': list(blockchain.nodes)}

    return jsonify(response), 201  # created


@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    """ Replace the chain for the longest if its necessary. """

    is_chain_replace = blockchain.replace_chain()

    if is_chain_replace:
        response = {'message': 'Nodes has a different chains, all has replaced with a new valid chain',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'All nodes are synchronized, not replaced',
                    'actual_chain': blockchain.chain}

    return jsonify(response), 200  # successful


# start the app in ngrok server
app.run()

# start the app in local
# app.run(host='0.0.0.0', port=5000)  # 0.0.0.0 is open host
