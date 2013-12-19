import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from client_config import *
from xmlrpc import *
from threading import Thread
import os

def get_dir(path):
        p=path.split('/')
        size=len(p)
        return p[size-2],p[size-1]

class custom_handler(FileSystemEventHandler):

    def on_created(self, event):
        info=get_dir(event.src_path)
        notify_server("created", info[0],info[1])

    def on_deleted(self, event):
        info=get_dir(event.src_path)
        notify_server("deleted", info[0],info[1])

    def on_modified(self, event):
        r=os.stat(event.src_path)
        info=get_dir(event.src_path)
        notify_server("modified", info[0],info[1])

def sync(client, password):
    while True:
        time.sleep(time_to_sync)
        r = server.client_sync(client, password)
        print r
        if len(r) > 1:
            f=path + "/" + r[1] + "/" + r[2]
            if r[0] == "D":
                os.system("rm %s" % (f))
                pass

            if r[0] == "C":
                #sim_key,iv=r[3],r[4]
                #f_server(f, sim_key, iv)
                pass

            if r[0] == "M":
                #os.system("rm %s" % (f))
                #f_server(f, sim_key, iv)
                    pass





def run_observer():
    observer = Observer()
    observer.schedule(custom_handler(),path,recursive=True)
    observer.start()
    print "Client Daemon running... "
    th=Thread( target=sync, args = (client,password ) )
    th.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()