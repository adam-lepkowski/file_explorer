from tkinter import ttk


class ObjectTransfer(ttk.Frame):
    """
    Container for file transfer buttons.

    Attributes
    ---------------
    copy_right_btn : ttk.Button
        copy object from left to right
    move_right_btn : ttk.Button
        move object from left to right
    copy_left_btn : ttk.Button
        copy object from right to left
    move_left_btn : ttk.Button
        move object from right to left
    """

    def __init__(self, root):
        super().__init__(root)
        self["padding"] = (0, 0, 15, 5)
        self.copy_right_btn = ttk.Button(self, text=">", style="ExpBar.TButton")
        self.copy_right_btn.grid(row=1, column=0)
        self.move_right_btn = ttk.Button(self, text=">>", style="ExpBar.TButton")
        self.move_right_btn.grid(row=2, column=0)
        self.copy_left_btn = ttk.Button(self, text="<", style="ExpBar.TButton")
        self.copy_left_btn.grid(row=3, column=0)
        self.move_left_btn = ttk.Button(self, text="<<", style="ExpBar.TButton")
        self.move_left_btn.grid(row=4, column=0)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(5, weight=1)
