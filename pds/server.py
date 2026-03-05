
from xmlrpc.server import SimpleXMLRPCServer
class Calculator:

    def add(self, a, b):
        return a + b


    def subtract(self, a, b):
        return a - b


server = SimpleXMLRPCServer(("localhost", 8000))
server.register_instance(Calculator())

print("RPC Server running on port 8000...")
server.serve_forever()