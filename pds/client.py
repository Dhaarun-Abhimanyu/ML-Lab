import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

result = proxy.add(5, 3)

print("Addition result: ", result)

result = proxy.subtract(10, 4)

print("Subtraction Result:", result)