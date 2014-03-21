# -*- coding: utf-8 -*-

# ----------------------------------------------------
#   IMPORTS ET CONFIGURATION
# ----------------------------------------------------



# ----------------------------------------------------
#   CLASS
# ----------------------------------------------------

class Alarme(object):
    """L'alarme """

    __tablename__ = 'reveil'
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    jours = Column(Date)
    heuredebut = Column(Date)
    heurefin = Column(Date)
    volume = Column(Integer)
    idmedia = Column(Integer, ForeignKey("media.id"))
    iduser = Column(Integer, ForeignKey("user.id"))

    def __init__(self, nom, jours, heuredebut, heurefin, volume, idmedia, iduser):
        self.nom = nom
        self.jours = jours
        self.heuredebut = heuredebut
        self.heurefin = heurefin
        self.volume = volume