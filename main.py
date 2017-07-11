# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 19:47:49 2017

@author: Louis
"""
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from script_view import ScriptView

import re

def parseScripts(filepath):
    fp = open(filepath, encoding="UTF-8")
    
    iid_re = re.compile("<.+(([NTZ])[0-9]+)>")
    
    tags = {"N": "name", "T": "text", "Z": "other"}
    
    # In the form of {iid: [comment, orig, trans]}    
    parsed = {"name": {},
              "text": {},
              "other": {}}
    
    # Expect file in the triad form: comment begin with //, orig followed by
    # trans
    line = fp.readline()
    while (line != ""):
        # Begin of the triad
        if (line.startswith("///")):
            pass
        elif (line.startswith("//")):
            comment = line.rstrip()
            
            orig_line = fp.readline()
            head = iid_re.search(orig_line)
            iid = head.group(1)
            tag = tags[head.group(2)]
            orig = orig_line[head.end():].rstrip()
            
            trans_line = fp.readline()
            head = iid_re.search(trans_line)
            trans = trans_line[head.end():].rstrip()
            
            parsed[tag][iid] = (comment, orig, trans)
            
        line = fp.readline()
    
    return parsed

def openFile():
    fileName = filedialog.askopenfilename()
    parsed = parseScripts(fileName)
    
    for tab in n.tabs():
        n.forget(tab)
    
    for tag in parsed.keys():
        f = ScriptView(n, tag, parsed[tag])
        n.add(f, text = tag.capitalize())
    
def doubleClickToEdit(event):
    rowid = treeviews["text"].identify_row(event.y)
    colid = treeviews["text"].identify_column(event.x)
    
    x, y, width, height = treeviews["text"].bbox(rowid, colid)
    
    text = treeviews["text"].set(rowid, colid)
    
    entry = Entry(treeviews["text"])
    entry.place(x = x, y = y, width = width, height = height)
    entry.insert(0, text)
    entry.focus_set()
    entry.select_range(0, "end")
    entry.bind("<Return>", lambda e: entry.destroy())

root = Tk()
root.title("Scripts Traslator")

root.option_add("*tearOff", False)

# Add menubar
menubar = Menu(root)
root["menu"] = menubar

menu_file = Menu(menubar)
menubar.add_cascade(menu=menu_file, label = "File")

menu_file.add_command(label = "Open...", command = openFile)

tags = ["name", "text", "other"]

# Create and config the outer frame
n = ttk.Notebook(root, padding=(5, 5, 12, 0))
n.grid(column=0, row=0, sticky="NSWE")

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

frames = {}
treeviews = {}

for tag in tags:
    f = ScriptView(n, tag)
    n.add(f, text = tag.capitalize())

root.mainloop()