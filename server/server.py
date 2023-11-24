import threading
import socket
import json
class ClientThread(threading.Thread):
    def __init__(self, client_address, client_socket,remove_conn, add_conn):

        threading.Thread.__init__(self)
        self.csocket = client_socket
        self.client_address = client_address
        self.remove_conn = remove_conn
        self.details = None
        self.add_conn = add_conn
        print("New connection added: ", self.client_address)

    def run(self):
        print("Connection from : ", self.client_address)

        while True:
            data = self.csocket.recv(2048)
            if not data:
                self.disconnect()
                break

            self.details = json.loads(data.decode('utf-8'))
            self.add_conn(self)

    def send_message(self, message):
        self.csocket.send(bytes(message, 'UTF-8'))

    def disconnect(self):
        print("Client at ", self.client_address , " disconnected...")
        self.remove_conn(self)
        self.csocket.close()

class Server():
    def __init__(self, add_conn, remove_conn):
        self.add_conn = add_conn
        self.remove_conn = remove_conn
        pass

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", 8080))
        print("Server started")
        print("Waiting for client request..")
        while True:
            server.listen(1)
            client_sock, client_addr = server.accept()
            new_thread = ClientThread(client_addr, client_sock, self.remove_conn, self.add_conn)
            new_thread.start()