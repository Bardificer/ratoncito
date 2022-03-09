import subprocess
import socket
import os


def run(cmd):
    completed = subprocess.run(["pwsh", "-Command", cmd], capture_output=True)
    return completed

# test powershell capabilities
if __name__ == '__main__':
    hello_command = "Write-Host 'Hello Wolrd!'"
    hello_info = run(hello_command)
    if hello_info.returncode != 0:
        print("An error occured: %s", hello_info.stderr)
    else:
        print("Hello command executed successfully!")
    
    print("-------------------------")

SEPARATOR = '<sep>'

def callback(output):
    message = f"{output}{SEPARATOR}{os.getcwd()}"

while True:
        # get the command from prompt
    command = input(f"PS | {os.getcwd()} $> ")
    splited_command = command.split()
    print(command + " - " + str(splited_command))
    # send the command
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
        output = run(command)
    # print output
    try:
        print(output.stdout.decode())
    except:
        print(output)
