# -*- coding: utf-8 -*-

"""// Script d'une WebApp de smart radio reveil pour Raspberry Pi
////////////////////////////////////////////////////////////////////////
Création de la BDD en SQLite (fichier : mydatabase.db) à la première connexion uniquement """

import sqlite3
from liste_fichier import recup_liste
from jouer_mpd import create_MPDplaylist

# ----------------------------------------------------
#   DATABASE : CREATION / INSERTION / AFFICHAGE
#   http://www.blog.pythonlibrary.org/2012/07/18/python-a-simple-step-by-step-sqlite-tutorial/
# ----------------------------------------------------


def creation_bdb():
    # verification de l'existence du fichier mydatabase et...
    try:
        open("mydatabase.db")

    #... si non --> creation (puis insertion exemple) / commit et close du fichier
    except IOError:
        fichier = open("mydatabase.db", "w")
        conn = sqlite3.connect("mydatabase.db")   # or use :memory: to put it in RAM
        cursor = conn.cursor()
        # creation des tables (à éffectuer une seule fois)

        cursor.execute("""CREATE TABLE media
                            (idmedia integer primary key autoincrement ,
                            type varchar(50),
                            title varchar(50),
                            urlmedia text)
                         """)

        cursor.execute("""CREATE TABLE user
                            (iduser integer primary key autoincrement ,
                            nameuser varchar(50),
                            prenom varchar(50),
                            mail varchar(50),
                            passwd varchar(50),
                            role text,
                            lang text,
                            perso text,
                            googlec varchar(50),
                            twitterc varchar(50))
                         """)

        cursor.execute("""CREATE TABLE alarm
                            (idalarm integer primary key autoincrement ,
                            namealarm varchar(50),
                            startdate date,
                            duration date,
                            frequence text,
                            days text,
                            mediaid INTEGER,
                            userid INTEGER,
                            FOREIGN KEY(mediaid) REFERENCES media(idmedia),
                            FOREIGN KEY(userid) REFERENCES user(iduser))
                         """)

        cursor.execute("""CREATE TABLE playlist
                            (idplaylist integer primary key autoincrement ,
                            nameplaylist varchar(50),
                            mediaid2 INTEGER,
                            userid2 INTEGER,
                            FOREIGN KEY(mediaid2) REFERENCES media(idmedia),
                            FOREIGN KEY(userid2) REFERENCES user(iduser))
                         """)
        # doit on préciser un champ pour L'insertion de l'ID comme cle definit en auto increment ?
        cursor.execute("INSERT INTO user VALUES("
                       "1,"
                       "'fiot', "
                       "'jerome', "
                       "'j_fiot@hotmail.com', "
                       "'apiclock', "
                       "'admin', "
                       "'fr', "
                       "'#blue', "
                       "'no', "
                       "'grominet')")
        # on met a jour tout ca sur la base
        conn.commit()
        fichier.close()
        # on recupere le fichier radio, parse, insere dans la base
        recup_liste()
        # on recupere le fichier radio, parse, insere dans la base
        create_MPDplaylist()
    except:
        print "Unexpected error:", sys.exc_info()[0]


def show_media(type_media):
    # pourquoi marche pas : def show_base(table)
    conn = sqlite3.connect("mydatabase.db")
    #conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    typem = (type_media,)
    sql = "SELECT * FROM media WHERE type=?"
    cursor.execute(sql, typem)
    conn.commit()
    return cursor.fetchall()


def delete_media(idmedia):
    """Suppression d'un enregistrement par l'argment idmedia"""
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    typem = (idmedia,)
    sql = "DELETE FROM media WHERE idmedia=?"
    cursor.execute(sql, typem)
    conn.commit()


def add_media(typemedia, title, urlmedia):
    """ajout d'un enregistrement"""
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO media ("
                   "idmedia, "
                   "type, "
                   "title, "
                   "urlmedia) "
                   "VALUES (?,?,?,?)",
                   ('10', typemedia, title, urlmedia))
    conn.commit()


def update_media(idmedia, typemedia, title, urlmedia):
    """mise à jour de la table media avec les arguments correspond. aux lignes"""
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    liste_arguments = ["typemedia", "title", "urlmedia"]
    sql = "UPDATE media (type, title, urlmedia) VALUES (?,?,?) WHERE idmedia="+idmedia+""
    for item in liste_arguments:
        cursor.execute(sql, item)
    conn.commit()