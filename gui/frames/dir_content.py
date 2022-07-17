import tkinter as tk
from tkinter import ttk


class DirContent(ttk.Frame):
    """
    Frame holding treeview to browse directory content.

    Parameters
    ---------------
    root : Tk or any other container Frame
        ExplorerTree master window

    Attributes
    ---------------
    tree : ttk.Treeview
        view directory content
    scrl : tk.Scrollbar
        scroll through tree content
    """

    def __init__(self, root):
        super().__init__(root)
        self["padding"] = 5
        columns = ["Name", "Last modified", "Type"]
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.scrl = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.scrl.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrl.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.scrl.grid(row=0, column=1, sticky="sne")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
