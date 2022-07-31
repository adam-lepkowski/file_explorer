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
    fe : Facade
        core file manipulation, display and cache functionality
    prev_focus : tk.Widget or None
        display container that had focus before the one currently focused
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
        self.command_menu.add_command(
            label='copy', command=lambda: self.store_src("copy")
        )
        self.command_menu.add_command(
            label='cut', command=lambda: self.store_src("move")
        )
        self.command_menu.add_command(label='paste', command=self.paste)

    def add_tab(self, event=None):
        """
        Open new tab. Set up container with default directory content displayed
        """

        text = f"Tab {len(self.nbook.tabs()) + 1}"
        tab = Explorer(self.nbook, view=self.view_var.get())
        default_dir = self.fe.get_default_dir()
        tab.l_frm.nav_bar.addr_var.set(default_dir)
        tab.l_frm.current_dir = default_dir
        l_cnf = tab.l_frm.nav_bar.cnf_addr_btn
        l_nav_bar = tab.l_frm.nav_bar.addr_bar
        l_cnf["command"] = lambda: self.display_content(l_cnf)
        l_nav_bar.bind("<Return>", lambda event: l_cnf.invoke())
        l_parent_btn = tab.l_frm.nav_bar.parent_btn
        l_parent_btn["command"] = lambda: self.display_parent(l_parent_btn)
        vcmd = (self.register(self.fe.is_valid_path), "%P")
        ivcmd = (self.register(self.invalid_addr), "%W")
        l_nav_bar.configure(
            validate="focusout", validatecommand=vcmd, invalidcommand=ivcmd
        )
        tab.l_frm.tree.tree.bind('<Button-3>', self.menu_popup)
        if self.view_var.get() == "double":
            tab.r_frm.nav_bar.addr_var.set(default_dir)
            tab.r_frm.current_dir = default_dir
            r_cnf = tab.r_frm.nav_bar.cnf_addr_btn
            r_nav_bar = tab.r_frm.nav_bar.addr_bar
            r_cnf["command"] = lambda: self.display_content(r_cnf)
            r_nav_bar.bind("<Return>", lambda event: r_cnf.invoke())
            r_parent_btn = tab.r_frm.nav_bar.parent_btn
            r_parent_btn["command"] = lambda: self.display_parent(r_parent_btn)
            r_nav_bar.configure(
                validate="focusout", validatecommand=vcmd, invalidcommand=ivcmd
            )
            tab.r_frm.tree.tree.bind('<Button-3>', self.menu_popup)
        self.refresh(tab)
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

        path = button.master.addr_var.get()
        try:
            content = self.fe.get_content(path)
            tree = button.master.master.tree.tree
            tree.delete(*tree.get_children())
            for row in content:
                tree.insert(parent="", index="end", values=row)
            button.master.master.current_dir = path
        except FileNotFoundError as e:
            msg.showerror(title="Invalid directory", message=str(e))
            button.master.addr_var.set(button.master.master.current_dir)

    def refresh(self, frm):
        """
        Refresh frame and displayed content.
        """

        frm.l_frm.nav_bar.cnf_addr_btn.invoke()
        frm.r_frm.nav_bar.cnf_addr_btn.invoke()

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
        button.master.addr_var.set(parent)
        button.master.cnf_addr_btn.invoke()

    def menu_popup(self, event):
        """
        Display popup menu containing explorer functions.
        """

        iid = event.widget.identify_row(event.y)
        if iid:
            event.widget.selection_set(iid)
            event.widget.focus(item=iid)
            self.prev_focus = event.widget
            self.command_menu.post(event.x_root, event.y_root)

    def copy(self):
        """
        Store file or dir path to be copied later.
        """

        row = self.prev_focus.item(self.prev_focus.focus())["values"]
        name = row[0]
        directory = self.prev_focus.master.master.current_dir
        try:
            self.fe.copy(directory, name)
        except FileNotFoundError as e:
            msg.showerror("Invalid destination directory", str(e))
        explorer = self.prev_focus.master.master.master
        self.refresh(explorer)

    def paste(self):
        """
        Paste copied object and refresh displayed tab.
        """

        dst = self.prev_focus.master.master.current_dir
        try:
            self.fe.paste(dst)
        except FileNotFoundError as e:
            msg.showerror("Invalid destination directory", str(e))
        explorer = self.prev_focus.master.master.master
        self.refresh(explorer)

    def invalid_addr(self, widget):
        """
        Restore last correct dir path to address bar.
        """

        widget = self.nametowidget(widget)
        current_dir = widget.master.master.current_dir
        widget.master.addr_var.set(current_dir)

    def store_src(self, mode):
        """
        Store file or dir path to copy/move it later.

        Parameters
        ---------------
        mode : {move, copy}
            file operation intended for src file
        """

        row = self.prev_focus.item(self.prev_focus.focus())["values"]
        name = row[0]
        directory = self.prev_focus.master.master.current_dir
        try:
            self.fe.store_src(directory, name, mode)
        except FileNotFoundError as e:
            msg.showerror("Invalid destination directory", str(e))
        explorer = self.prev_focus.master.master.master
        self.refresh(explorer)
