from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
# Create an instance of Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'h8f76234bf42672nd22d9hHIDW98272^*@IB(@BHFNB9'

# Jinja filters:
# safe
# capitalize
# lower
# upper
# title
# trim
# striptags


class MyForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a route decorator
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', user=name)


# Invalid URl error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Internal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
