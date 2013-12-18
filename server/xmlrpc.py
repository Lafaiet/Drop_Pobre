"""SecureXMLRPCServer.py - simple XML RPC server supporting SSL.

Based on articles:
    1. http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/81549
    2. http://code.activestate.com/recipes/496786-simple-xml-rpc-server-over-https/
    3. http://stackoverflow.com/questions/5690733/xmlrpc-server-over-https-in-python-3
"""


from server_config import *
import SocketServer
import BaseHTTPServer
import SimpleHTTPServer
import SimpleXMLRPCServer
from security import *
from action import *
from threading import Thread

import socket, ssl
dependencies=[]

class SecureXMLRPCServer(BaseHTTPServer.HTTPServer,SimpleXMLRPCServer.SimpleXMLRPCDispatcher):
    def __init__(self, server_address, HandlerClass, logRequests=True):
        """Secure XML-RPC server.
        It it very similar to SimpleXMLRPCServer but it uses HTTPS for transporting XML data.
        """
        self.logRequests = logRequests

        try:
            SimpleXMLRPCServer.SimpleXMLRPCDispatcher.__init__(self)
        except TypeError:
            # An exception is raised in Python 2.5 as the prototype of the __init__
            # method has changed and now has 3 arguments (self, allow_none, encoding)
            #
            SimpleXMLRPCServer.SimpleXMLRPCDispatcher.__init__(self, False, None)

        SocketServer.BaseServer.__init__(self, server_address, HandlerClass)

        self.socket = ssl.wrap_socket(socket.socket(), server_side=True, certfile=CERTFILE,
                            keyfile=KEYFILE, ssl_version=ssl.PROTOCOL_SSLv23)

        self.server_bind()
        self.server_activate()

class SecureXMLRpcRequestHandler(SimpleXMLRPCServer.SimpleXMLRPCRequestHandler):
    """Secure XML-RPC request handler class.
    It it very similar to SimpleXMLRPCRequestHandler but it uses HTTPS for transporting XML data.
    """

    def setup(self):
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)

    def do_POST(self):
        """Handles the HTTPS POST request.

        It was copied out from SimpleXMLRPCServer.py and modified to shutdown the socket cleanly.
        """

        try:
            # get arguments
            data = self.rfile.read(int(self.headers["content-length"]))
            # In previous versions of SimpleXMLRPCServer, _dispatch
            # could be overridden in this class, instead of in
            # SimpleXMLRPCDispatcher. To maintain backwards compatibility,
            # check to see if a subclass implements _dispatch and dispatch
            # using that method if present.
            response = self.server._marshaled_dispatch(
                    data, getattr(self, '_dispatch', None)
                )
        except: # This should only happen if the module is buggy
            # internal error, report as HTTP server error
            self.send_response(500)
            self.end_headers()
        else:
            # got a valid XML RPC response
            self.send_response(200)
            self.send_header("Content-type", "text/xml")
            self.send_header("Content-length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

            # shut down the connection
            self.wfile.flush()

            #modified as of http://docs.python.org/library/ssl.html
            self.connection.shutdown(socket.SHUT_RDWR)
            self.connection.close()

def run_server(HandlerClass = SecureXMLRpcRequestHandler, ServerClass = SecureXMLRPCServer):
    """Test xml rpc over https server"""
    class xmlrpc_registers:
        def __init__(self):
            import string
            self.python_string = string

        '''testing methods...'''

        def add(self, x, y):
            return x + y

        def mult(self,x,y):
            return x*y

        def div(self,x,y):
            return x//y

        '''---------------------'''

        def client_sync(self,client,password):
            if client_auth(client, password):
                for d in dependencies:
                    for i in range(len(d.owners)):
                        c=d.owners[i]
                        if client==c:
                            if d.pend_type=="D":
                                print d.directory
                                print d.f
                                return "D",d.directory,d.f

                            if d.pend_type=="C":
                                sim_key=gen_key(16)
                                iv=gen_iv()
                                f=root_path+"/"+d.directory+"/"+d.f
                                f_client(f, sim_key, iv)
                                return "C",d.directory,d.f,sim_key,iv

                            if d.pend_type=="M":
                                sim_key=gen_key(16)
                                iv=gen_iv()
                                f=root_path+"/"+d.directory+"/"+d.f
                                f_client(f, sim_key, iv)
                                return "C",d.directory,d.f,sim_key,iv

                            d.owners.pop(i)


                return "N"



        def client_notify(self,client,directory,f,password,reason):
            #print "client= %s password= %s dir=%s f=%s"%(client,password,directory,f)

            if client_auth(client, password):
                if check_ownership(client, directory) :
                    sim_key=gen_key(16)
                    iv=gen_iv()
                    if reason== "created":
                        th=Thread( target=f_created, args = (client,directory,f,sim_key,iv ) )
                        th.start()
                        dependencies.append(add_pedency(client, directory, f, "C"))
                        return sim_key,iv


                    if reason== "modified":
                        th=Thread( target=f_modified, args = (client,directory,f,sim_key,iv ) )
                        th.start()
                        dependencies.append(add_pedency(client, directory, f, "M"))
                        return sim_key,iv


                    if reason== "deleted":
                        th=Thread( target=f_deleted, args = (client,directory,f ) )
                        th.start()
                        dependencies.append(add_pedency(client, directory, f, "D"))
                        return "Done!"

            return False

    server_address = (LISTEN_HOST, LISTEN_PORT)
    server = ServerClass(server_address, HandlerClass)
    server.register_instance(xmlrpc_registers())

    try:
        print "Serving HTTPS on %s, port %d" % (LISTEN_HOST, LISTEN_PORT)
        server.serve_forever()
    except KeyboardInterrupt:
        print 'Exiting'