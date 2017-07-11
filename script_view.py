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
        
        # Display treeview
        self.displayTreeview()
        
        # Display scripts
        self.displayScripts()
    
    def bindTreeview(self):
        self.__tree.bind("<Double Button-1>", self.doubleClickToEdit)
    
    def displayTreeview(self):
        """
        Put treeview and scrollbar on the frame
        """
        self.__tree.grid(column=0, row=0, sticky="WNSE")
        self.__tree["show"] = "headings"
        
        self.__tree.heading("char", text="Character")
        self.__tree.heading("orig", text="Original")
        self.__tree.heading("trans", text="Translation")
        
        self.__tree.column("char", width=100, stretch=False)
        
        # Set scrollbar
        scrollbar = ttk.Scrollbar(self, command=self.__tree.yview)
        self.__tree["yscrollcommand"] = scrollbar.set
        scrollbar.grid(column=1, row=0, sticky="NS")
        
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
            
            self.__tree.insert("", "end", iid=iid, values=(char, orig, trans))
    
    def doubleClickToEdit(self, event):
        """
        Double click on the row to popup a window for editing the line
        """
        # Get the contents in the row
        rowid = self.__tree.identify_row(event.y)
        contents = self.__tree.set(rowid)
        
        EditWindow(self, rowid, contents)
        
        #edit_w = Toplevel(self)
        

    def editLine(self):
        pass
    
    def outputScripts(self):
        triad_arr = []
        
        for iid in sorted(self.__scripts.keys()):
            comment = self.__scripts[iid][0]
            orig_line = "<ja{0}>{1}".format(iid, self.__scripts[iid][1])
            trans_line = "<ch{0}>{1}".format(iid, self.__scripts[iid][2])
            triad = "\n".join([comment, orig_line, trans_line]) + "\n"
            triad_arr.append(triad)
        
        return "\n".join(triad_arr)

#def doubleClickToEdit(event):
#    rowid = treeviews["text"].identify_row(event.y)
#    colid = treeviews["text"].identify_column(event.x)
#    
#    x, y, width, height = treeviews["text"].bbox(rowid, colid)
#    
#    text = treeviews["text"].set(rowid, colid)
#    
#    entry = Entry(treeviews["text"])
#    entry.place(x = x, y = y, width = width, height = height)
#    entry.insert(0, text)
#    entry.focus_set()
#    entry.select_range(0, "end")
#    entry.bind("<Return>", lambda e: entry.destroy())