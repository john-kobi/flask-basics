from flask import Flask, render_template

# Create an instance of Flask
app = Flask(__name__)

# Jinja filters:
# safe
# capitalize
# lower
# upper
# title
# trim
# striptags


# Create a route decorator
@app.route('/')
def index():
    # return render_template('index.html')
    return '<h1 style="color:red;">Hello World!</h1>'


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
