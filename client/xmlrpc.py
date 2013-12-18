import xmlrpclib
from client_config import *
from file_transfer import *
import time


server = xmlrpclib.Server('https://localhost:8443')

def notify_server(reason,dir,f):
    if reason is 'created':
        print "created!"
        sim_key,iv= server.client_notify(client,dir,f,password,reason)
        time.sleep(1)
        f_client(path+"/"+dir+"/"+f,sim_key,iv)
        print "Sent!"


    if reason is 'deleted':
        server.client_notify(client,dir,f,password,reason)


    if reason is 'modified':
        print "modified!"
        #server.client_notify(client,dir,f,password,'deleted')
        sim_key,iv= server.client_notify(client,dir,f,password,reason)
        time.sleep(1)
        f_client(path+"/"+dir+"/"+f,sim_key,iv)
        print "Sent!"


#print server.add(1,1)
