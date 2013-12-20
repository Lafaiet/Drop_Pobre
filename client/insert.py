from xmlrpc import *
from security import *


if __name__ == "__main__":
    server = xmlrpclib.Server('https://localhost:8443')
    name="lafa"
    password="password"
    r=server.insert_sec(name,gen_key(16))
    if r=="exist":
        print "User name already picked!!!"

    if r=="weak":
        print "Weak password!"

        pass
    if r=="inserted":
        print "Inserted!"

