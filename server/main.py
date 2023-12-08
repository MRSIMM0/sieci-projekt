import tkinter as tk
import threading
import signal
import sys

from server import Server
from gui import GUI, CustomStyle

default_address = 'localhost'
default_port = 8080

use_default = input("Do you want to use the default address and port (localhost:8080)? (yes/no): ")
if use_default.lower() != 'yes':
    address = input("Enter the server address: ")
    port = int(input("Enter the server port: "))
else:
    address = default_address
    port = default_port

def signal_handler(sig, frame):
    serverInstance.stop_server()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def on_shutdown():
    gui.current_item.send_message("shutdown")
    gui.current_item.disconnect()
    pass

def on_closing():
    serverInstance.stop_server()
    root.destroy()
    sys.exit(0)

root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)
custom_style = CustomStyle()
gui = GUI(root, on_shutdown)

serverInstance = Server(gui.add_client, gui.remove_client, address, port)

server_thread = threading.Thread(target=serverInstance.start_server, daemon=True)
server_thread.start()
root.mainloop()