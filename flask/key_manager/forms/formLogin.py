from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class Login(FlaskForm):
    account = StringField("Conta", validators=[DataRequired()])
    password = PasswordField("Senha", validators=[DataRequired()])
    send = SubmitField("Entrar")