# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 19:47:49 2017

@author: Louis
"""
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import re

def parseScripts(filepath):
    fp = open(filepath, encoding="UTF-8")
    parsed_orig = {"name": [],
                   "text": [],
                   "other": []}
    parsed_trans = {"name": [],
                   "text": [],
                   "other": []}
    
    char_arr = []
    
    tags = ["name", "text", "other"]
    
    orig_re = re.compile("<ja([TNZ])[0-9]+>")
    trans_re = re.compile("<ch([TNZ])[0-9]+>")
    text_comment_re = re.compile("//TEXT")
    char_re = re.compile("【(.+)】")
    
    for line in fp.readlines():
        line = line.strip()
        
        search = text_comment_re.search(line)
        if search:
            search = char_re.search(line)
            if search:
                char_arr.append(search.group(1))
            else:
                char_arr.append("")
            continue

        search = orig_re.search(line)
        if search:
            if search.group(1) == "N":    
                parsed_orig["name"].append(line[search.end():])
            elif search.group(1) == "T":
                parsed_orig["text"].append(line[search.end():])
            else:
                parsed_orig["other"].append(line[search.end():])
            continue
        
        search = trans_re.search(line)
        if search:
            if search.group(1) == "N":    
                parsed_trans["name"].append(line[search.end():])
            elif search.group(1) == "T":
                parsed_trans["text"].append(line[search.end():])
            else:
                parsed_trans["other"].append(line[search.end():])
    
    parsed_text = {}
    for tag in tags:
        if tag == "text":
            parsed_text[tag] = zip(char_arr, parsed_orig[tag], parsed_trans[tag])
        else:
            parsed_text[tag] = zip(parsed_orig[tag], parsed_trans[tag])
    
    return parsed_text

def openFile():
    fileName = filedialog.askopenfilename()
    texts = parseScripts(fileName)
    
    for tag in texts.keys():
        for row in treeviews[tag].get_children():
            treeviews[tag].delete(row)
        for line in texts[tag]:
            treeviews[tag].insert("", "end", values=line)
        
root = Tk()
root.title("Scripts Traslator")

root.option_add("*tearOff", False)\

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
    f = ttk.Frame(n)
    if tag == "text":
        treeview = ttk.Treeview(f, columns=("character", "original", "translation"))
    else:
        treeview = ttk.Treeview(f, columns=("original", "translation"))
    
    frames[tag] = f
    treeviews[tag] = treeview
    n.add(f, text = tag.capitalize())
    
    treeview.grid(column=0, row=0, sticky="WNSE")
    treeview["show"] = "headings"
    
    treeview.heading("original", text="Original")
    treeview.heading("translation", text="Translation")
    if tag == "text":
        treeview.heading("character", text="Char")
        treeview.column("character", width=10)
        
    scrollbar = Scrollbar(f, command=treeview.yview)
    scrollbar.grid(column=1, row=0, sticky="NS")
    treeview["yscrollcommand"] = scrollbar.set
    
    f.grid_columnconfigure(0, weight=1)
    f.grid_rowconfigure(0, weight=1)

root.mainloop()