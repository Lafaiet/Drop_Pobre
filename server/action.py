from file_transfer import *
from server_config import *
import os
from pendency import *
from database import *


def add_pedency(client,directory,f,pend_type):
    owners=get_clients_dir(directory)
    p=pendency(directory,file,pend_type,owners)
    for i in range(len(p.owners)):
        if client==p.owners[i]:
            p.owners.pop(i)
            break
    return p


def f_created(client,directory,f,sim_key,iv):
    f_server(root_path+"/"+directory+"/"+f, sim_key, iv)
    print "Transfered!"

def f_modified(client,directory,f,sim_key,iv):
    os.system("rm %s"%(root_path+"/"+directory+"/"+f))
    f_server(root_path+"/"+directory+"/"+f, sim_key, iv)
    print "Modified!"

def f_deleted(client,directory,f):
    os.system("rm %s"%(root_path+"/"+directory+"/"+f))
    print "Deleted!"


#add_pedency("fulano", "ful_dir", "whatever", "D")
#print pendencies[0].owners
