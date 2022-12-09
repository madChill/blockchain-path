import datetime 
import hashlib
import json
from flask import Flask 


class Blockchain: 
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
    def create_block(self, proof, previous_hash):
        block = {   'index': len(self.chain) +1, 
                    'timestamp': str(datetime.datetime.now()),
                    'proof': proof,
                    'previous_hash': previous_hash
                }
        self.chain.append(block)
        return block
    def get_previous_block(self):
        return self.chain[-1]
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str( new_proof**2 - previous_proof**2 ).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof+=1
        return new_proof
    def hash(self, block):
        dump_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(dump_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while(block_index < len(chain)):
            current_block = chain[block_index]
            if current_block["previous_hash"] != self.hash(previous_block):
                return False
            previous_proof = previous_block["proof"]
            current_proof = current_block["proof"]
            hash_operation = hashlib.sha256(str( current_proof**2 - previous_proof**2 ).encode()).hexdigest()
            if hash_operation[:4] != '0000' : return False
            previous_block = current_block
            block_index+=1
        return True

app = Flask(__name__)

block_chain = Blockchain()

@app.route('/mine_block', method = ['GET'])
def mine_block():
    previous_block = block_chain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = block_chain.proof_of_work(previous_proof)
    previous_hash = block_chain.hash(previous_block)
    block = block_chain.create_block(proof, previous_hash)
    response = {
        'message': 'new block',
        'index': block['index'],
        'proof': block['proof'],
    }
    return response, 200


    
