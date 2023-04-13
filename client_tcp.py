import socket

HOST = 'localhost'  # the server's hostname or IP address
PORT = 8888        # the port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Connect the client to the server
    s.connect((HOST, PORT))
    while True:
        # Allow the user to input any command/message whenever they want
        message = input("Type a message to send to the server: ")
        s.sendall(message.encode('utf-8'))
        # Make the user listen for the server response
        data = s.recv(1024)
        while not data:
            data = s.recv(1024)
        # Ouput the server response
        print('Server sent:', data.decode('utf-8'))
