#!/usr/bin/env python
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


def code_to_wikitable(code):
    if code == '':
        return ''
    table = code[3:].replace('\r\n', '\n|- \n|')
    table = '|- \n|' + table.replace('\t', ' || ') + '\n'
    text = table + '|}'
    return text


def init_page(title):
    text = "xxxx \n" + \
            "''' " + title + "'''"

    return text
    
def init_table():
    return """{| class=\"wikitable\" 
! scope=\"col\" | Code 
! scope=\"col\" | Label """   

    
def write_wiki_page(feuille):
    text = ''
    for _, row in feuille.iterrows():
        text_page = init_page(row['nom_var_raccourci']) + '\n'
        text_page += row['Description'] + '\n \n'
        if row['Codification'] != '':
            text_page += init_table()+ '\n'
            text_page += code_to_wikitable(row['Codification']) + '\n \n'
        text_page += 'yyyy \n \n'
        text += text_page
    return text


def generate_wiki(filename):
    file = os.path.join(path_doc, filename)
    feuille = pd.read_csv(file + '.csv', sep=';')
    feuille = feuille[feuille.nom_var.notnull()]
    feuille.fillna('', inplace=True)
    text = write_wiki_page(feuille)
    
    path = os.path.join(path_doc, filename + '_wiki.txt')
    f = open(path, 'w+')
    f.write(text.decode('cp1250').encode('utf-8'))
    f.close()
    



#xxxx
#'''Nom de la page'''
#Texte ici
#
#yyyy
#xxxx
#'''Nom d'une autre page'''
#Un autre texte
#yyyy

if __name__ == '__main__':
    for filename in [ #'wbcontac', 'glsdp010', 
                     'fi001000', 
                     #'allaah', 'allpaje','glgc0020'
                     ]:
        generate_wiki(filename)
    
    path = os.path.join(path_doc, filename + '_wiki.txt')
    from scripts import pagefromfile

    titleStartMarker = "'''"
    titleEndMarker = "'''"
    options = {}
    include = False
    notitle = False
    reader = pagefromfile.PageFromFileReader(path, 'xxxx', 'yyyy',
                                titleStartMarker, titleEndMarker, include,
                                notitle)
    bot = pagefromfile.PageFromFileRobot(reader, **options)
    bot.run()

