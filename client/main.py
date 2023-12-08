import signal
from client import Client
from utils import get_server_details

if __name__ == "__main__":
    address, port = get_server_details()

    client = Client(address, port)
    signal.signal(signal.SIGINT, client.signal_handler)
    try:
        client.start_client()
    except KeyboardInterrupt:
        client.signal_handler()