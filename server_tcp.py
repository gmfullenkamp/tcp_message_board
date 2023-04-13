import socket
import select

HOST = 'localhost'
PORT = 8888

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f'Server listening on port {PORT}')
    sockets_list = [server_socket]
    clients = {}

    while True:
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

        for notified_socket in read_sockets:
            # TODO: Fix to allow multiple clients to send/recieve simultaneously
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                print(f'New client connected: {client_address[0]}:{client_address[1]}')
                sockets_list.append(client_socket)
                clients[client_socket] = client_address
            else:
                message = notified_socket.recv(1024)
                if not message:
                    print(f'Client disconnected: {clients[notified_socket][0]}:{clients[notified_socket][1]}')
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]
                    continue
                print(f'Received message from {clients[notified_socket][0]}:{clients[notified_socket][1]}: {message.decode()}')
                for client_socket in clients:
                    if client_socket != server_socket and client_socket != notified_socket:
                        client_socket.send(message)
