import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msg

from gui.frames import Explorer
from explorer import Facade


class GUI(tk.Tk):
    """
    GUI for file explorer.

    Attributes
    ---------------
    style : ttk.Style
    nbook : ttk.Notebook
        represent Explorer frames in a tabbed view
    menubar : tk.Menu
        menu bar holding view options and methods
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
        self.view_var = tk.StringVar()
        self.view_var.set("double")
        self.view_menu.add_checkbutton(
            label="Toggle adjacent explorer", variable=self.view_var,
            onvalue="double", offvalue="single"
        )
        self.view_menu.add_command(label="New Tab", command=self.add_tab)
        self.view_menu.add_command(label="Close Tab", command=self.close_tab)
        self.fe = Facade()
        self.add_tab()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.bind("<Control_L><w>", self.close_tab)
        self.bind("<Control_L><t>", self.add_tab)
        self.prev_focus = None
        self.command_menu = tk.Menu(self)
        self.command_menu.add_command(label='copy')

    def add_tab(self, event=None):
        """
        Open new tab. Set up container with default directory content displayed
        """

        text = f"Tab {len(self.nbook.tabs()) + 1}"
        tab = Explorer(self.nbook, view=self.view_var.get())
        default_dir = self.fe.get_default_dir()
        tab.l_frm.nav_bar.addr_bar.insert(0, default_dir)
        tab.l_frm.current_dir = default_dir
        l_cnf = tab.l_frm.nav_bar.cnf_addr_btn
        l_nav_bar = tab.l_frm.nav_bar.addr_bar
        l_cnf["command"] = lambda button=l_cnf: self.display_content(button)
        l_nav_bar.bind("<Return>", lambda event: l_cnf.invoke())
        l_parent_btn = tab.l_frm.nav_bar.parent_btn
        l_parent_btn["command"] = lambda button=l_parent_btn: self.display_parent(button)
        tab.l_frm.tree.tree.bind('<Button-3>', self.menu_popup)
        l_cnf.invoke()
        if self.view_var.get() == "double":
            tab.r_frm.nav_bar.addr_bar.insert(0, default_dir)
            tab.r_frm.current_dir = default_dir
            r_cnf = tab.r_frm.nav_bar.cnf_addr_btn
            r_nav_bar = tab.r_frm.nav_bar.addr_bar
            r_cnf["command"] = lambda button=r_cnf: self.display_content(button)
            r_nav_bar.bind("<Return>", lambda event: r_cnf.invoke())
            r_parent_btn = tab.r_frm.nav_bar.parent_btn
            r_parent_btn["command"] = lambda button=r_parent_btn: self.display_parent(button)
            tab.r_frm.tree.tree.bind('<Button-3>', self.menu_popup)
            r_cnf.invoke()
        self.nbook.add(tab, text=text)

    def close_tab(self, event=None):
        """
        Close currently viewed tab if more than one tab is open.
        """

        if len(self.nbook.tabs()) > 1:
            self.nbook.forget(self.nbook.select())

    def display_content(self, button):
        """
        Display directory content.

        Parameters
        ---------------
        button : ttk.Button
            button that called the method
        """

        path = button.master.addr_bar.get()
        try:
            content = self.fe.get_content(path)
            tree = button.master.master.tree.tree
            tree.delete(*tree.get_children())
            for row in content:
                tree.insert(parent="", index="end", values=row)
            button.master.master.current_dir = path
        except FileNotFoundError as e:
            msg.showerror(title="Invalid directory", message=str(e))
            button.master.addr_bar.delete(0, tk.END)
            button.master.addr_bar.insert(0, button.master.master.current_dir)

    def display_parent(self, button):
        """
        Display currently viewed directories parent dir.

        Parameters
        ---------------
        button : ttk.Button
            button that called the method
        """

        path = button.master.master.current_dir
        parent = self.fe.get_parent(path)
        button.master.addr_bar.delete(0, tk.END)
        button.master.addr_bar.insert(0, parent)
        button.master.cnf_addr_btn.invoke()

    def menu_popup(self, event):
        """
        Display popup menu containing explorer functions.
        """

        iid = event.widget.identify_row(event.y)
        if iid:
            event.widget.selection_set(iid)
            self.command_menu.post(event.x_root, event.y_root)
