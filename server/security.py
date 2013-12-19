from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto import Random
from Crypto.Random import random
from database import *
from utils import *


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
    return check_pass(password+c[2], c[1])


def check_ownership(client,directory):
    dirs= get_dirs_client(client)
    for i in dirs:
        if directory == i[0]:
            return True
    return False


def encript_word(key,word,iv):
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return cipher.encrypt(word)

def decript_word(key,word,iv):
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return cipher.decrypt(word)


def gen_iv():
    #return Random.new().read(AES.block_size)
    return gen_key(AES.block_size)

def gen_key(size):
    k=""
    for i in range(size):
        k=k+str(chr(random.randint(39,126)))
        #k=k+str(chr(random.randint(0,127)))
    return k


def enc_file(e_f,d_f,sim_key,iv):
    e_f=open(e_f,"w")
    d_f=open(d_f,"r")
    s=d_f.read(16)

    while len(s)>0:
        enc_s=decript_word(sim_key, s, iv)
        e_f.write(enc_s)
        s=d_f.read(16)
    e_f.close()
    d_f.close()
    return "done"

def dec_file(e_f,d_f,sim_key,iv):
    e_f=open(e_f,"r")
    d_f=open(d_f,"w")
    s=e_f.read(16)

    while len(s)>0:
        dec_s=encript_word(sim_key, s, iv)
        d_f.write(dec_s)
        s=e_f.read(16)
    d_f.close()
    e_f.close()
    return "done"

def get_f_h(f):
    f=open(f,"r")
    st=f.read()
    return MD5.new(st).hexdigest()

def test_integrity(f,f_h):
    return get_f_h(f)==f_h

# sim_key=gen_key(16)
# iv=gen_iv()
# #
# enc_file("enc", "file",sim_key, iv)
# dec_file("enc", "file2",sim_key, iv)
# print "Done!"

# init_database()
# salt=gen_key(32)
# insert_client('fulano', pass_hash("key"+salt),salt)
# #
# salt=gen_key(32)
# insert_client('ciclano', pass_hash("key"+salt),salt)
# #
# salt=gen_key(32)
# insert_client('beltrano', pass_hash("key"+salt),salt)
# #
# insert_dir("fulano", "ful_dir")
# insert_dir("ciclano", "cil_dir")
# insert_dir("ciclano", "ful_dir")
# insert_dir("beltrano", "bel_dir")
# #
# print "done!"
#print client_auth("ciclano", "key")


# w="ola, tudo bem?"
# k=gen_key(16)
# # print k
# iv=gen_iv()
# cp=encript_word(k, w,iv)
# dc=decript_word(k, cp, iv)
# print dc

#print check_ownership("teste1", "tese1_dir")