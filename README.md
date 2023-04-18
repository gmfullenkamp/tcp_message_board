# tcp_message_board
## Running the Server
1. To run the server, be sure to have Python 3.10 installed on your local machine.
2. Next, open a command terminal.
3. Navigate to the directory where the server_tcp.py file is located.
4. Run the command 'python server_tcp.py'.

Notes:
- The server is ran on the host address localhost and the port 8888 (localhost:8888).
- You may need to turn off your firewall in order for the client to correctly communicate with the server.
## Running a client
1. To run the client, be sure to have Python 3.10 installed on your local machine.
2. Next, open a command terminal.
3. Navigate to the directory where the server_tcp.py file is located.
4. Run the command 'python client_tcp.py'.

### ClientCommands
- **%connect**: This connects the user to the server through a given hostport and username. (example: "%connect localhost:8888 Grant")
- **%exit**: This disconnects the user from the server they have connected to. (example: "%exit")
- **%join**: Once connected to the server, this allows the user to join the public group. (example: "%join")
- **%users**: Once connected to the server, this allows the user to see all the other users on the server. (example: "%users")
- **%post**: Once connected to the server, this allows the user to post a subject and message to the public group. (example: "%post subject 'this is the message'")
- **%message**: Once connected to the server, this allows the user to retrieve a post from the public group based on the message id. (example: "%message 0")
- **%leave**: Once connected to the server and joined in the public group, this allows the user to leave the public group. (example: "%leave")
- **%groups**: Once connected to the server, this allows the user to see all the other groups available to join. (example: "%groups")
- **%groupjoin**: Once connected to the server, this allows the user to join any available group. (example: "%groupjoin python")
- **%groupusers**: Once connected to the server, this allows the user to see all the other users on the specified group. (example: "%groupusers python")
- **%grouppost**: Once connected to the server, this allows the user to post a subject and message to the specified group. (example: "%grouppost python python_subject 'this is the python message'")
- **%groupmessage**: Once connected to the server, this allows the user to retrieve a post from the specified group based on the message id. (example: "%groupmessage python 0")
- **%groupleave**: Once connected to the server and joined in a group, this allows the user to leave the group specified. (example: "%groupleave python")

Notes:
- The server has these commands implemented correctly with the given parameters; although, not a lot of error handling has been done for incorrect commands or their parameters. (spell check and parameter check before sending)
## Not Implemented
1. The %post commands don't update all the clients who are connected to the group that a user posted on, but all the posts are received correctly and saved correctly within the group for %message retrieval.
2. The %join commands don't update all the clients who are connected to the group with 'user _ has joined the group'.
3. The %leave commands don't update all the clients who are connected to the group with 'user _ has left the group'.
