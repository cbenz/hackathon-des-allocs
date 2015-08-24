# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 21:51:31 2015

@author: alexis
"""

import os
import re
import pdb
import pandas as pd
from os.path import join


path_doc = 'D:/data/code_cnaf/'
path_wiki = 'C:/git/hackathon-des-allocs.wiki'

filename, decalage = 'wbcontac.csv', 0
file = os.path.join(path_doc, filename)

feuille = pd.read_csv(file, sep=';')

# TODO: faire une page pour un filename
feuille.fillna('', inplace=True)


def code_to_md_table(code):
    if code == '':
        return ''
        
    text = '| Code | Label | \n|----|----| \n'
    table = code[3:].replace('\r\n', '| \n|') 
    table = '|' + table.replace('\t', ' | ') + '|'
    text += table
    return text

for _, row in feuille.iterrows():
    print row
    path = os.path.join(path_wiki, row['nom_var'] + '.md') 
    

        
    
    text = row['Description'] + '\n' + '\n' 
    text += code_to_md_table(row['Codification'])
    
    f = open(path, 'w+')
    f.write(text)
