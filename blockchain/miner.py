import hashlib
import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random
import json
# import random

def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    - Note:  We are adding the hash of the last proof to a number/nonce for the new proof
    """

    start = timer()

    print("Searching for next proof")
    proof = 0
    #  TODO: Your code here

    encoded_last_proof = str(last_proof).encode()
    last_proof_hash = hashlib.sha256(encoded_last_proof).hexdigest()

    while valid_proof(last_proof_hash, proof) is False:
        # print(proof)
        proof += 1
    return proof
    print("Proof found: " + str(proof) + " in " + str(timer() - start))

def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the proof?

    IE:  last_hash: ...AE9123456, new hash 123456888...
    """

    # TODO: Your code here!
    # guess = f"{last_hash}{proof}".encode()
    # guess_hash = hashlib.sha256(guess).hexdigest()
    new_proof = str(proof).encode()
    newer_proof = hashlib.sha256(new_proof).hexdigest()

    return newer_proof[:6] == last_hash[-6:]


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin-test-1.herokuapp.com/api"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
