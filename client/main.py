import socket
import os
import json
import sys
import psutil
import time
import threading


class Details():
    def __init__(self):
        self.name = socket.gethostname()
        self.osName = os.name
        self.cpu = psutil.cpu_percent(4)
        self.ramPercentage= psutil.virtual_memory()[2]
        self.ramUsed = "{:.1f}".format(psutil.virtual_memory()[3]/1000000000)
        self.ramTotal = "{:.1f}".format(psutil.virtual_memory()[0]/1000000000)
        disk = psutil.disk_usage('/')
        self.diskTotal = "{:.1f}".format(disk.total/1000000000)
        self.diskUsed = "{:.1f}".format(disk.used/1000000000)
        self.diskFree = "{:.1f}".format(disk.free/1000000000)
        self.diskPercentage = disk.percent

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
    client_socket.connect(('192.168.1.19', 8080))
    def send_details():
        while True:
            details = json.dumps(Details().__dict__)
            client_socket.send(bytes(details, 'UTF-8'))
            time.sleep(4)

    details_thread = threading.Thread(target=send_details)
    details_thread.start()

    while True:
        try:
            client_socket.connect(('192.168.1.19', 8080))
            while True:
                msg = client_socket.recv(1024)
                if not msg:
                    break
                print('Received from server: ', msg.decode('utf-8'))
                handle_server_message(msg.decode('utf-8'))
        except ConnectionResetError:
            print('Server disconnected. Reconnecting...')
            time.sleep(2)
        except Exception as e:
            print(f'An error occurred: {e}')
            time.sleep(2)
        finally:
            client_socket.close()
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if __name__ == "__main__":
    start_client()