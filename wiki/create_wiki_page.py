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
feuille = feuille[feuille.nom_var.notnull()]

# Page de la table
def list_var_to_md_table(code):
    text = '| Variable | Nom var raccourci | \n|----|----| \n'
    table = '|' + code['Unnamed: 0'] + '|'
    text += table
    return text

text = feuille['Unnamed: 0'] + ' | [[' + \
        feuille['nom_var_raccourci'] + ']] |'
text = text.to_string()

text = '## ' + filename[:-4] + '\n Cette table contient les ' + \
        'variables suivantes : \n \n' + text

path = os.path.join(path_wiki, filename[:-4] + '.md')
f = open(path, 'w+')
f.write(text)
f.close()


# Page des variables
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
    text = row['Description'] + '\n' + '\n'
    text += code_to_md_table(row['Codification'])

    path = os.path.join(path_wiki, row['nom_var'] + '.md')
    print path
    f = open(path, 'w+')
    f.write(text)
    f.close()
