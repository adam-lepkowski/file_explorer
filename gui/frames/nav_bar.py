import tkinter as tk
from tkinter import ttk


class NavBar(ttk.Frame):
    """
    Frame holding Explorer buttons and address bar.

    Parameters
    ---------------
    root : Tk or any other container Frame
        ExplorerFrm master window

    Attributes
    ---------------
    parent_btn : ttk.Button
        direct File Explorer to currently viewed directories parent
    cnf_addr_brn : ttk.Button
        confirm path entered to addr_bar
    addr_bar : ttk.Entry
        hold currently viewed directory absolute path
    addr_var : tk.StringVar
        address bar string variable
    """

    def __init__(self, root):
        super().__init__(root)
        self["padding"] = 5
        self.parent_btn = ttk.Button(self, style="ExpBar.TButton", text="^")
        self.parent_btn.grid(row=0, column=0, sticky="we")
        self.addr_var = tk.StringVar(self)
        self.addr_bar = ttk.Entry(self, textvariable=self.addr_var)
        self.addr_bar.grid(row=0, column=1, sticky="we")
        self.cnf_addr_btn = ttk.Button(self, style="ExpBar.TButton", text=">")
        self.cnf_addr_btn.grid(row=0, column=2, sticky="we")
        self.columnconfigure(1, weight=1)
