# -*- coding: utf-8 -*-

from wtforms import Form, TextField, TextAreaField, SubmitField, PasswordField, validators, ValidationError


class LoginForm(Form):
    """Définition pour formulaire login"""
    username = TextField(u'Utilisateur', [validators.length(min=4, max=20)])
    passwd = PasswordField(u'Mot de passe', [validators.length(min=8, max=32)])
    submit = SubmitField(u'Entrer')


class Mediaform(Form):
    """Ajout media radio"""
    nommedia = TextField(u'Nom Radio', [validators.length(min=4, max=40)])
    urlmedia = TextField(u'Url Radio', [validators.length(min=4, max=100)])
    submit = SubmitField(u'Ajouter')
    submit = SubmitField(u'Modifier')
    submit = SubmitField(u'Supprimer')


class ContactForm(Form):
    """Définition pour formulaire contact"""
    email = TextField("Email", [validators.Email("Veuillez saisir un mail valide !"),
                                validators.Required("Veuillez saisir un mail valide !")])
    subject = TextField("Sujet")
    message = TextAreaField("Message", [validators.Required("Vous n'avez rien à dire ?!")])
    submit = SubmitField(u'Entrer')