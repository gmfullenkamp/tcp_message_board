import socket
import select

HOST = 'localhost'  # the server's hostname or IP address
PORT = 8888         # the port used by the server

group_list = []

user_list = []


class Group:
    def __init__(self, name):
        self.name = name
        self.users = []
        self.recent = []


class User:
    def __init__(self, name, port_number):
        self.name = name
        self.port_number = port_number
        self.group = None


publicGroup = Group("public")
grantGroup = Group("grant")
trevorGroup = Group("trevor")
pythonGroup = Group("python")
cppGroup = Group("cpp")

group_list.append(publicGroup)
group_list.append(grantGroup)
group_list.append(trevorGroup)
group_list.append(pythonGroup)
group_list.append(cppGroup)

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

                # Boolean to mark user's first connection to create user object from entered username
                first = True

            else:
                # Receive data from the client
                message = notified_socket.recv(1024)

                # If the client has sent a message, print it and send it to all connected clients
                print(f'Received command from {clients[notified_socket][0]}:{clients[notified_socket][1]}: '
                      f'{message.decode()}')

                # If first time user has connected, get username and port number to update User object and userList
                if first:
                    user_list.append(User(message.decode(), clients[notified_socket][1]))
                    print(user_list[-1].name, user_list[-1].port_number)
                    first = False
                    notified_socket.sendall(message + b' is connected.')
                    
                elif b'%exit' == message.split(b' ')[0]:  # Exit command removes the client
                    print(f'Client exiting: {clients[notified_socket][0]}:{clients[notified_socket][1]}')
                    for user in user_list:
                        if user.port_number == clients[notified_socket][1]:
                            break
                    user_list.remove(user)
                    notified_socket.sendall(b'Disconnected from server.')
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]
                    continue
                
                elif b'%join' == message.split(b' ')[0]:
                    for user in user_list:
                        if user.port_number == clients[notified_socket][1]:
                            # Error handling implemented if user is already in public
                            if user.group != 'public':
                                group_list[0].users.append(user)
                                user.group = 'public'
                                break
                            else:
                                notified_socket.sendall(b'User is already in public')
                                continue
                            
                    notified_socket.sendall(b'User added to public')
                    continue
                
                elif b'%post' == message.split(b' ')[0]:  # TODO: Post command
                    notified_socket.sendall(b'%post command is not implemented.')
                    
                elif b'%users' == message.split(b' ')[0]:
                    send_string = 'List of connected users: \n'
                    for user in user_list:
                        send_string += user.name + '\n'
                    notified_socket.sendall(send_string.encode())
                    continue
                
                elif b'%leave' == message.split(b' ')[0]:
                    for user in user_list:
                        if user.port_number == clients[notified_socket][1]:
                            # Error handling implemented if user is not in public
                            if user.group == 'public':
                                group_list[0].users.remove(user)
                                user.group = None
                                break
                            else:
                                notified_socket.sendall(b'User is not in public')
                                continue
                    notified_socket.sendall(b'User removed from public')
                    continue
                
                elif b'%message' == message.split(b' ')[0]:  # TODO: Message command
                    notified_socket.sendall(b'%message command is not implemented.')
                    
                elif b'%groups' == message.split(b' ')[0]:
                    send_string = 'List of groups: \n'
                    for group in group_list:
                        send_string += group.name + '\n'
                    notified_socket.sendall(send_string.encode())
                    continue
                
                elif b'%groupjoin' == message.split(b' ')[0]:
                    for user in user_list:
                        if user.port_number == clients[notified_socket][1]:
                            for group in group_list:
                                if message.split(b' ')[1].decode() == group.name:
                                    # Error handling implemented for if user is already in requested group
                                    if user.group != group.name:
                                        group.users.append(user)
                                        user.group = group.name
                                        break
                                    else:
                                        print(group.users)
                                        notified_socket.sendall(b'User is already in ' + group.name.encode())
                                        continue
                                    
                    notified_socket.sendall(b'User added to ' + group.name.encode())
                    continue
                
                elif b'%grouppost' == message.split(b' ')[0]:  # TODO: Grouppost command
                    notified_socket.sendall(b'%grouppost command is not implemented.')
                    
                elif b'%groupusers' == message.split(b' ')[0]:
                    send_string = 'List of users in ' + message.split(b' ')[1].decode() + ':\n'
                    for group in group_list:
                        if message.split(b' ')[1].decode() == group.name:
                            for user in group.users:
                                send_string += user.name + '\n'
                    notified_socket.sendall(send_string.encode())
                    continue
                    
                elif b'%groupleave' == message.split(b' ')[0]:
                    for user in user_list:
                        if user.port_number == clients[notified_socket][1]:
                            for group in group_list:
                                if message.split(b' ')[1].decode() == group.name:
                                    # Error handling implemented for if user is not in requested group
                                    if user.group == group.name:
                                        group.users.remove(user)
                                        user.group = None
                                        break
                                    else:
                                        notified_socket.sendall(b'User is not in ' + group.name.encode())
                                        continue
                                    
                    notified_socket.sendall(b'User removed from ' + group.name.encode())
                    continue
                
                elif b'%groupmessage' == message.split(b' ')[0]:  # TODO: Groupmessage command
                    notified_socket.sendall(b'%groupmessage command is not implemented.')
                    
                else:  # TODO: Make else error handling, possible print all commands and functions?
                    notified_socket.sendall(message)
