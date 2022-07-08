# -*- coding: utf-8 -*-

"""Class Admin: Administration root window.

This is the entry point to the administration user interface application
of DCR.
"""
import tkinter
import tkinter.ttk


class Admin(tkinter.Tk):
    """Administration root window."""

    # -----------------------------------------------------------------------------
    # Class variables.
    # -----------------------------------------------------------------------------

    # -----------------------------------------------------------------------------
    # Object initializer.
    # -----------------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__()

        self.title("DCR Administration")
        self.columnconfigure(0, weight=1)

        tkinter.ttk.Label(self, text="DCR Administration", font=("TkDefaultFont", 16))

        self.status = tkinter.StringVar()
        tkinter.ttk.Label(self, textvariable=self.status).grid(sticky=(tkinter.W + tkinter.E), row=2, padx=10)


if __name__ == "__main__":
    admin = Admin()
    admin.mainloop()
