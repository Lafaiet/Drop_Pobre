import xmlrpclib
from client_config import *
from file_transfer import *
import time
from security import *


server = xmlrpclib.Server('https://localhost:8443')

def notify_server(reason,dir,f):
    if reason is 'created':
        print "created!"
        f_h=get_f_h(path+"/"+dir+"/"+f)
        sim_key,iv= server.client_notify(client,dir,f,password,reason,f_h)
        time.sleep(1)
        f_client(path+"/"+dir+"/"+f,sim_key,iv)
        print "Sent!"


    if reason is 'deleted':
        server.client_notify(client,dir,f,password,reason,"dummy")


    if reason is 'modified':
        print "modified!"
        #server.client_notify(client,dir,f,password,'deleted')
        f_h=get_f_h(path+"/"+dir+"/"+f)
        sim_key,iv= server.client_notify(client,dir,f,password,reason,f_h)
        time.sleep(1)
        f_client(path+"/"+dir+"/"+f,sim_key,iv)
        print "Sent!"


#print server.add(1,1)
