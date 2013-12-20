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


"""
Class for checking the strength of a password.
Copyright (C) 2011 Henry Longmore.  This version
of this file may be copied for personal, educational,
or commercial purposes.  Use at your own risk.
"""

import os
from os import path
import math

# Nota Bene: the configuration module is non-standard. You will
# need to format and read your dictionary file yourself.
#from djangoapps import configuration

password_file = "/home/lafaiet/Drop_Pobre/server/data/dictionary" #Check out here---> http://wiki.skullsecurity.org/Passwords



# Based on Password Strength Meter posted at Snipplr
# http://snipplr.com/view/8755/password-strength-meter/

class PasswordStrengthChecker(object):

    def get_dict_words(self,password_file):
        words=[]
        f=open(password_file)
        w=f.readline()

        while len(w)>0:
            words.append(w.rstrip())
            w=f.readline()
        f.close()
        return words


    def __init__(self, strength='medium'):
        self.punctuation = list("!@#$%^&* ()_+-='\";:[{]}\|.>,</?`~")
        self.similarity_map = {
            '3': 'e', 'x': 'k', '5': 's', '$': 's', '6': 'g', '7': 't',
            '8': 'b', '|': 'l', '9': 'g', '+': 't', '@': 'a', '0': 'o',
            '1': 'l', '2': 'z', '!': 'i', '1': 'i'}
        #password_dictionary = configuration.Configuration(configpath=pwd_dict)
        self.word_list = dict()
        words=self.get_dict_words(password_file)

        for w in words:
            try:
                self.word_list[len(w)]
                self.word_list[len(w)].append(w)
            except KeyError:
                s=[]
                s.append(w)
                self.word_list[len(w)]=s

        #print self.word_list

#            self.word_list[i] = password_dictionary.get_option('%s' % i, [])

        self.strengths = ['medium', 'strong', 'best']
        self.thresholds = {'medium': 0.8, 'strong': 0.6, 'best': 0.6}
        self.min_length = {'medium': 8, 'strong': 8, 'best': 14}
        self.min_charsets = {'medium': 2, 'strong': 3, 'best': 3}
        self.similarity = {'medium': False, 'strong': True, 'best': True}

        if strength not in self.strengths:
            strength = self.strengths[0]
        self.strength = strength

    def is_charset_type(self, c, c_class):
        if c_class == 'capital':
            return c.isalpha() and c == c.upper()
        if c_class == 'lower':
            return c.isalpha() and c == c.lower()
        if c_class == 'digit':
            return c.isdigit()
        if c_class == 'punctuation':
            return c in self.punctuation
        return False

    def canonicalize_word(self, word, letters_only=False):
        canonicalized = ''
        for c in list(word.lower()):
            if letters_only and not self.is_charset_type(c, 'lower'):
                canonicalized += c
            else:
                canonicalized += self.similarity_map.get(c, c)
        return canonicalized

    def charset_span(self, word):
        checks = {'capital': 0, 'lower': 0, 'digit': 0, 'punctuation': 0}
        for c in list(word):
            for key in checks:
                if not checks[key] and self.is_charset_type(c, key):
                    checks[key] = 1
                    break
        return sum(checks.values())

    def in_dictionary(self, word):
        similarity_check = self.similarity[self.strength]
        canonicalized = self.canonicalize_word(word, letters_only=similarity_check)
        word_length = len(canonicalized)

        try:
            if canonicalized in self.word_list[word_length]:
                return True
        except KeyError:
            pass

        if similarity_check:
            minimum_meaningful_match = int(math.floor((self.thresholds[self.strength]) * word_length))
            for length in xrange(minimum_meaningful_match, word_length):
                for start in xrange(0, word_length - minimum_meaningful_match):
                    subword = canonicalized[start:start + length]
                    try:
                        if subword in self.word_list[len(subword)]:
                            return True
                    except KeyError:
                        pass
        return False

    def strong_enough(self, password):
        if not password:
            return False
        if len(password) < self.min_length[self.strength]:
            return False
        if self.charset_span(password) < self.min_charsets[self.strength]:
            return False
        if self.in_dictionary(password):
            return False
        return True

#global password_checker
#password_checker = PasswordStrengthChecker(strength='strong')
#print password_checker.strong_enough("password123")
#print password_checker.in_dictionary("camaro")

def insert_user(name,password):
    user=get_client(name)
    if user is None:
        global password_checker
        password_checker = PasswordStrengthChecker(strength='strong')
        if password_checker.strong_enough(password):
            insert_client(name, pass_hash(password), gen_key(32))
            return "inserted"
        return "weak"
    return "exist"


# iv = gen_iv()
# key=gen_key(16)
# cipher = AES.new(key, AES.MODE_CTR)
# var=cipher.encrypt("xxxxxxxxxxxxxxxx")
# print var
# #cipher = AES.new(key, AES.MODE_OPENPGP,iv)
# var=cipher.decrypt(var)
# print var

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


