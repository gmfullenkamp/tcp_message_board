import socket
import select

HOST = 'localhost'  # the server's hostname or IP address
PORT = 8888        # the port used by the server


groupList = []

userList = []

class Group:
    def __init__(self, name):
        self.name = name
        self.users = []
        self.recent = []

class User:
    def __init__(self, username, portNumber):
        self.username = username
        self.portNumber = portNumber
        self.group = None

publicGroup = Group("public")

# Create the server socket and bind it to the specified host and port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f'Server listening on port {PORT}')

    # Create a list of sockets to listen on and a dictionary to keep track of clients
    sockets_list = [server_socket]
    clients = {}

    # Wait for incoming connections and handle data from clients
    while True:
        # Use select.select() to wait for I/O events on the sockets
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list, 0)

        # Handle sockets that are ready to be read
        for notified_socket in read_sockets:
            # If the socket is the server socket, accept the connection from the client
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                print(f'New client connected: {client_address[0]}:{client_address[1]}')

                # Add the client socket to the list of sockets to listen on and the clients dictionary
                sockets_list.append(client_socket)
                clients[client_socket] = client_address
            else:
                # Receive data from the client
                message = notified_socket.recv(1024)

                # If the client has disconnected, remove the socket from the list and the dictionary
                if not message:
                    print(f'Client disconnected: {clients[notified_socket][0]}:{clients[notified_socket][1]}')
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]
                    continue

                # If the client has sent a message, print it and send it to all connected clients
                print(f'Received message from {clients[notified_socket][0]}:{clients[notified_socket][1]}: {message.decode()}')
                for client_socket in clients:
                    if client_socket != server_socket and client_socket != notified_socket:
                        
                        client_socket.send(message)

                        

        # Handle sockets that have exceptions (e.g. a client has disconnected unexpectedly)
        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            del clients[notified_socket]
