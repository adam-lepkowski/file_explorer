from tkinter import ttk


class ExplorerFrm(ttk.Frame):

    def __init__(self, root):
        super().__init__(root)
        self["padding"] = 5
        self.parent_btn = ttk.Button(self, style="ExpBar.TButton", text="^")
        self.parent_btn.grid(row=0, column=0, sticky="we")
        # add validatecommand option to entry initialization - validate on focusout
        self.addr_bar = ttk.Entry(self)
        self.addr_bar.grid(row=0, column=1, sticky="we")
        self.cnf_addr_btn = ttk.Button(self, style="ExpBar.TButton", text=">")
        self.cnf_addr_btn.grid(row=0, column=2, sticky="we")
        self.columnconfigure(1, weight=1)
