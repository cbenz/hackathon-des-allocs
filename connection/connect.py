# -*- coding: utf-8 -*-
"""
Created on Fri Oct 02 09:17:10 2015

@author: Alexis
"""


from sqlalchemy import create_engine
import psycopg2

# cfg
import Tools.config as config

##############
# PostgreSQL #
##############

table_name = 'GCA'
command = "SELECT * FROM public." + table_name

print "il faut bien préciser la commande pour ne pas charger l'integralité de la base"

# -- Connect
def connect_hackallocs(command):
    ''' connexion postgre à partir d'un tuple (schema, table) et renvoie un tuple (table, colnames)'''

    conn_string = "host= 10.20.7.252 dbname=cnaf user=cnaf password=cnaf"
    # print the connection string we will use to connect
    conn = psycopg2.connect(conn_string)
    del password, conn_string
    cur = conn.cursor()
    print("Connected!")
    cur.execute(command)
    colnames = [desc[0] for desc in cur.description]
    return (cur.fetchall(), colnames)