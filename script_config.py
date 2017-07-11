# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 21:11:43 2017

@author: Louis
"""
# Configuration setup for diffrent kind of extracted script file
# Basic format for every line is triad as follow:
#   //comment([char])
#   <(lang)(type)(id)>Text // Original
#   <(lang)(type)(id)>Text // Translation
# //: Begin of one line comment
# [char]: Optional text indicating characters who say the text
# lang: language code, such as en, ja
# type: One character to identify what kind of text it is, such as T, N, Z
# id: a string of number to indicate order of the tag
# Different section of the texts are combined by sep

# Different types of section of the text
types = {"N": "name", "T": "text", "Z": "other"}

# Seperator combine different sections
sep = "\n///================================================================================\n\n"