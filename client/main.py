from client import Client
from utils import get_server_details

if __name__ == "__main__":
    address, port = get_server_details()

    client = Client(address, port)
    try:
        client.start_client()
    except KeyboardInterrupt:
        print("Shutting down client...")
        client.signal_handler()