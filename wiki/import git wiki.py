# -*- coding: utf-8 -*-
"""
Created on Mon Sep 07 20:23:03 2015

@author: alexis
"""

import os
import codecs

path_wiki = 'C:\git\DAMIR.wiki'

files = os.listdir(path_wiki)
files = [x for x in files if x[-3:] == '.md']
files.remove('_Sidebar.md')


def init_page(title):
    text = "{{-start-}} \n" + \
            "'''" + title + "'''" + "\n\n" 
    return text.decode('utf8')


def bas_de_page():
    text = '\n \nCette page a été générée par un robot \n\n[[Category:CNAMTS]]\n{{-stop-}} \n \n'
    return text.decode('utf8')


def fill_model(name):
    # TODO: dict to translate format into type
    text = """
{{Variable
|nom= """ + name + """
|table= OpenDamir
|type= """ + """
|format=
}}

"""
    return text.decode('utf8')

count = 0
all_pages = ''
total_text = ''
for page in files:
    path = os.path.join(path_wiki, page)
    with codecs.open(path, encoding='utf8') as f:
        text = f.read()
        if '| ' in text:
            count +=1
            import pdb; pdb.set_trace()

    name = page[:-3].decode('cp1252').encode('utf8')
    total_text += init_page(name) + fill_model(name) + text + bas_de_page()
    
    all_pages += '[[' + name + ']]'

print count


file_to_wiki = os.path.join(path_wiki, 'damir_wiki.txt')
with open(file_to_wiki, 'w+') as f:
    f.write(total_text.encode('utf8'))

file_to_delete = os.path.join(path_wiki, 'damir_pages.txt')
with open(file_to_delete, 'w+') as f:
    f.write(all_pages)




