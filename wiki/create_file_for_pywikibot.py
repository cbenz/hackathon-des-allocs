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
    text = "{{-start-}} \n" + \
            "'''" + title + "'''"

    return text


def init_table():
    return """{| class=\"wikitable\"
! scope=\"col\" | Code
! scope=\"col\" | Label """


def fill_model(row, filename):
    # TODO: dict to translate format into type
    text = """
{{Variable
|nom= """ + row['nom_var_raccourci'] + """
|table= """ + filename + """
|type= """ + """
|format= """ + "\n }}"
    return text


def bas_de_page():
    return 'Cette page a été générée par un robot \n\n[[Category:CNAF]]\n{{-stop-}} \n \n'.decode('utf8')

def write_wiki_page(feuille, filename):
    text = ''
    feuille = feuille.iloc[:5, :]
    for _, row in feuille.iterrows():
        text_page = init_page(row['nom_var_raccourci']) + '\n'
        descr = row['Description']
        if descr[0] == ' ':
            descr = descr[1:]
        text_page += descr + '\n \n'
        text_page += fill_model(row, filename) + '\n \n'
        if row['Codification'] != '':
            text_page += init_table()+ '\n'
            text_page += code_to_wikitable(row['Codification']) + '\n \n'
        text_page += bas_de_page()
        text += text_page
    return text


def generate_wiki(filename):
    file = os.path.join(path_doc, filename)
    feuille = pd.read_csv(file + '.csv', sep=';', encoding='utf8')
    feuille = feuille[feuille.nom_var.notnull()]
    feuille.fillna('', inplace=True)
    text = write_wiki_page(feuille, filename)

    path = os.path.join(path_doc, filename + '_wiki.txt')
    f = open(path, 'w+')
    f.write(text.encode('utf8'))
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
    print path

# cd /git/pywikibot-core/scripts
#python pagefromfile.py -force -notitle -file:D:/data/code_cnaf/fi001000_wiki.txt
