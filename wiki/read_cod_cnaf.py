# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 09:54:04 2015

@author: Alexis
"""

import os
import re
import pdb
from os.path import join


path = 'D:/data/code_cnaf/'

filename, decalage = 'fileas.txt', 1
filename, decalage = 'wbcontac.txt', 0

file = os.path.join(path, filename)


doc = open(file)
text = doc.read()

text_par_bloc = text.split('\n\n')


def bloc_sous_groupe(bloc):
    bloc = bloc[1:]
    bloc_par_case = bloc.split('\n')
    name = bloc_par_case[0].split('\t: ')
    assert bloc_par_case[1][:6] == 'Table '
    descriptif = ''
    precision = ''
    if len(bloc_par_case) > 2:
        descriptif =  bloc_par_case[2]
    if len(bloc_par_case) > 3:
        precision = bloc_par_case[3]
    if len(bloc_par_case) > 4:
            print bloc_par_case
            pdb.set_trace()
    return name, descriptif, precision


def get_info(bloc):
    print bloc
    dico = dict()
    mots_cles = ['nature', 'format', 'longueur', 'précision']
    mot_ = 'nom_var'
    for mot in mots_cles: 
        mot_total =  '\t' + mot + ' : '
        if mot_total in bloc:
            split_mot = bloc.split(mot_total)
            dico[mot_] = split_mot[0]
            mot_ = mot
            bloc = split_mot[1]
    dico[mot_] = bloc

    #travail sur nom_var pour delier deux truc
    en_entier = dico['nom_var']
    en_deux = en_entier.split('\t')
    dico['nom_var_raccourci'] =  en_deux[1][1:-1]
    dico['nom_var'] = en_deux[0]
    return dico

## split les \n\n
#dico = dict()
dic_general = dict()
for bloc in text_par_bloc:
#    print bloc[:20]
    if bloc[:21] == '\nSous groupe logique ':
        bloc_sous_groupe(bloc)
        #TODO: faire quelque chose non ? 
    else:
        bloc = bloc[:]
        valeurs = dict()
        mots_cles = ['Description', 'Elaboration', 'Commentaire',
                     'Codification']
        mots_suivants = mots_cles[:]
        mot_en_cours = 'Debut'
        
        for mot in mots_cles:
            
            mot_total = '\n' + mot + ' :'
            if mot_total in bloc:
                split_mot = bloc.split(mot_total)
                
                for test in mots_cles:
                    if test != mot:
                        assert test not in split_mot[0]
                
                if mot_en_cours == 'Debut':
                    text = split_mot[0][decalage:]
#                    pdb.set_trace()
                    premiere_ligne = text.split('\n')[0]
                    valeurs = get_info(premiere_ligne)
                    nom = text.split('\n')[1]
                    assert nom[-1] == '\t'
                    nom = nom[:-1]
                else: 
                    valeurs[mot_en_cours] = split_mot[0]
                mot_en_cours = mot
                bloc = split_mot[1]
                
        valeurs[mot_en_cours] = bloc
        dic_general[nom] = valeurs


## on crée une table avec les valuers
import pandas as pd
table = pd.DataFrame(dic_general)
table = table.T

table.to_csv(file[:-3] + 'csv', sep=';', quotchar= '\"')

## étude de l'élaboration
col = table.Elaboration
col.fillna('', inplace=True)
annexe = col.str.contains('Annexe')

col = col[~annexe]

        