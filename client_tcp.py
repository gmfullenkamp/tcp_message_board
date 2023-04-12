import socket

HOST = 'localhost'  # the server's hostname or IP address
PORT = 8888        # the port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    message = input("Type a message to send to the server: ")
    s.sendall(message.encode('utf-8'))
