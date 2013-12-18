#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import sys
from security import *
import os

# import SimpleHTTPServer
# import SocketServer
# from server_config import *
#
# def run_fserver(directory):
#     print "HTTP server runnig at port %s"%(fs_PORT)
#     os.system("cd %s"%directory)
#     os.system("python -m SimpleHTTPServer %s"%(fs_PORT))
#
# def kill_fserver():
#     os.system("p=$(ps aux | grep Simple | awk 'NR==1 {print $2}')")
#     os.system("kill $p")


def f_server(f,sim_key,iv):

    s = socket.socket()
    s.bind(("localhost",9999))
    s.listen(10)

    sc, address = s.accept()
    print f
    r_f = open("temp",'wb') #open in binary
    l = 1
    while(l):
        l = sc.recv(1024)
        while (l):
            r_f.write(l)
            l = sc.recv(1024)
    r_f.close()


    sc.close()

    s.close()
    dec_file("temp",f, sim_key, iv)
    os.system("rm %s"%("temp"))



def f_client(f,sim_key,iv):
    enc_file("temp_",f, sim_key, iv)
    s = socket.socket()
    s.connect(("localhost",9999))
    f=open ("temp_", "rb")
    l = f.read(1024)
    while (l):
        s.send(l)
        l = f.read(1024)
    s.close()
    os.system("rm %s"%("temp_"))

#f_server("f2", "xxxxxxxxxxxxxxxx", "xxxxxxxxxxxxxxxx")
