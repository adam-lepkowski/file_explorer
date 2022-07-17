from tkinter import ttk

from frames import NavBar, DirContent


class Container(ttk.Frame):
    """
    Container frame for explorer main components.

    Attributes
    ---------------
    nav_bar : NavBar
        address bar and associated buttons
    tree : DirContent
        directory content view and manipulation
    """

    def __init__(self, root):
        super().__init__(root)
        self.nav_bar = NavBar(self)
        self.nav_bar.grid(row=0, column=0, sticky="we")
        self.tree = DirContent(self)
        self.tree.grid(row=1, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
