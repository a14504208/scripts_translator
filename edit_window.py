# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 23:33:15 2017

@author: Louis
"""
from tkinter import *
from win_mani import center

class EditWindow(Toplevel):
    def __init__(self, master, rowid, contents):
        Toplevel.__init__(self, master)
        
        self.__rowid = rowid
        
        f = ttk.Frame(self, padding=(5, 5, 12, 0))
        f.grid(column=0, row=0, sticky="NWSE")
        
        char_l = ttk.Label(f, text=contents["char"]+":", font=("",16))
        char_l.grid(column=0, row=0, sticky="W")
        
        orig_display = Text(f, width=50)
        orig_display.insert(1.0, contents["orig"])
        orig_display["state"] = "disabled"
        orig_display.grid(column=0, row=1, sticky="NWSE")
        
        trans_edit = Text(f, width=50)
        trans_edit.insert(1.0, contents["trans"])
        trans_edit.grid(column=1, row=1, sticky="NWSE")
        
        btn_f = ttk.Frame(f, padding=(0, 5, 0, 5))
        btn_f.grid(column=1, row=2, sticky="E")
                
        OK_btn = ttk.Button(btn_f, text="OK")
        OK_btn.grid(column=0, row=0)
        
        cancel_btn = ttk.Button(btn_f, text="Cancel", command=self.destroy)
        cancel_btn.grid(column=1, row=0)
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        f.rowconfigure(1, weight=1)
        f.columnconfigure(0, weight=1)
        f.columnconfigure(1, weight=1)
        
        center(self)
    