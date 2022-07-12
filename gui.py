import tkinter as tk
from tkinter import ttk

from frames import ExplorerFrm, ExplorerTree


class GUI(tk.Tk):
    """
    GUI for file explorer.
    """

    def __init__(self):
        super().__init__()
        self.title("File Explorer")
        self.style = ttk.Style()
        self.style.configure("ExpBar.TButton", width=5)
        self.frm = ExplorerFrm(self)
        self.frm.grid(row=0, column=0, sticky="we")
        self.tree_frm = ExplorerTree(self)
        self.tree_frm.grid(row=1, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

g = GUI()
g.mainloop()
