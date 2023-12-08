import socket
import os
import sys
import time
import threading

from utils import shutdown
from details import Details
class Client:
    def __init__(self, address, port):
        self.client_socket = None
        self.running = True
        self.address = address
        self.port = port
        self.details_thread_running = False

    def signal_handler(self, sig, frame):
        self.client_socket.close()
        sys.exit(0)

    def handle_server_message(self, message):
        if message == "shutdown":
            shutdown()

    def start_details_thread(self):
        def send_details():
            while self.details_thread_running:
                try:
                    details = Details().getJson()
                    self.client_socket.send(bytes(details, 'UTF-8'))
                    time.sleep(2)
                except Exception as e:
                    self.stop()
                    break

        self.details_thread_running = True
        details_thread = threading.Thread(target=send_details, daemon=True)
        details_thread.start()

    def stop(self):
        self.running = False
        self.details_thread_running = False
        self.client_socket.close()

    def start_client(self):
        while True:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((self.address, self.port))
                print("Connected to server.")

                break
            except Exception as e:
                self.client_socket.close()
                print("Failed to connect to server. Retrying...")
                time.sleep(2)

        self.start_details_thread()

        try:
            self.running = True
            while self.running:
                msg = self.client_socket.recv(1024)
                if not msg:
                    self.stop()
                    self.start_client()
                    break
                print('Received from server: ', msg.decode('utf-8'))
                self.handle_server_message(msg.decode('utf-8'))
        except Exception as e:
            print("Lost connection to server. Reconnecting...")
            self.stop()
            self.start_client()