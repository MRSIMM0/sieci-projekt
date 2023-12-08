import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from tkinter import messagebox

class CustomStyle:
    def __init__(self):
        self.style = ttk.Style()
        self.configure_styles()

    def configure_styles(self):
        self.configure_treeview_style()
        self.configure_button_style()

    def configure_treeview_style(self):
        self.style.configure('Custom.Treeview', rowheight=50)
        self.style.map('Custom.Treeview',
                       background=[('selected', 'dim gray'), ('active', 'gray30')])

    def configure_button_style(self):
        self.style.configure('Custom.CTkButton', fg_color='red', corner_radius=10)

class GUI:
    def __init__(self, root, on_shutdown):
        self.root = root
        self.on_shutdown = on_shutdown
        self.configure_root()
        self.create_widgets()
        self.clients = {}
        self.items = {}
        self.current_item = None

    def configure_root(self):
        self.root.configure(background='grey')
        self.root.geometry("800x480")
        self.root.title("Server")

    def shutdown(self):
        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to shutdown this system?")
        if confirm:
            self.on_shutdown()

    def right_frame(self):
        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.grid(row=0, column=1, sticky='nsew')

        self.details_label = tk.Label(master=self.right_frame, text="", font=("Helvetica", 14, "bold"), padx=10, pady=10)
        self.details_label.pack()

        self.system_label = tk.Label(master=self.right_frame, text="", font=("Helvetica", 14, "bold"), padx=10, pady=10)
        self.system_label.pack()

        self.cpu_label = tk.Label(master=self.right_frame, text="", font=("Helvetica", 14, "bold"), padx=10, pady=10)
        self.cpu_label.pack()

        self.ram_label = tk.Label(master=self.right_frame, text="", font=("Helvetica", 14, "bold"), padx=10, pady=10)
        self.ram_label.pack()

        self.disk_label = tk.Label(master=self.right_frame, text="", font=("Helvetica", 14, "bold"), padx=10, pady=10)
        self.disk_label.pack()

        self.button = ctk.CTkButton(master=self.right_frame, text="Shutdown",command=self.shutdown, fg_color='red', hover_color='red3', corner_radius=10)
        self.button.pack(side='bottom', pady=10)

        self.update_tree_indicator()
        self.right_frame.grid_remove()
        pass
    def tree(self):
        self.tree = ttk.Treeview(self.main_frame, style='Custom.Treeview')
        self.tree['columns'] = ('#1',)
        self.tree['show'] = 'headings'
        self.tree.column('#1', width=100, anchor='center')
        self.tree.grid(row=0, column=0, sticky='nsew')
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
    def tree_indicator(self):
        self.tree_indicator_label = tk.Label(self.main_frame, text="")
        self.tree_indicator_label.grid(row=1, column=0, sticky='w')

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root, width=800, height=480)
        self.main_frame.pack(fill='both', expand=True)

        self.tree()

        self.tree_indicator()

        self.right_frame()

        self.main_frame.grid_columnconfigure(1, weight=0)

        self.main_frame.grid_columnconfigure(0, weight=3)
        self.main_frame.grid_rowconfigure(0, weight=1)

    def update_tree_indicator(self):
        if not self.tree.get_children():
            self.tree_indicator_label.config(text="There are no clients connected")
        else:
            self.tree_indicator_label.config(text="")

    def add_client(self, client):
        try:
            item = self.clients.get(client.client_address)
            if item is not None:
                self.tree.item(item, values=(client.details['name'],))
                self.update_details()
            else:
                item = self.tree.insert('', 'end', values=(client.details['name'],))
                self.clients[client.client_address] = item
                self.items[item] = client
                if len(self.clients) % 2 == 0:
                    self.tree.item(item, tags='even')
                else:
                    self.tree.item(item, tags='odd')
                self.tree.tag_configure('even', background='gray47')
                self.tree.tag_configure('odd', background='gray55')
            self.update_tree_indicator()
        except Exception as e:
            pass


    def remove_client(self, client):
        item = self.clients.get(client.client_address)
        if item is not None and item != '':
            self.tree.delete(item)
            del self.clients[client.client_address]
            self.update_tree_indicator()

    def update_details(self):
        current_item = self.current_item
        self.system_label.config(text=f"System: {current_item.details['osName']}")
        self.details_label.config(text=f"Device Name: {current_item.details['name']}")
        self.cpu_label.config(text=f"CPU Usage: {current_item.details['cpu']}%")
        self.ram_label.config(text=f"RAM Usage: {current_item.details['ramPercentage']}% - {current_item.details['ramUsed']}GB/{current_item.details['ramTotal']}GB")
        self.disk_label['text'] = f"Disk: {current_item.details['diskUsed']}GB/{current_item.details['diskTotal']}GB ({current_item.details['diskPercentage']}%)"

    def on_select(self, event):
        item = self.tree.selection()
        if item:
            current_item = self.items.get(item[0])
            self.current_item = current_item
            self.update_details()
            self.right_frame.grid()
            self.main_frame.grid_columnconfigure(1, weight=1)
        else:
            self.right_frame.grid_remove()
            self.main_frame.grid_columnconfigure(1, weight=0)


