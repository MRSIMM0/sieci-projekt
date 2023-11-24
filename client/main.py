import socket
import os
import json
import sys

class Details():
    def __init__(self, name):
        self.name = name

def shutdown_computer():
    if os.name == 'nt':
        os.system('shutdown /s /t 0')
    elif os.name == 'posix':
        if sys.platform == "darwin":
            os.system('sudo shutdown -h now')
        else:
            os.system('sudo shutdown now')
    else:
        print('Unsupported operating system.')


def handle_server_message(message):
    if message == "shutdown":
        shutdown_computer()

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = socket.gethostname()

    details = json.dumps(Details(host).__dict__)

    client_socket.connect(('localhost', 8080))

    client_socket.send(bytes(details, 'UTF-8'))
    while True:
        msg = client_socket.recv(1024)
        print('Received from server: ', msg.decode('utf-8'))
        handle_server_message(msg.decode('utf-8'))

    client_socket.close()

if __name__ == "__main__":
    start_client()