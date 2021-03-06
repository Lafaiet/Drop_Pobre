from file_transfer import *
from server_config import *
import os
from pendency import *
from database import *
from security import *
import time


def f_created_s(f,sim_key,iv):
    print "Waiting for client to connect..."
    time.sleep(2)
    f_client(f, sim_key, iv)


def add_pedency(client,directory,f,pend_type):
    owners=get_clients_dir(directory)
    p=pendency(directory,f,pend_type,owners)
    for i in range(len(p.owners)):
        if client==p.owners[i]:
            p.owners.pop(i)
            break
    return p


def f_created(client,directory,f,sim_key,iv,f_h):
    f=root_path+"/"+directory+"/"+f
    f_server(f, sim_key, iv)
    if test_integrity(f, f_h):
        print "Successfully Transfered!"
    else:
        print "An error has occurred!"

def f_modified(client,directory,f,sim_key,iv,f_h):
    os.system("rm %s"%(root_path+"/"+directory+"/"+f))
    f=root_path+"/"+directory+"/"+f
    f_server(f, sim_key, iv)
    if test_integrity(f, f_h):
        print "Successfully Transfered!"
    else:
        print "An error has occurred!"

def f_deleted(client,directory,f):
    os.system("rm %s"%(root_path+"/"+directory+"/"+f))
    print "Deleted!"


#add_pedency("fulano", "ful_dir", "whatever", "D")
#print pendencies[0].owners
