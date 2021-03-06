from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto import Random
from Crypto.Random import random



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
        enc_s=encript_word(sim_key, s, iv)
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
        dec_s=decript_word(sim_key, s, iv)
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
