import datetime
import hashlib
import json
from urllib.parse import urlparse
from pip._vendor import requests


class Blockchain:

    def __init__(self):
        self.chain = []
        self.data = []
        self.nodes = set()
        self.create_block(nonce = 1, previous_hash = '0')

    def create_block(self, nonce, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'nonce': nonce,
                 'previous_hash': previous_hash,
                 'data': self.data,
                 }
        self.data = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_nonce):
        new_nonce = 1
        check_nonce = False
        while check_nonce is False:
            hash_operation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_nonce = True
            else:
                new_nonce += 1
        return new_nonce

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_nonce = previous_block['nonce']
            nonce = block['nonce']
            hash_operation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

    def add_data(self, patient, practicioner, meta_data, patient_data, time): #New
        self.data.append({
            'patient': patient,
            'practicioner': practicioner,
            'meta_data': meta_data,
            'patient_data': patient_data,
            'time': str(datetime.datetime.now())
            })
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    def add_node(self, address): #New
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self): #New
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False

    def get_patient_data(self, patient):
        patient_data = []
        for block in self.chain:
            for data in block['data']:
                if data['patient'] == patient:
                    patient_data.append(data['patient_data'])
        return patient_data

    def get_patient_treated_by_doctor(self, patient, doctor):
        patient_data = []
        for block in self.chain:
            for data in block['data']:
                if data['patient'] == patient and data['doctor'] == doctor:
                    patient_data.append(data['patient_data'])
        return patient_data





