# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bdd import Media

POPULATION = (
    (Media, ('RTL', 'radio', 'www.rtl.fr')),
    (Media, ('Europe1', 'radio', 'www.rtl.fr')),
    (Media, ('Nova', 'radio', 'www.rtl.fr')),
    (Media, ('Inter', 'radio', 'www.rtl.fr')),
    (Media, ('Pouet', 'radio', 'www.rtl.fr')),
)

engine = create_engine('sqlite:///apiclock.sqlite')
session = sessionmaker(bind=engine)

DB = session()

if DB.query(Media).count() != 0:
    print "La base est déjà remplie."
else:
    for item in POPULATION:
        klass, args = item
        DB.add(klass(*args))

    DB.commit()
