import sys
import socket
import threading
import argparse


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except:
        print("[!!] Failed to listen on {local_host}:{local_port}".format(local_host=local_host, local_port=local_port))
        print("[!!] Check for other listening socket or correct permissions.")
        sys.exit(0)

    print(f"[*] Listening on {local_host}:{local_port}".format(local_host=local_host, local_port=local_port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        print("[==>] Receive incoming connection from {client_host}:{client_port}".format(client_host=addr[0],
                                                                                          client_port=addr[1]))
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port,
                                                                    receive_first))
        proxy_thread.start()


def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

        remote_buffer = response_handler(remote_buffer)

        if len(remote_buffer):
            print("[<==] Sending {} bytes to localhost".format(len(remote_buffer)))
            client_socket.send(remote_buffer)

    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            print("[==>] Received {} bytes from localhost".format(len(local_buffer)))
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] sent to remote.")

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Received {} bytes from remote.".format(len(remote_buffer)))
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[<==] Sent to Localhost.")

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data, Closing Connections")
            break


def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, str) else 2

    for i in range(0, len(src), length):
        s = src[i:i + length]
        hexa = ' '.join([f"{ord(x):{digits}x}" for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(b"%04X %-*s %s" % (i, length * (digits + 1), hexa, text))

    print(b'\n'.join(result))


def receive_from(connection):
    buffer = ""
    connection.settimeout(2)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except:
        pass

    return buffer


def response_handler(buffer):
    # perform packet modification
    return buffer


def request_handler(buffer):
    # perform packet modification
    return buffer


def main(args):
    local_host = args.lh
    local_port = args.lp
    remote_host = args.rh
    remote_port = args.rp
    receive_first = args.first

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-lh', type=str, help="local host")
    parser.add_argument('-lp', type=str, help='local port')
    parser.add_argument('-rh', type=str, help="remote host")
    parser.add_argument('-rp', type=str, help='remote port')
    parser.add_argument('-first', action='store_true', help='Receive first or not')
    args = parser.parse_args()
    main(args)
