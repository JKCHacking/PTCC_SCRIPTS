import socket
import threading
from queue import Queue

target = '10.0.241.254'
q = Queue()
open_port_list = []


def port_scan(port):
    connect_info = (target, port)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(connect_info)
        return True
    except:
        return False


def fill_queue(port_list):
    for port in port_list:
        q.put(port)


def worker():
    while not q.empty():
        port = q.get()
        if port_scan(port):
            print(f'port {port} is open')
            open_port_list.append(port)


port_list = range(1, 1024)
fill_queue(port_list=port_list)

thread_list = []

thread_num = 10
for t in range(thread_num):
    thread = threading.Thread(target=worker)
    thread_list.append(thread)

for thread in thread_list:
    thread.start()

for thread in thread_list:
    thread.join()

print("Open port are: ", open_port_list)
