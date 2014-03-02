# -*- coding: utf-8 -*-

# on recup le fichier interface
source = open("/etc/network/interfaces", "r")
source = source.readlines()

chaine = ""
result = chaine.replace("supplicant.conf", "nmotdepasserecrit")

# on l ecrit dans test.csv
dest = open("wifi.csv", "w")
for lignes in source:
    dest.write(lignes)
dest.close()

# to do : interface de config wifi raspberry