# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 15:49:41 2017

@author: Louis
"""
from tkinter import *
from tkinter import ttk

class ScriptView(ttk.Frame):
    def __init__(self, master, tag, scripts = None):
        """
        Scripts take form as {iid: [comment, orig, trans]}
        """
        
        ttk.Frame(self, master)
        self.tag = tag
        self.__scripts = scripts
        
        # Bind treeview to the self frame
        self.__tree = ttk.Treeview(self, columns = ("orig", "trans"))
        
        # Bind events to treeview
        self.bindTreeview()
        
        # Display treeview
        self.displayTreeview()
        
        # Display scripts
        self.displayScripts()
        
        # Adjust to resize
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
    
    def bindTreeview(self):
        pass
    
    def displayTreeview(self):
        """
        Put treeview and scrollbar on the frame
        """
        self.__tree.grid(column=0, row=0, sticky="WNSE")
        self.__tree["show"] = "headings"
        
        self.__tree.heading("orig", text="Original")
        self.__tree.heading("trans", text="Translation")
        
        # Set scrollbar
        scrollbar = ttk.Scrollbar(self, command=self.__tree.yview)
        self.__tree["yscrollcommand"] = scrollbar.set
        scrollbar.grid(column=1, row=0, sticky="NS")
        
    def displayScripts(self):
        """
        Display scripts in the treeview
        """
        if not self.__scripts:
            return
        
        for iid in self.__scripts.keys():
            comment, orig, trans = self.__scripts[iid]
            self.__tree.insert("", "end", iid=iid, values=(orig, trans))
    
    def doubleClickToEdit(self):
        pass
    
    def editScript(self):
        pass
    
    def outputScripts(self):
        pass