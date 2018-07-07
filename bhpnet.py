import sys
import socket
import getopt
import threading
import subprocess

# define global variables
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


def usage():
    """Prints program usage information"""
    print("BHP Net tool")
    print("")
    print("Usage: bhpnet.py -t target_host -p port")
    print("-l --listen                      listen on [host]:[port] for incoming connection")
    print("-e --execute=file_to_run         execute the given file name upon receiving a connection")
    print("-c --command                     initialize a command shell")
    print("-u --upload=destination          upon receiving a connection upload a file and write to [destination]")
    print("")
    # print("")
    print("Examples: ")
    print("bhnet.py -t 192.168.0.1 -p 5555 -l -c")
    print("bhnet.py -t 192.168.0.1 -p 5555 -u=c:\\\\target.exe")
    print("bhnet.py -t 192.168.0.1 -p 5555 -l -e\"cat /etc/passwd\"")
    print("echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135")
    sys.exit(0)


def main():
    """Program main"""
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not sys.argv[1:]:  # if no arguments were passed, call usage()
        usage()

    # read the command line options
    # TODO
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help", "listen", "execute", "target", "port",
                                                                 "command", "upload"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        elif o in ("-c", "--command"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        else:
            assert False, "Unhandled Option"

    # are we going to listen or just send data from stdin?
    if not listen and len(target) and port > 0:
        # read in the buffer from standard in. This will block so send CTRL + D if not sending data from stdin.
        buffer = sys.stdin.read()

        # send data off
        client_sender(buffer)

    # we are going to listen and potentially
    # upload things, execute commands, and drop a shell back
    # depending on our command line options above
    if listen:
        server_loop()


def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # connect to our target host
        client.connect((target, port))
        if len(buffer):
            client.send(buffer)



main()
