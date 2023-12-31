import tkinter as tk
import threading
import signal
import sys

from server import Server
from gui import GUI, CustomStyle
from utils import get_server_details

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

if __name__ == "__main__":

    address, port = get_server_details()

    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    custom_style = CustomStyle()
    gui = GUI(root, on_shutdown)

    serverInstance = Server(gui.add_client, gui.remove_client, address, port)

    server_thread = threading.Thread(target=serverInstance.start_server, daemon=True)
    server_thread.start()
    root.mainloop()