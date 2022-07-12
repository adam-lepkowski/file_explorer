import tkinter as tk
from tkinter import ttk

from frames import Container


class GUI(tk.Tk):
    """
    GUI for file explorer.
    """

    def __init__(self):
        super().__init__()
        self.title("File Explorer")
        self.option_add("*tearOff", tk.FALSE)
        self.style = ttk.Style()
        self.style.configure("ExpBar.TButton", width=5)
        self.nbook = ttk.Notebook(self)
        self.nbook.grid(row=0, column=0, sticky="nsew")
        self.menubar = tk.Menu(self)
        self["menu"] = self.menubar
        self.view_menu = tk.Menu(self.menubar)
        self.menubar.add_cascade(menu=self.view_menu, label="View")
        self.view_menu.add_command(label="New Explorer Frame")
        self.view_menu.add_command(label="New Tab", command=self.add_tab)
        self.tab_1 = Container(self.nbook)
        self.nbook.add(self.tab_1, text="Tab 1")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def add_tab(self):
        """
        Open new tab with Container set up.
        """
        
        text = f"Tab {len(self.nbook.tabs()) + 1}"
        tab = Container(self.nbook)
        self.nbook.add(tab, text=text)

g = GUI()
g.mainloop()
