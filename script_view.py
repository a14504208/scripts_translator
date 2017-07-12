# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 15:49:41 2017

@author: Louis
"""
from tkinter import *
from tkinter import ttk

import re

from edit_window import EditWindow

class ScriptView(ttk.Frame):
    def __init__(self, master, scripts):
        """
        Scripts take form as {iid: [comment, orig, trans]}
        """
       
        ttk.Frame.__init__(self, master)
        self.__scripts = scripts
        
        # Bind treeview to the self frame
        self.__tree = ttk.Treeview(self, columns = ("char", "orig", "trans"))
        
        # Bind events to treeview
        self.bindTreeview()
        
        # Display treeview and associated widget
        self.displayWidgets()
        
        # Display scripts
        self.displayScripts()
    
    def bindTreeview(self):
        self.__tree.bind("<Double Button-1>", self.openEditWindow)
        self.__tree.bind("<Return>", self.openEditWindow)
    
    def displayWidgets(self):
        """
        Put widget on the frame
        """
        # Setup treeview
        self.__tree.grid(column=0, row=0, sticky="WNSE")
        self.__tree["show"] = "headings"
        
        self.__tree.heading("char", text="Character")
        self.__tree.heading("orig", text="Original")
        self.__tree.heading("trans", text="Translation")
        
        self.__tree.column("char", width=100, stretch=False)
        
        # Setup different color for state of translation
        self.__tree.tag_configure("translated", background="#7eff7e")
        self.__tree.tag_configure("untranslated", background="#ff9e9e")
        
        # Setup scrollbar
        scrollbar = ttk.Scrollbar(self, command=self.__tree.yview)
        self.__tree["yscrollcommand"] = scrollbar.set
        scrollbar.grid(column=1, row=0, sticky="NS")
        
        # Setup popup menu to change state of translation
        menu = Menu(self.__tree, tearoff = 0)
        
        # Add menu command
        menu.add_command(label="Set As Translated", command=self.setAsTranslated)
        menu.add_command(label="Set As Untranslated", command=self.setAsUntranslated)
        
        # Bind to the treeview
        self.__tree.bind("<Button-3>", lambda e: menu.post(e.x_root, e.y_root))
        
        # Adjust to resize
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
    def displayScripts(self):
        """
        Display scripts in the treeview
        """      
        for iid in sorted(self.__scripts.keys()):            
            char_re = re.compile("【(.+)】")
            
            comment, orig, trans = self.__scripts[iid]
            
            char_match = char_re.search(comment)
            if char_match:
                char = char_match.group(1)
            else:
                char = ""
            
            state = "translated" if comment.endswith("*") else "untranslated"
            
            self.__tree.insert("", "end", iid=iid, values=(char, orig, trans),
                               tags = state)
    def openEditWindow(self, event):
        """
        Popup a window for editing the line
        """
        # Get the contents in the row
        rowid = self.__tree.focus()
        contents = self.__tree.set(rowid)
        
        EditWindow(self, rowid, contents)
                

    def editLine(self, rowid, trans):
        trans = trans.rstrip()
        self.__scripts[rowid][2] = trans
        self.__tree.set(rowid, "trans", trans)
        
        # Change the underlying tag
        if not self.__scripts[rowid][0].endswith("*"):
            self.__scripts[rowid][0] += "*"
            self.__tree.item(rowid, tags="translated")
        
        self.update()
    
    def setAsTranslated(self):
        rowids = self.__tree.selection()
        
        for rowid in rowids:
            if not self.__scripts[rowid][0].endswith("*"):
                self.__scripts[rowid][0] += "*"
                self.__tree.item(rowid, tags="translated")
        
        self.update()

    def setAsUntranslated(self):
        rowids = self.__tree.selection()
        
        for rowid in rowids:
            if self.__scripts[rowid][0].endswith("*"):
                self.__scripts[rowid] = self.__scripts[rowid][:-1]
                self.__tree.item(rowid, tags="untranslated")
                
        self.update()

    
    def outputScripts(self):
        triad_arr = []
        
        for iid in sorted(self.__scripts.keys()):
            comment = self.__scripts[iid][0]
            orig_line = "<ja{0}>{1}".format(iid, self.__scripts[iid][1])
            trans_line = "<ch{0}>{1}".format(iid, self.__scripts[iid][2])
            triad = "\n".join([comment, orig_line, trans_line]) + "\n"
            triad_arr.append(triad)
        
        return "\n".join(triad_arr)
    
    def update(self):
        pass