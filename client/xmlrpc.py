import xmlrpclib
from client_config import *

server = xmlrpclib.Server('https://localhost:8443')

def notify_server(reason,file):
    if reason is 'created':
        print server.client_notify(client,file,password,reason)
        print file

    elif reason is 'deleted':
        print server.client_notify(client,file,password,reason)
        print file

    else:
        print server.client_notify(client,file,password,reason)
        print file