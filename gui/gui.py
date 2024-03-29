import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msg

from gui.frames import Explorer, RenameMany
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
        self.command_menu.add_command(label='rename', command=self.rename_popup)
        self.command_menu.add_command(label="delete", command=self.delete)
        self.bind_all("<Control_L><z>", self.undo)
        self.bind_all("<Control_L><y>", self.redo)

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
        tab.l_frm.tree.tree.bind("<Control_L><c>", lambda e: self.store_src("copy", e))
        tab.l_frm.tree.tree.bind("<Control_L><x>", lambda e: self.store_src("move", e))
        tab.l_frm.tree.tree.bind("<Control_L><v>", self.paste)
        tab.l_frm.tree.tree.bind("<Delete>", self.delete)
        tab.l_frm.tree.tree.bind("<Double-Button-1>", self.open)
        if self.view_var.get() == "double":
            tab.transfer_bar.copy_right_btn["command"] = lambda: self.transfer("right", "copy")
            tab.transfer_bar.copy_left_btn["command"] = lambda: self.transfer("left", "copy")
            tab.transfer_bar.move_right_btn["command"] = lambda: self.transfer("right", "move")
            tab.transfer_bar.move_left_btn["command"] = lambda: self.transfer("left", "move")
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
            tab.r_frm.tree.tree.bind("<Control_L><c>", lambda e: self.store_src("copy", e))
            tab.r_frm.tree.tree.bind("<Control_L><x>", lambda e: self.store_src("move", e))
            tab.r_frm.tree.tree.bind("<Control_L><v>", self.paste)
            tab.r_frm.tree.tree.bind("<Delete>", self.delete)
            tab.r_frm.tree.tree.bind("<Double-Button-1>", self.open)
        self.nbook.add(tab, text=text)
        self.refresh()

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
        except PermissionError as e:
            msg.showerror(title="Permission denied", message=str(e))
            button.master.addr_var.set(button.master.master.current_dir)

    def refresh(self):
        """
        Refresh all frames and displayed content.
        """

        for frm in self.nbook.tabs():
            frm = self.nametowidget(frm)
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
            if len(event.widget.selection()) <= 1:
                event.widget.selection_set(iid)
            event.widget.focus(item=iid)
            self.prev_focus = event.widget
            self.command_menu.post(event.x_root, event.y_root)

    def paste(self, event=None):
        """
        Paste copied object and refresh displayed tab.
        """

        if event:
            self.prev_focus = event.widget

        dst = self.prev_focus.master.master.current_dir
        try:
            self.fe.paste(dst)
        except FileNotFoundError as e:
            msg.showerror("Invalid destination directory", str(e))
        explorer = self.prev_focus.master.master.master
        self.refresh()

    def invalid_addr(self, widget):
        """
        Restore last correct dir path to address bar.
        """

        widget = self.nametowidget(widget)
        current_dir = widget.master.master.current_dir
        widget.master.addr_var.set(current_dir)

    def store_src(self, func, event=None):
        """
        Store file or dir path to copy/move it later.

        Parameters
        ---------------
        func : {move, copy}
            file operation intended for src file
        """

        if event:
            self.prev_focus = event.widget

        if self.prev_focus.selection():
            objs = self.get_path()
            try:
                objs["func"] = func
                self.fe.store_src(objs)
            except FileNotFoundError as e:
                msg.showerror("Invalid destination directory", str(e))
            explorer = self.prev_focus.master.master.master
        self.refresh()

    def transfer(self, direction, func):
        """
        Transfer files and directories between two open explorer frames.

        Parameters
        ---------------
        direction : {left, right}
            left -> transfer object from right to left
            right -> left to right
        func : {move, copy}
            file operation intended for src file
        """

        names = []
        widget = self.nametowidget(self.nbook.select())
        l_addr = widget.l_frm.nav_bar.addr_var.get()
        r_addr = widget.r_frm.nav_bar.addr_var.get()
        tree = widget.l_frm.tree.tree if direction == "right" else widget.r_frm.tree.tree
        src = l_addr if direction == "right" else r_addr
        dst = r_addr if direction == "right" else l_addr
        for item in tree.selection():
            row = tree.item(item)["values"]
            if row:
                names.append(row[0])
        objs = {"src": src, "dst": dst, "names": names, "func": func}
        self.fe.transfer(objs)
        self.refresh()

    def rename_popup(self):
        """
        Display entries to rename objects.
        """

        if len(self.prev_focus.selection()) == 1:
            x, y, w, h = self.prev_focus.bbox(self.prev_focus.focus(), column="Name")
            entry = ttk.Entry(self.prev_focus)
            entry.place(x=x, y=y, width=w, height=h)
            entry.focus()
            entry.bind("<FocusOut>", lambda e: entry.destroy())
            entry.bind("<Return>", lambda e: self.rename(entry))
        elif len(self.prev_focus.selection()) > 1:
            rename = RenameMany(self)
            rename.submit_btn["command"] = lambda: self.rename_many(rename)

    def rename_many(self, rename):
        """
        Rename object using a common name and optional predefined or custom
        prefix and suffix.
        """

        selection = self.get_path()
        prefix = rename.pref_var.get()
        name = rename.name_var.get()
        suffix = rename.suff_var.get()
        self.fe.rename_many(selection, name, prefix, suffix)
        self.refresh()
        rename.destroy()

    def rename(self, entry):
        """
        Rename an object.

        Parameters
        ---------------
        entry : ttk.Entry
            entry created by rename_popup containing w new file/dir name
        """

        new_name = entry.get()
        selection = self.get_path()
        directory, name = selection["parent"], selection["names"][0]

        try:
            self.fe.rename(directory, name, new_name)
        except FileExistsError as e:
            msg.showerror(f"File {new_name} already exists", str(e))
        finally:
            entry.destroy()
            self.refresh()

    def delete(self, event=None):
        """
        Permanently delete a file or directory and clear cache.
        """

        if event:
            self.prev_focus = event.widget

        if self.prev_focus.focus():
            objs = self.get_path()
            message = "Do you really want to delete selected items?\n" \
            "This operation can't be undone."
            if msg.askyesno(title="Delete", message=message):
                self.fe.delete(objs)
                self.fe.clear_cache()
        self.refresh()

    def get_path(self):
        """
        Get selected objects names and parent dir path.

        Returns
        ---------------
        dictionary
            parent: object parent directory
            names: list of file/dir names
        """

        names = []
        directory = self.prev_focus.master.master.current_dir
        for selected in self.prev_focus.selection():
            row = self.prev_focus.item(selected)["values"]
            name = row[0]
            names.append(name)
        return {"parent": directory, "names": names}

    def undo(self, event):
        """
        Undo a previously performed action.
        """

        try:
            self.fe.undo()
        except FileNotFoundError as e:
            title = "Operation can't be undone"
            message = "An error has occured while undoing operation "
            msg.showerror(title=title, message=f"{message}: {str(e)}")
        self.refresh()

    def redo(self, event):
        """
        Redo a previously undone action.
        """

        try:
            self.fe.redo()
        except FileNotFoundError as e:
            title = "Operation can't be redone"
            message = "An error has occured while redoing operation "
            msg.showerror(title=title, message=f"{message}: {str(e)}")
        self.refresh()

    def open(self, event):
        """
        Open file or dir. If file - open in default application or choose one.
        If dir - display it's content. Show error message if it does not exist
        or user has no permission.
        """

        row = event.widget.item(event.widget.selection())["values"]
        name = row[0]
        current_dir = event.widget.master.master.nav_bar.addr_var.get()
        dst_dir = self.fe.open(current_dir, name)
        if dst_dir:
            event.widget.master.master.nav_bar.addr_var.set(dst_dir)
        self.refresh()
