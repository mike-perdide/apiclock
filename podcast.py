# -*- coding: utf-8 -*-

"""// Script d'une WebApp de smart radio reveil pour Raspberry Pi
////////////////////////////////////////////////////////////////////////
Récupération depuis l'URL RSS (XML) d'un podcast puis parsing (Beautifulsoup)
et téléchargement

Définir endroit de téléchargement / nom / playlist
+ rajout insertion BDD

"""

import urllib2
from bs4 import BeautifulSoup
import os
import sqlite3

# url = 'http://radiofrance-podcast.net/podcast09/rss_10504.xml'
url = 'http://www.1001podcast.com/podcast/BFM/channel17/BFMchannel17.xml'
page = urllib2.urlopen(url)
soup = BeautifulSoup(page)
dossier = './podcast'

# on récupère les 4 premiers liens dans le XML ayant pour tag enclosure
# playlists = soup.find_all("enclosure", limit=1)

# on récupère le premier (param limit) lien dans le XML ayant pour tag guid
playlists = soup.find_all("guid", limit=1)

#ramener la date + titre +img du podcast ?
# titre_podcast = soup.find_all("title", limit=2)
# date_podcast = soup.find_all("pubDate", limit=2)

# le lien de l'img est dans la balise <url> sous-balise d'<image> sous-balise de <channel>
# img_podcast = soup.find_all("url", limit=2)

def ajout_podcast():
    i=0
    
    while i<len(playlists):
        # on récupère le 1er contenu de l'élément
        lien = playlists[i].contents
        # on supprime les crochets et autres
        output = str(lien)[3:-2]
    
        # on définit le nom de sortie (en ne gardant que la fin de l'url
        file_name = output.split('/')[-1]
        
        # on rajoute le nom du dossier PODCAST
        file_url = dossier+'/'+file_name
    
        # on vérifie que le fichier n'existe pas déjà
        if not os.path.isfile(file_name):
    
            u = urllib2.urlopen(output)
            f = open(file_name, 'wb')
            meta = u.info()
            file_size = int(meta.getheaders("Content-Length")[0])
            print "Downloading: %s Bytes: %s" % (file_name, file_size)
            
            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break
                
                file_size_dl += len(buffer)
                f.write(buffer)
                status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                status = status + chr(8)*(len(status)+1)
                print status,
                
            f.close()
            
            # on insert le tout dans la bdd
            conn = sqlite3.connect("mydatabase.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO media (type, title, urlmedia) VALUES (?, ?, ?)", ('podcast', file_name, file_url))
            conn.commit()
            
        else :
            print "Fichier déjà téléchargé"
    
        i+=1
