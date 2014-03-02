# -*- coding: utf-8 -*-

import os.path
import sqlite3
import urllib


def listdir(path):
# lister l'arbo d'un rep (rep / ss rep et fichier de tout le monde)
# remplacer DOSSIER, FICHIER par des class CSS

    #fichier=[]

    for root, dirs, files in os.walk(path):

        for h in files:
            # on récupère l'indice du dernier signe "/"
            cheminset = root.rfind('/')
            # on découpe la fin de "path" depuis le dernier indice "/" récupéré
            chemin = root[cheminset::]
            print chemin

            if h.endswith(".mp3"):
                #fichier.append("FICHIER "+os.path.join(root, j))
                print "FICHIER : "+h

    #print fichier

# ----------------------------------------------------
#   RECUPERATION LISTE RADIO DEPUIS FICHIER SUR gromfiot.free.fr
# ----------------------------------------------------


def recup_liste():
    """ recup du fichier "radios.txt" sur gromfiot.free.fr puis formatage pour l'inserer dans la base"""
    #recuperation
    sock = urllib.urlopen("http://gromfiot.free.fr/radios.txt")
    
    #formatage (on crere une liste)
    radios = []

    for i in sock:
        # alors pourquoi je dois faire un fichier txt en sautant une ligne sur deux...?
        # radio1 = sock.readline().rstrip('\n')
        ligne = str(i)
        radio = tuple(ligne.split(','))
        radios.append(radio)
    
    #insertion
    conn = sqlite3.connect("mydatabase.db")   # or use :memory: to put it in RAM
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO media VALUES (NOT NULL,?,?,?)", radios)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    listdir("/Users/fiot/Documents/GIT/MUSIC_PLAYER/app/static/uploads")