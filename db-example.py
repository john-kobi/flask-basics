from flask import Flask, render_template, redirect, flash, request, url_for
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users-example2.db'
app.config['SECRET_KEY'] = 'h8f76234bf42672nd'
db = SQLAlchemy(app)


with app.app_context():
    class Users(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(200), nullable=False)
        email = db.Column(db.String(200), nullable=False, unique=True)

        # Optional: this will allow each book object to be identified by its title when printed.
        def __repr__(self):
            return f'<User {self.name}>'
    # db.create_all()
    # db.session.commit()

    try:
        new_user = Users(id=None, name="jimm", email="jizz demon")
        db.session.add(new_user)
        db.create_all()
        db.session.commit()
    except:
        print('User already added!')

if __name__ == '__main__':
    app.run(debug=True)
