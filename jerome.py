# ----------------------------------------------------
#   IMPORTS ET CONFIGURATION
# ----------------------------------------------------

from flask import Flask, render_template, redirect, request, session, url_for, flash, abort
import time
import os
from flask_bootstrap import Bootstrap
from datetime import datetime
from forms import LoginForm, ContactForm, Mediaform

# from liste_fichier import recup_liste, listdir
# from bdd import creation_bdb, show_media, delete_media, add_media, update_media, \
from bdd import Reveil, User, Media, Playlist, sessiont


from jouer_mpd import create_MPDplaylist, play_MPD
from podcast import ajout_podcast

heure = datetime.now().strftime("%H:%M:%S")
# A changer : le path des config (playlist MPD) // 

# ----------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------
USERNAME = 'admin'
PASSWORD = 'default'
SECRET_KEY = 'clef de securite en carton'

RECAPTCHA_PUBLIC_KEY = '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

# ----------------------------------------------------
#   FONCTIONS
# ----------------------------------------------------


def recup_heure():
    # recup l'heure et la transmet au param for_js transmis au JS pour affichage
    # pour n'afficher que l'heure : d.strftime('%H')
    d = datetime.now()
    return d


# creation_bdb()


# ----------------------------------------------------
#   CREATION APPLICATION
# ----------------------------------------------------

app = Flask(__name__)
app.config.from_object(__name__)
Bootstrap(app)

# ----------------------------------------------------
#   GESTION IDENTIFICATION 
# ----------------------------------------------------

@app.route('/index', methods=('GET', 'POST'))
@app.route('/', methods=('GET', 'POST'))

def welcome():
    """Si corectement identifie on renvoie vers welcome.html sinon vers login.html"""
    form = Mediaform()
    # on recupere la liste ds medai de type "radio"
    radio = sessiont.query(Media).filter(Media.type == 'radio').all()

    if session.get('logged_in'):

        if request.method == 'POST':

            # SUPPRESSION
            if request.form['supprimer_radio']:
                idsupprimer = request.form['id_media_supprimer']
                sessiont.query(Media).filter_by(id=idsupprimer).delete()
                sessiont.commit()

            # JOUER
            elif request.form['jouer_radio']:
                radiojouer = sessiont.query(Media).filter_by(id=idmedia).first()
                path = radiojouer.url
                play_MPD(path)

            # MODIFICATION
            elif request.form['modifier_radio']:
                idmodif = request.form['idmedia']
                modift = request.form['nommedia']
                typemodif = request.form['typemedia']
                test = idmodif
                sessiont.query(Media).filter(Media.id == idmodif).update({'nom': modift}, {'type': typemodif})
                sessiont.commit()

            # AJOUTER RADIO
            elif request.form['ajouter_radio']:
                nom = request.form['nommedia']
                urlmedia = request.form['urlmedia']
                test = urlmedia
                radiot = Media(nom=nom, type='radio', url=urlmedia)
                sessiont.add(radiot)
                sessiont.commit()

        else:
            return render_template('welcome.html',
                               form=form,
                               test=test,
                               radio=radio,
                               heures=recup_heure().strftime('%H'),
                               minutes=recup_heure().strftime('%M'),
                               secondes=recup_heure().strftime('%S'))

    else:
        return render_template('welcome.html',
                               form=form,
                               radio=radio,
                               heures=recup_heure().strftime('%H'),
                               minutes=recup_heure().strftime('%M'),
                               secondes=recup_heure().strftime('%S'))

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    error = None

    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['passwd'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('welcome'))

    return render_template('login.html',
                           error=error,
                           form=form,
                           heures=recup_heure().strftime('%H'),
                           minutes=recup_heure().strftime('%M'),
                           secondes=recup_heure().strftime('%S'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('welcome'))


# ----------------------------------------------------
#   PAGES NON PROTEGEES 
# ----------------------------------------------------


@app.route('/about', methods=['GET', 'POST'])
def about():
    form = ContactForm()
    error = None
    ajout_podcast()

    return render_template('about.html',
                           form=form,
                           error=error)

# ----------------------------------------------------
#   PAGES  PROTEGEES 
# ----------------------------------------------------

#@app.route('/protege', methods=['GET', 'POST'])
#def protege():
#    # on verifie qu'on est bien identifie et que le form a ete soumis
#    if session.get('logged_in') and request.method == 'POST':
#        return render_template('protege.html')
#    else:
#        return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')