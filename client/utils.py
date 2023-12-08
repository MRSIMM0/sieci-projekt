def shutdown():
        if os.name == 'nt':
            os.system('shutdown /s /t 0')
        elif os.name == 'posix':
            if sys.platform == "darwin":
                os.system('sudo shutdown -h now')
            else:
                os.system('sudo shutdown now')
        else:
            print('Unsupported operating system.')

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
