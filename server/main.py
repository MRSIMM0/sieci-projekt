import tkinter as tk
import threading

from server import Server
from gui import GUI, CustomStyle

def onShutdown():
    gui.current_item.send_message("shutdown")
    gui.current_item.disconnect()
    pass

root = tk.Tk()
custom_style = CustomStyle()
gui = GUI(root, onShutdown)
server = Server(gui.add_client, gui.remove_client)

server_thread = threading.Thread(target=server.start_server)
server_thread.start()
root.mainloop()