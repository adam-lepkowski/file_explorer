from tkinter import ttk

from frames import ExplorerFrm, ExplorerTree


class Container(ttk.Frame):
    """
    Container frame for explorer main components.

    Attributes
    ---------------
    frm : ExplorerFrm
        address bar and associated buttons
    tree_frm : ExplorerTree
        directory content view and manipulation
    """

    def __init__(self, root):
        super().__init__(root)
        self.frm = ExplorerFrm(self)
        self.frm.grid(row=0, column=0, sticky="we")
        self.tree_frm = ExplorerTree(self)
        self.tree_frm.grid(row=1, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
