# coding: utf-8
from __future__ import unicode_literals
from wtforms import Form, StringField, PasswordField, validators, TextAreaField


class HomeworkForm(Form):
    class Meta:
        locales = ['pl_PL', 'pl']


class LoginForm(Form):
    username = StringField("Nazwa użytkownika", [validators.DataRequired()])
    password = PasswordField("Hasło", [validators.DataRequired()])


class RegisterForm(Form):
    username = StringField(
        "Nazwa użytkownika",
        [validators.Length(min=3, max=20)]
    )
    password = PasswordField("Hasło", [validators.Length(min=4)])
    repeat_password = PasswordField(
        "Powtórz hasło",
        [validators.EqualTo('password', "Hasła muszą się zgadzać.")]
    )
    public_key = TextAreaField(
        "Twój publiczny klucz PGP",
        [validators.DataRequired()],
        description="-----BEGIN PGP PUBLIC KEY BLOCK-----     "
                    "-----END PGP PUBLIC KEY BLOCK-----"
    )

class MessageForm(Form):
    subject = StringField('Temat', [validators.DataRequired()])
    encmessage = StringField(
        'Zaszyfrowana wiadomość',
        [validators.DataRequired()]
    )
    recipient = StringField('Adresat', [validators.DataRequired()])