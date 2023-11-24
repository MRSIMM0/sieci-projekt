import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk

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
    clients = {}
    current_item = None
    items = {}

    def __init__(self, root, on_shutdown):
        self.root = root
        self.on_shutdown = on_shutdown
        self.configure_root()
        self.create_widgets()

    def configure_root(self):
        self.root.configure(background='grey')
        self.root.geometry("800x480")
        self.root.title("Server")

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root, width=800, height=480)
        self.main_frame.pack(fill='both', expand=True)

        self.tree = ttk.Treeview(self.main_frame, style='Custom.Treeview')
        self.tree['columns'] = ('#1',)
        self.tree['show'] = 'headings'
        self.tree.column('#1', width=100, anchor='center')
        self.tree.grid(row=0, column=0, sticky='nsew')
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        self.tree_indicator_label = tk.Label(self.main_frame, text="")
        self.tree_indicator_label.grid(row=1, column=0, sticky='w')

        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.grid(row=0, column=1, sticky='nsew')

        self.button = ctk.CTkButton(master=self.right_frame, text="Shutdown",command=self.on_shutdown, fg_color='red', hover_color='red3', corner_radius=10)
        self.button.pack(side='bottom', pady=10)

        self.details_label = tk.Label(master=self.right_frame, text="")
        self.details_label.pack()

        self.update_tree_indicator()
        self.right_frame.grid_remove()
        self.main_frame.grid_columnconfigure(1, weight=0)

        self.main_frame.grid_columnconfigure(0, weight=3)
        self.main_frame.grid_rowconfigure(0, weight=1)

    def update_tree_indicator(self):
        if not self.tree.get_children():
            self.tree_indicator_label.config(text="There are no clients connected")
        else:
            self.tree_indicator_label.config(text="")

    def add_client(self, client):
        item = self.tree.insert('', 'end', values=(client.details['name'],))
        self.clients[client] = item
        self.items[item] = client
        if len(self.clients) % 2 == 0:
            self.tree.item(item, tags='even')
        else:
            self.tree.item(item, tags='odd')
        self.update_tree_indicator()
        self.tree.tag_configure('even', background='gray47')
        self.tree.tag_configure('odd', background='gray55')

    def remove_client(self, client):
        item = self.clients.get(client)
        if item is not None and item != '':
            self.tree.delete(item)
            del self.clients[client]
            self.update_tree_indicator()

    def on_select(self, event):
        item = self.tree.selection()
        if item:
            selected = self.tree.item(item[0], 'values')[0]
            self.current_item = self.items.get(item[0])
            self.details_label.config(text=selected)
            self.right_frame.grid()
            self.main_frame.grid_columnconfigure(1, weight=1)
        else:
            self.right_frame.grid_remove()
            self.main_frame.grid_columnconfigure(1, weight=0)


