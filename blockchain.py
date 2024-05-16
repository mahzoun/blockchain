import hashlib
import random
import string
import json
import binascii
import numpy as np
import pandas as pd
import pylab as pl
import logging
import datetime
import collections
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

class Client:
    def __init__(self):
        random = Crypto.Random.new().read
        self._private_key = RSA.generate(1024, random)
        self._public_key = self._private_key.publickey()
        self._signer = PKCS1_v1_5.new(self._private_key)

    @property
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')
    

class Transaction:
    def __init__(self, sender, recipient, value):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.time = datetime.datetime.now()

    def to_dict(self):
        if self.sender == "Genesis":
            identity = "Genesis"
        else:
            identity = self.sender.identity

        return collections.OrderedDict({
            'sender': identity,
            'recipient': self.recipient,
            'value': self.value,
            'time' : self.time})
    
    def sign_transaction(self):
        private_key = self.sender._private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')
    
class Block:
    def __init__(self):
        self.verified_transactions = []
        self.previous_block_hash = ""
        self.Nonce = ""
    def dump_blockchain(self):
        print("Number of blocks in the chain: " + str(len(self)))
    

    



def dump_blockchain(TPCoins):
    print ("Number of blocks in the chain: " + str(len(TPCoins)))
    for x in range (len(TPCoins)):
        block_temp = TPCoins[x]
        print ("block # " + str(x))
        for transaction in block_temp.verified_transactions:
            display_transaction (transaction)   

def display_transaction(transaction):
    dict = transaction.to_dict()
    print ("sender: " + dict['sender'])
    print ('___________________________')
    print ("recipient: " + dict['recipient'])
    print ('___________________________')
    print ("value: " + str(dict['value']))
    print ('___________________________')
    print ("time: " + str(dict['time']))
    print ('___________________________')

def sha256(message):
    return hashlib.sha256(message.encode('ascii')).hexdigest()

def mine(message, difficulty=1):
    assert difficulty >= 1
    prefix = '1' * difficulty
    for i in range(1000):
        digest = sha256(str(hash(message)) + str(i))
        if digest.startswith(prefix):
            print ("after " + str(i) + " iterations found nonce: "+ digest)
            return digest
        
last_block_hash = ""
transactions = []
Dinesh = Client()
Ramesh = Client()
Seema = Client()
Vijay = Client()

t0 = Transaction(
    "Genesis",
    Ramesh.identity,
    5.0
)

transactions.append(t0)

block0 = Block()
block0.previous_block_hash = None
Nonce = None
block0.verified_transactions.append(t0)
digest = hash(block0)
last_block_hash = digest
TPCoins = []
TPCoins.append(block0)
dump_blockchain(TPCoins)
last_transaction_index = 0
for i in range(1):
   temp_transaction = transactions[last_transaction_index]
   block0.verified_transactions.append(temp_transaction)
   last_transaction_index += 1

block0.previous_block_hash = last_block_hash
block0.Nonce = mine (block0, 2)
digest = hash (block0)
TPCoins.append (block0)
last_block_hash = digest
