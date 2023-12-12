import os
import sys
import subprocess

def shutdown():
    try:
        if os.name == 'nt':
            subprocess.call(['shutdown', '/s', '/t', '0'])
        elif os.name == 'posix':
            if sys.platform == "darwin":
                subprocess.call(['shutdown', '-h', 'now'])
            else:
                subprocess.call(['shutdown', 'now'])
        else:
            print('Unsupported operating system.')
    except Exception as e:
        print(f"Failed to shutdown: {e}")

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
