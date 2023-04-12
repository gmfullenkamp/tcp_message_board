import socket

HOST = 'localhost'  # the server's hostname or IP address
PORT = 8888        # the port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, server')
    data = s.recv(1024)

print('Received', repr(data))
