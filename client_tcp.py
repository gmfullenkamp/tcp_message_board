import socket


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Wait for the user to %connect to their desired server
    print("Welcome to Chat GTC, the Grant and Trevor Client.\n"
          "Please use the '%connect <host_addr:port_#> <username>' to connect to your desired server.\n")
    while True:
        connect_command = input()
        if "%connect " in connect_command:
            host_addr, username = connect_command.split(" ")[1:3]
            print(f"Connecting to {host_addr} as user {username}...")
            host, port = host_addr.split(":")
            # Connect the client to the server
            s.connect((host, int(port)))
            # Allow the user to input any command/message whenever they want
            s.sendall(username.encode('utf-8'))
            break
        else:
            print("Try again.")  # TODO: Error Handling

    while True:
        # Allow the user to input any command/message whenever they want
        message = input("Type a message to send to the server: ")
        s.sendall(message.encode('utf-8'))
        # Make the user listen for the server response
        data = s.recv(1024)
        while not data:
            data = s.recv(1024)
        # Output the server response
        print('Server sent:', data.decode('utf-8'))
