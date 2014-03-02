# ----------------------------------------------------
#   IMPORTS ET CONFIGURATION
# ----------------------------------------------------

from flask import Flask, render_template, redirect, request, session, url_for, flash, abort
import time
import os
from datetime import datetime
from forms import LoginForm, ContactForm

from liste_fichier import recup_liste, listdir
from bdd import creation_bdb, show_media, delete_media, add_media, update_media
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

# ----------------------------------------------------
#   FONCTIONS
# ----------------------------------------------------


def recup_heure():
    # recup l'heure et la transmet au param for_js transmis au JS pour affichage
    # pour n'afficher que l'heure : d.strftime('%H')
    d = datetime.now()
    return d


creation_bdb()


# ----------------------------------------------------
#   CREATION APPLICATION
# ----------------------------------------------------

app = Flask(__name__)
app.config.from_object(__name__)

# ----------------------------------------------------
#   GESTION IDENTIFICATION 
# ----------------------------------------------------

@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def welcome():
    form = LoginForm()
    """Si corectement identifie on renvoie vers welcome.html sinon vers login.html"""
    if session.get('logged_in'):
        # on recupere la liste ds radios ()show_media) et des podcast (show_podcast)
        # pour les afficher avec un bouton pour les jouer radio = show_media()
        radio = show_media('radio')
        podcast = show_media('podcast')

        # On affiche le repertoire /static/music pour afficher + btn pour les jouer
        # lecteur ne marche pas avec un rep monte en reseau dans /home/pi/music-debian/ .. pourquoi ??
        # music = os.listdir('../music-debian/AIR/moon safari')
        #music = os.listdir('../static/music')

        # on insere un cron job avec python-crontab
        # insertion_crontab(2)
        test = 'base'

    # verif de la presence de param pour modif OU ajout OU suppression RADIO
    if request.method == 'POST':
        # Fonction Suppression (on recupere l'ID passe dans le hidden form et on execute delete_media)
        if request.form['supprimer_radio'] == 'Supprimer':
            test = 'supprimer'
            i = request.form['id_media_supprimer']
            # si un param est passe par le champ "titre du podcast" depuis "Ajouter un podcast"
            delete_media(i)
            # accents passent pas ??
            flash('Radio supprime')

        # Fonction Jouer
        # MARCHE PAS ??
        elif request.form['jouer_radio'] == 'Jouer':
            i = request.form['id_media']
            path = request.form['url_media']
            play_MPD(path)
            test = 'jouer'
            flash('i')

        # Fonction Ajout (si le champ hidden ajouter_radio n'est pas vide on attribue les valeurs du formulaire
        # aux variables > arguments pour la fonction add_media()
        # MARCHE PAS ??
        elif request.form['ajouter_radio'] == 'Ajouter':
            test = 'ajouter'
            typemedia = 'radio'
            title = request.form['titremedia']
            urlmedia = request.form['urlmedia']
            add_media(typemedia, title, urlmedia)
            flash('Radio ajoutee')

        # Fonction modification (si le champ hidden ajoutradio n'est pas vide on attribue
        # les valeurs du formulaire aux variables > arguments pour la fonction update_media()
        # MARCHE PAS ??
        elif request.form['modifier_radio'] == 'Modifier':
            test = 'modifier'
            i = request.form['id_media_modif']
            typemedia = 'radio'
            title = request.form['modif_titre']
            urlmedia = request.form['modif_url']
            update_media(i, typemedia, title, urlmedia)
            flash('Radio modifiee')
    else:
        test = 'rien'
        return render_template('welcome.html',
                               radio=radio,
                               podcast=podcast,
                               test=test,
                               # music = music,
                               # testcron = testcron,
                               heures=recup_heure().strftime('%H'),
                               minutes=recup_heure().strftime('%M'),
                               secondes=recup_heure().strftime('%S'))

    else:
        return render_template('login.html',
                               form=form,
                               heures=recup_heure().strftime('%H'),
                               minutes=recup_heure().strftime('%M'),
                               secondes=recup_heure().strftime('%S'))


@app.route('/login', methods=['GET', 'POST'])
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