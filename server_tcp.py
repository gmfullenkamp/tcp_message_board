import socket

HOST = 'localhost'  # the server's hostname or IP address
PORT = 8888        # the port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on port {PORT}")
    while True:
        conn, addr = s.accept()
        print(f"Client {addr[0]}:{addr[1]} has connected")
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)
