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
        self.view_menu.add_command(label="Close Tab", command=self.close_tab)
        self.tab_1 = Container(self.nbook)
        self.nbook.add(self.tab_1, text="Tab 1")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.bind("<Control_L><w>", self.close_tab)
        self.bind("<Control_L><t>", self.add_tab)

    def add_tab(self, event=None):
        """
        Open new tab with Container set up.
        """

        text = f"Tab {len(self.nbook.tabs()) + 1}"
        tab = Container(self.nbook)
        self.nbook.add(tab, text=text)

    def close_tab(self, event=None):
        """
        Close currently viewed tab if more than one tab is open.
        """

        if len(self.nbook.tabs()) > 1:
            self.nbook.forget(self.nbook.select())


g = GUI()
g.mainloop()
