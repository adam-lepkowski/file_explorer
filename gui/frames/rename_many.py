import tkinter as tk
import tkinter.ttk as ttk


class RenameMany(tk.Toplevel):
    """
    Define naming parameters to change multiple file/dir names.

    Parameters
    ---------------
    root : Tk or any other container Frame
        ExplorerTree master window
    """

    def __init__(self, root):
        super().__init__(root)
        self.resizable(False, False)
        self.pref_var = tk.StringVar(self)
        self.name_var = tk.StringVar(self)
        self.suff_var = tk.StringVar(self)
        self.pref_lbl = ttk.Label(self, text="Prefix:")
        self.pref_lbl.grid(row=0, column=0)
        self.pref_ent = ttk.Entry(self, textvariable=self.pref_var)
        self.pref_ent.grid(row=0, column=1)
        self.name_lbl = ttk.Label(self, text="Name:")
        self.name_lbl.grid(row=0, column=2)
        self.name_ent = ttk.Entry(self, textvariable=self.name_var)
        self.name_ent.grid(row=0, column=3)
        self.suff_lbl = ttk.Label(self, text="Suffix:")
        self.suff_lbl.grid(row=0, column=4)
        self.suff_ent = ttk.Entry(self, textvariable=self.suff_var)
        self.suff_ent.grid(row=0, column=5)
        self.submit_btn = ttk.Button(self, text="Submit")
        self.submit_btn.grid(row=0, column=6)
