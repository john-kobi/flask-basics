from flask import Flask, render_template, redirect, flash, request, url_for, jsonify
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor, CKEditorField
from flask_login import UserMixin, LoginManager, login_required, logout_user, current_user

# Create an instance of Flask
app = Flask(__name__)

Bootstrap(app)
ckeditor = CKEditor(app)
# old SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users2.db'
# MYSQL database location
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:jMwrF!2o7@localhost/users'
app.config['SECRET_KEY'] = 'h8f76234bf42672nd22d9hHIDW98272^*@IB(@BHFNB9'
# Initialize database
db = SQLAlchemy(app)
# migrate = Migrate(app, db)
sarah_birthday_mug = '011101000110111100100000011010010111010001100101011100100110000101110100011001' \
                     '010010000001101001011100110010000001101000011101010110110101100001011011100010' \
                     '110000100000011101000110111100100000011100100110010101100011011101010111001001' \
                     '11001101100101001000000110010001101001011101100110100101101110011001010000000000000100'
# Create a database model/table
with app.app_context():
    class Posts(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(200), nullable=False)
        sub_title = db.Column(db.String(200), nullable=False)
        body = db.Column(db.String(200), nullable=False)
        author = db.Column(db.String(200), nullable=False)
        date = db.Column(db.String(200), nullable=False)
        img_url = db.Column(db.String(200), nullable=False)


    class Users(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(200), nullable=False)
        username = db.Column(db.String(200), nullable=False, unique=True)
        email = db.Column(db.String(200), nullable=False, unique=True)
        fave_color = db.Column(db.String(200), nullable=True)
        date_added = db.Column(db.DateTime, default=datetime.datetime.now())
        password_hash = db.Column(db.String(128))

        @property
        def password(self):
            raise AttributeError('Password is not a readable attribute')

        @password.setter
        def password(self, password):
            self.password_hash = generate_password_hash(password)

        def verify_password(self, password):
            return check_password_hash(self.password_hash, password)

        # Create a string
        def __repr__(self):
            return '<Name %r>' % self.name

    # Use only once to create the database
    # db.create_all()
    # db.session.commit()
    # new_post = Posts(
    #     title="john",
    #     sub_title="is",
    #     author="a",
    #     body="body text",
    #     date='today',
    #     img_url="https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187_2x1.jpg"
    # )
    # db.session.add(new_post)
    # db.session.commit()


class PostForm(FlaskForm):
    author = StringField("Author", validators=[DataRequired()])
    title = StringField("Post title", validators=[DataRequired()])
    sub_title = StringField("Post subtitle", validators=[DataRequired()])
    body = StringField("Post subtitle", validators=[DataRequired()])
    # body = CKEditorField('Body', validators=[DataRequired()])
    img_url = StringField("Image URL", validators=[DataRequired()])
    submit = SubmitField("Submit")


