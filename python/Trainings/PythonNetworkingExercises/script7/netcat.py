import sys
import socket
import getopt
import threading
import subprocess


def client_sender(buffer, target, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((target, port))
        if len(buffer):
            client.send(buffer.encode('ascii'))

        while True:
            recv_len = 1
            response = ""

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data.decode("utf-8")

                if recv_len < 4096:
                    break

            print(response, end='')
            buffer = input("")
            buffer += "\n"
            client.send(buffer.encode('ascii'))
    except Exception as e:
        print(repr(e))
        print("[*] Exception! Exiting.")
        client.close()


def server_loop(target, port, execute, command, upload_dest):
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        client_thread = threading.Thread(target=client_handler,
                                         args=(client_socket, execute, command, upload_dest))
        client_thread.start()


def client_handler(client_socket, execute, command, upload_dest):
    if len(upload_dest):
        file_buffer = ""
        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data
        try:
            file_descriptor = open(upload_dest, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()
        except:
            client_socket.send(f"Failed to save file to {upload_dest} \r\n")

    if len(execute):
        output = run_command(execute)
        client_socket.send(output)

    if command:
        while True:
            client_socket.send("<BHP:#> ".encode('ascii'))
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024).decode("utf-8")

            response = run_command(cmd_buffer)
            client_socket.send(response.encode('ascii'))


def run_command(command):
    command = command.rstrip()
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        print(repr(e))
        output = "Failed to execute command. \r\n"
    return output


def usage():
    print("BHP Net Tool"
          "\n"
          "Usage: bhpnet.py -t target_host -p port\n"
          "\n"
          "-l --listen              - listen on [host]:[port] for incoming connections\n"
          "-e --execute=file_to_run - execute the given file upon receiving a connection.\n"
          "-c --command             - initialize command shell\n"
          "-u --upload=destination  - upon receiving a connection upload a file and write to [destination]\n"
          "\n"
          "\n"
          "Examples:\n"
          "bhpnet.py -t 192.168.0.1 -p 5555 -l -c\n"
          "bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe\n"
          "bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"\n"
          "echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135\n")
    sys.exit(0)


def main():
    listen = False
    command = False
    upload = False
    execute = ""
    target = ""
    upload_destination = ""
    port = 0

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                                   ["help", "listen", "execute", "target", "port", "command", "upload"])
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
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

    if not listen and len(target) and port > 0:
        buffer = sys.stdin.read()
        client_sender(buffer, target, port)
    if listen:
        server_loop(target, port, execute, command, upload_destination)


if __name__ == "__main__":
    main()
