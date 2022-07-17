from tkinter import ttk

from frames import NavBar, DirContent, ObjectTransfer


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


class Explorer(ttk.Frame):
    """
    Main File Explorer frame. View one or two dirs in adjacent frames.

    Parameters
    ---------------
    root
        frames container
    view : {'single', 'double'}, default='single'
        set Explorer view

    Attributes
    ---------------
    l_frm : Container
        frame positioned on the left side
    transfer_bar : ObjectTransfer
        transfer buttons. Only in double view
    r_frm : Container
        frame positioned on the right side. Only in double view
    """

    def __init__(self, root, view="single"):
        super().__init__(root)
        self.l_frm = Container(self)
        self.l_frm.grid(row=0, column=0, sticky="nsew")
        if view == "double":
            self.transfer_bar = ObjectTransfer(self)
            self.transfer_bar.grid(row=0, column=1, sticky="ns")
            self.r_frm = Container(self)
            self.r_frm.grid(row=0, column=2, sticky="nsew")
            self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