class UserForm(FlaskForm):
    name = StringField("Full name", validators=[DataRequired()])
    email = StringField("Email address", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    password_hash2 = PasswordField("Confirm", validators=[DataRequired()])
    password_hash = PasswordField("Choose a password",
                                  validators=[EqualTo('password_hash2', message="Passwords must match")])
    fave_color = StringField("What's your favourite color?")
    submit = SubmitField("Submit")


class TestPw(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class MyForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    email = StringField("Email address", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

# with app.app_context():
#     new_user = Users(
#         name='john',
#         email='dsflkgjndf@lknjfds',
#         fave_color="blue"
#     )
#     db.session.add(new_user)
#     db.session.commit()


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('dashboard'))

    return render_template('login.html', form=form)

@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    return render_template('dashboard.html')

@app.route('/delete/<int:id>', methods=["GET", "POST"])
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    db.session.delete(post_to_delete)
    db.session.commit()
    flash(message='Post deleted!')
    return redirect(url_for('all_posts'))


@app.route('/edit-post/<int:id>', methods=["GET", "POST"])
def edit_post(id):
    form = PostForm()
    post_to_edit = Posts.query.get_or_404(id)
    if form.validate_on_submit():
        post_to_edit.title = form.title.data
        post_to_edit.sub_title = form.sub_title.data
        post_to_edit.author = form.author.data
        post_to_edit.body = form.body.data
        post_to_edit.date = post_to_edit.date
        post_to_edit.img_url = form.img_url.data
        # print(post_to_edit.title,
        # post_to_edit.sub_title,
        # post_to_edit.author,
        # post_to_edit.body,
        # post_to_edit.date,
        # post_to_edit.img_url)

        db.session.add(post_to_edit)
        db.session.commit()
        flash(message='Edit saved!')
        return redirect(url_for('all_posts'))
    form.title.data = post_to_edit.title
    form.sub_title.data = post_to_edit.sub_title
    form.author.data = post_to_edit.author
    form.body.data = post_to_edit.body
    form.img_url.data = post_to_edit.img_url
    return render_template('edit-post.html', form=form, post=post_to_edit)


@app.route('/post/<int:id>')
def show_post(id):
    post = Posts.query.get_or_404(id)
    print(post)
    print(post.title)
    return render_template('show-post.html', post=post)


@app.route('/all-posts', methods=["GET", "POST"])
def all_posts():
    posts = Posts.query.order_by(Posts.date)
    return render_template('all-posts.html', posts=posts)


@app.route('/add-post', methods=["GET", "POST"])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        print("Form validated on submit!")
        new_post = Posts(
            title=form.title.data,
            sub_title=form.sub_title.data,
            author=form.author.data,
            body=form.body.data,
            date=datetime.datetime.now().strftime("%A %d %B %Y %H:%M"),
            img_url=form.img_url.data,
        )
        print(new_post)
        db.session.add(new_post)
        db.session.commit()
        flash(message='Post added!')
        return redirect(url_for('all_posts'))
    return render_template('add-post.html', form=form)


@app.route('/date')
def get_date():
    # dict = {
    #     "Set A":
    #         {
    #             "name": "john",
    #             "age": 122,
    #             "sex": "male",
    #             "height": 181,
    #             "alive": True, },
    #     "Set B":
    #         {
    #             "name": "Steve",
    #             "age": 122123,
    #             "sex": "female",
    #             "height": 11,
    #             "alive": False, },
    #
    # }
    return {"Date": datetime.datetime.now().strftime("%A %d %B %Y %H:%M")}


@app.route('/delete/<int:id>', methods=["GET", "POST"])
def delete(id):
    record_to_delete = Users.query.get_or_404(id)
    try:
        db.session.delete(record_to_delete)
        db.session.commit()
        flash(f"Record for {record_to_delete.name} deleted")
    except:
        flash(f"There was an error please try again...")
    return redirect(url_for('add_user'))


# Update user record in database
@app.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
    users = Users.query.order_by(Users.date_added)
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.password_hash = request.form['password_hash']
        name_to_update.fave_color = request.form['fave_color']
        try:
            db.session.commit()
            flash(f"User {name_to_update.name} updated!")
            form.name.data = ''
            form.email.data = ''
            form.password_hash.data = ''
            return render_template('update-user.html', form=form, users=users)
        except:
            flash(f"Error! You douchebag...")
            return render_template('update-user.html', form=form, name_to_update=name_to_update, users=users)
    else:
        return render_template('update-user.html', form=form, name_to_update=name_to_update, users=users)


@app.route('/user/add', methods=["GET", "POST"])
def add_user():
    form = UserForm()
    name = None
    our_users = Users.query.order_by(Users.date_added)
    if form.validate_on_submit():
        print("validated")
        user = Users.query.filter_by(email=form.email.data).first()
        if user == None:
            if form.password_hash.data == form.password_hash2.data:
                hashed_pw = generate_password_hash(form.password_hash.data)
                new_user = Users(
                    name=form.name.data,
                    email=form.email.data,
                    username=form.username.data,
                    fave_color=form.fave_color.data,
                    password_hash=hashed_pw,
                )
                db.session.add(new_user)
                db.session.commit()
                flash("You were added to the database")
                name = form.name.data
                form.name.data = ''
                form.email.data = ''
                form.username.data = ''
                form.fave_color = ''
                form.password_hash.data = ''
                print(f"Added {new_user} to database: {app.config['SQLALCHEMY_DATABASE_URI']}")
            else:
                flash('Passwords must match!')
                return render_template('add-user.html', form=form, name=name, users=our_users)
        else:
            flash("There is already an account with that email address! Please use a different email address.")
    return render_template('add-user.html', form=form, name=name, users=our_users)


@app.route('/test-pw', methods=["GET", "POST"])
def test_pw():
    form = TestPw()
    email = None
    password = None
    pw_to_check = None
    passed = None
    # Validate form
    if form.validate_on_submit():
        print("validated!")
        email = form.email.data
        print(email)
        password = form.password.data
        print(password)
        user_to_check = Users.query.filter_by(email=email).first()
        passed = check_password_hash(user_to_check.password_hash, password)
        if passed:
            flash('You are now logged in!', category='message')
        else:
            flash('Nope!', category='message')

            return render_template('test-pw.html', form=form, email=email, password=password,
                                   user_to_check=user_to_check)
        return render_template('test-pw.html', form=form, email=email, password=password,
                               user_to_check=user_to_check, passed=passed)
    return render_template('test-pw.html', form=form, email=email, password=password)


@app.route('/name', methods=["GET", "POST"])
def name():
    form = MyForm()
    if form.validate_on_submit():
        name = form.name.data
        flash('Form successfully submitted!', category='message')
        return render_template('name.html', name=name, form=form)
    else:
        name = None
    return render_template('name.html', name=name, form=form)


# Create a route decorator
@app.route('/')
def index():
    flash('Welcome to our website. Use code: 20%OFF this weekend only!')
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
