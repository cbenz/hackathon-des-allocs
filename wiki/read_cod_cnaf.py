# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 09:54:04 2015

@author: Alexis
"""

import os
import pdb
import pandas as pd

path_data = 'D:/data/code_cnaf/'

def read_txt(filename):
    file = os.path.join(path_data, filename + '.txt')
    doc = open(file)
    text = doc.read()
    return text.decode('cp1252').encode('utf8')


def _bloc_sous_groupe(bloc):
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


def _get_info(ligne):
    dico = dict()
    mots_cles = ['nature', 'format', 'longueur', 'précision']
    mot_ = 'nom_var'
    for mot in mots_cles:
        mot_total =  '\t' + mot + ' : '
        if mot_total in ligne:
            split_mot = ligne.split(mot_total)
            dico[mot_] = split_mot[0]
            mot_ = mot
            ligne = split_mot[1]
    dico[mot_] = ligne

    # travail sur nom_var pour delier deux truc
    en_entier = dico['nom_var']
    en_deux = en_entier.split('\t')
    dico['nom_var_raccourci'] = en_deux[1][1:-1]
    dico['nom_var'] = en_deux[0]
    return dico

def dict_from_txt(filename):
    dic_general = dict()

    text = read_txt(filename)
    text_par_bloc = text.split('\n\n')

    for bloc in text_par_bloc:
    #    print bloc[:20]
        if 'Sous groupe logique ' in bloc[:21]:
            _bloc_sous_groupe(bloc)
            #TODO: faire quelque chose non ?
        elif bloc[:16] == '\nGroupe logique ':
            pass
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
                        text = split_mot[0][0:]
                        if text[0] == '\n':
                            text = text[1:]
                        premiere_ligne = text.split('\n')[0]
                        valeurs = _get_info(premiere_ligne)
                        nom = text.split('\n')[1]
                        assert nom[-1] == '\t'
                        nom = nom[:-1]
                    else:
                        valeurs[mot_en_cours] = split_mot[0]
                    mot_en_cours = mot
                    bloc = split_mot[1]

            valeurs[mot_en_cours] = bloc
            dic_general[nom] = valeurs
    return dic_general


## on crée une table avec les valuers
def csv_from_txt(filename):
    dic_general = dict_from_txt(filename)
    table = pd.DataFrame(dic_general)
    table = table.T
    path_csv = os.path.join(path_data, filename + '.csv')
    table.to_csv(path_csv, sep=';', quotchar= '\"')

if __name__ == '__main__':
    for filename in ['wbcontac', 'glsdp010', 'fi001000', 'allaah', 'allpaje',
                     'glgc0020']:
        print filename
        csv_from_txt(filename)

