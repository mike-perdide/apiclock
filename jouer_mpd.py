# -*- coding: utf-8 -*-

from mpd import MPDClient
import os.path
import sqlite3


def play_MPD(path):
    """   """
    client = MPDClient()               # create client object
    client.timeout = 10                # network timeout in seconds (floats allowed), default: None
    client.idletimeout = None
    client.connect("localhost", 6600)  # connect to localhost:6600

    MPDClient.add(path)
    client.play(0)
    print MPDClient.playlistinfo()

    #client.close()                     # send the close command
    #client.disconnect()                # disconnect from the server
    
    
def create_MPDplaylist():
# cree un fichier radioplaylist dans le rep. (A CHANGER) /var/lib/mpd/playlists/ depuis la recup du fichier 
    fichier = open("/usr/local/Cellar/mpd/0.17.5/playlists/radios.m3u", "w")
    
    conn = sqlite3.connect("mydatabase.db")
    #conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql = "SELECT * FROM media"
    cursor.execute(sql)
    radio = cursor.fetchall()
    
    #for row in radio:
    #    fichier.write(row[0])
    #fichier.close()
    
# afficher les infos d'un stream
# mp3 http://stackoverflow.com/questions/6613587/reading-mp3-metadata-from-a-radio-stream-in-python
# jouerMPD("/Users/fiot/Documents/GIT/MUSIC_PLAYER/app/static/uploads/test")