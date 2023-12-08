import signal
from client import Client


def get_server_details():
    default_address = 'localhost'
    default_port = 8080

    use_default = input("Do you want to use the default address and port (localhost:8080)? (yes/no): ")
    if use_default.lower() != 'yes':
        address = input("Enter the server address: ")
        port = int(input("Enter the server port: "))
    else:
        address = default_address
        port = default_port
    return address, port

if __name__ == "__main__":
    address, port = get_server_details()

    client = Client(address, port)
    signal.signal(signal.SIGINT, client.signal_handler)
    client.start_client()