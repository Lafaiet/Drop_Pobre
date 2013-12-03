from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto import Random
from database import *


def pass_hash(key):
    hash = SHA256.new()
    hash.update(key)
    return hash.hexdigest()


def check_pass(password,digest):
    if pass_hash(password)==digest:
        return True
    return False


def client_auth(client,password):
    c=get_client(client)
    return check_pass(password, c[1])


def encript_word(key,word,iv):
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return cipher.encrypt(word)

def gen_iv():
    return Random.new().read(AES.block_size)