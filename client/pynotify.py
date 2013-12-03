import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from client_config import *
from xmlrpc import *


class custom_handler(FileSystemEventHandler):


    def on_created(self, event):
        notify_server("created", event.src_path)

    def on_deleted(self, event):
        notify_server("deleted", event.src_path)

    def on_modified(self, event):
        notify_server("modified",event.src_path)



def run_observer():
    observer = Observer()
    observer.schedule(custom_handler(),path,recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
