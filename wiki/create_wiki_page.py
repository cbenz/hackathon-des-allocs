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



# Page de la table
def list_var_to_md_table(code):
    text = '| Variable | Nom var raccourci | \n|----|----| \n'
    table = '|' + code['Unnamed: 0'] + '|'
    text += table
    return text

def write_page_table(filename, feuille):
    begin_table = '| Variable | Nom | \n|----|----| \n'

    values = '| ' + feuille['Unnamed: 0'].str.lstrip() + ' | [[' + \
             feuille['nom_var_raccourci'] + ']] |'
    values = '\n'.join(values.tolist())

    text = 'Cette table contient les ' + \
           'variables suivantes : \n \n' + begin_table + values

    path = os.path.join(path_wiki, filename + '.md')
    f = open(path, 'w+')
    f.write(text)
    f.close()



def code_to_md_table(code):
    if code == '':
        return ''

    text = '| Code | Label | \n|----|----| \n'
    table = code[3:].replace('\r\n', '| \n|')
    table = '|' + table.replace('\t', ' | ') + '|'
    text += table
    return text


def write_wiki_page(feuille):
    for _, row in feuille.iterrows():
        text = row['Description'] + '\n' + '\n'
        text += code_to_md_table(row['Codification'])

        path = os.path.join(path_wiki, row['nom_var_raccourci'] + '.md')
        print path
        f = open(path, 'w+')
        f.write(text)
        f.close()


def generate_wiki(filename):
    file = os.path.join(path_doc, filename)
    feuille = pd.read_csv(file + '.csv', sep=';')
    feuille = feuille[feuille.nom_var.notnull()]
    feuille.fillna('', inplace=True)

    write_page_table(filename, feuille)
    write_wiki_page(feuille)


if __name__ == '__main__':
    for filename in ['wbcontac', 'glsdp010', 'fi001000', 'allaah', 'allpaje',
                     'glgc0020']:
        generate_wiki(filename)


