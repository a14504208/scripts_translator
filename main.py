# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 19:47:49 2017

@author: Louis
"""
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from script_view import ScriptView

import script_config

import re

fileName = ""

def parseScripts(filepath):
    fp = open(filepath, encoding="UTF-8")
    types = script_config.types

    iid_re = re.compile("<.+(([{0}])[0-9]+)>".format("".join(types.keys())))
    
    # In the form of {type: {iid: [comment, orig, trans]}}
    parsed = {tag: {} for tag in types.values()}
    
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
            tag = types[head.group(2)]
            orig = orig_line[head.end():].rstrip()
            
            trans_line = fp.readline()
            head = iid_re.search(trans_line)
            trans = trans_line[head.end():].rstrip()
            
            parsed[tag][iid] = (comment, orig, trans)
            
        line = fp.readline()
    
    fp.close()
    
    return parsed

def setPanels(n, scripts):
    """
    Delete existing tabs in the notebook n, then display tabs to n, with keys 
    of scripts as the tag of the tab
    """
    for tab in n.tabs():
        n.forget(tab)
        
    for tag in scripts.keys():
        panel = ScriptView(n, scripts[tag])
        n.add(panel, text = tag.capitalize())

def openFile():
    global fileName
    fileName = filedialog.askopenfilename()
    scripts = parseScripts(fileName)
        
    setPanels(n, scripts)

def saveFile():
    sep = script_config.sep
    script_arr = []
    
    fp = open(fileName + ".tmp", "w", encoding="UTF-8")
    
    for tab_name in n.tabs():        
        script_arr.append(n.children[tab_name.split(".")[2]].outputScripts())
     
    fp.write(sep.join(script_arr))
    
    fp.close()

if __name__ == "__main__":
    root = Tk()
    root.title("Scripts Traslator")
    
    root.option_add("*tearOff", False)
    
    # Add menubar
    menubar = Menu(root)
    root["menu"] = menubar
    
    menu_file = Menu(menubar)
    menubar.add_cascade(menu=menu_file, label = "File")
    
    # Add open file button
    menu_file.add_command(label = "Open...", command = openFile)
    # Add save file button
    menu_file.add_command(label = "Save file", command = saveFile)
    
    # Create, display and config the notebook
    # n is global variable used by other function
    n = ttk.Notebook(root, padding=(5, 5, 12, 0))
    n.grid(column=0, row=0, sticky="NSWE")
    
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
        
    # Temporary line, replaced by reading temp file in the future
    openFile()
    
    
    
    root.mainloop()
    