import socket
import threading

HOST = '0.0.0.0'
PORT = 9999


def handle_client(client_socket):
    request = client_socket.recv(1024)
    print(f"[*] Received: {request}")
    client_socket.send(b"ACK!")
    client_socket.close()


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)

        print(f"[*] Listening on {HOST} {PORT}")
        while True:
            conn, addr = s.accept()
            print(f"[*] Accepted connection from: {addr[0]}:{addr[1]}")
            client_handler = threading.Thread(target=handle_client, args=(conn,))
            client_handler.start()
