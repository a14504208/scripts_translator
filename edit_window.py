# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 23:33:15 2017

@author: Louis
"""
from tkinter import *
from win_mani import center

class EditWindow(Toplevel):
    def __init__(self, master, rowid, contents):
        """
        Set up the basic display, and save data necessary to submit the edit 
        back to scripts
        """
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
        
        self.trans_edit = Text(f, width=50)
        self.trans_edit.insert(1.0, contents["trans"])
        self.trans_edit.grid(column=1, row=1, sticky="NWSE")
        
        # Focus on the editing widget
        self.trans_edit.focus_set()
        
        btn_f = ttk.Frame(f, padding=(0, 5, 0, 5))
        btn_f.grid(column=1, row=2, sticky="E")
                
        OK_btn = ttk.Button(btn_f, text="OK(CTRL-Enter)", command=self.submitEdit)
        OK_btn.grid(column=0, row=0)
        
        cancel_btn = ttk.Button(btn_f, text="Cancel(ESC)", command=self.close)
        cancel_btn.grid(column=1, row=0)
        
        self.bind("<Control-Return>", self.submitEdit)
        self.bind("<Escape>", self.close)
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        f.rowconfigure(1, weight=1)
        f.columnconfigure(0, weight=1)
        f.columnconfigure(1, weight=1)
        
        center(self)
        self.focus_force()
        
    def submitEdit(self, event = None):
        trans = self.trans_edit.get(1.0, "end")
        self.master.editLine(self.__rowid, trans)
        self.destroy()
    
    def close(self, event = None):
        self.destroy()