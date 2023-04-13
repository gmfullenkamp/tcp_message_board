import socket

HOST = 'localhost'  # the server's hostname or IP address
PORT = 8888        # the port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        message = input("Type a message to send to the server: ")
        s.sendall(message.encode('utf-8'))
        data = s.recv(1024)
        while not data:
            data = s.recv(1024)
        print('Server sent:', data.decode('utf-8'))
