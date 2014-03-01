from wtforms import Form, TextField, TextAreaField, SubmitField, PasswordField, validators, ValidationError
 
class LoginForm(Form):
  username = TextField(u'Utilisateur', [validators.length(min=4, max=20)])
  passwd = PasswordField(u'Mot de passe', [validators.length(min=8, max=32)])
  submit = SubmitField(u'Entrer')
  
class ContactForm(Form):
  email = TextField("Email" , [validators.Email("Veuillez saisir un mail valide !"), validators.Required("Veuillez saisir un mail valide !")])
  subject = TextField("Sujet")
  message = TextAreaField("Message" , [validators.Required("Vous n'avez rien a dire ?!")])
  submit = SubmitField(u'Entrer')