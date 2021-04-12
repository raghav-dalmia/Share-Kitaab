import smtplib
from flask_minify import minify
import flask_profiler
from flask import Flask, render_template, request
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from message.Credentials import me, password

from constants import CATEGORIES, LOCATIONS

app = Flask(__name__)
app.secret_key = 'fijsdahfiw234242wdashifn9328678324y32687hwu'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dao/app.db'

app.config["DEBUG"] = True

app.config["flask_profiler"] = {
    "enabled": app.config["DEBUG"],
    "storage": {
        "engine": "sqlite"
    },
    "basicAuth": {
        "enabled": True,
        "username": "admin",
        "password": "bansalji"
    },
    "ignore": [
        "^/static/.*"
    ]
}

db = SQLAlchemy()
db.init_app(app)

s = smtplib.SMTP('smtp.gmail.com', 587)

loginManager = LoginManager()
loginManager.login_view = '/login'
# TODO: add flash message to login manager
# TODO: add flash category to login manager
loginManager.init_app(app)

minify(app=app, html=True, js=True, cssless=True, fail_safe=True)

from dao.models.UserModel import User


@app.before_first_request
def create_tables():
    db.create_all()
    s.starttls()
    s.login(me, password)


from resources import signup

app.register_blueprint(signup.signup_blueprint)

from resources import login

app.register_blueprint(login.login_blueprint)

from resources import logout

app.register_blueprint(logout.logout_blueprint)

from resources import donate_book

app.register_blueprint(donate_book.donate_book_blueprint)

from resources import book

app.register_blueprint(book.book_blueprint)

from resources import profile

app.register_blueprint(profile.profile_blueprint)

from resources import book_request

app.register_blueprint(book_request.book_request_blueprint)

from resources import comment

app.register_blueprint(comment.comment_blueprint)


@loginManager.user_loader
def load_user(user_id):
    return User.find_user_by_id(int(user_id))


from dao.models.BookModel import Books


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(500)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(410)
def page_not_found(e):
    return render_template('404.html')


@app.route('/')
def index():
    location = request.args.get('filter_location')
    category = request.args.get('filter_category')
    print(location, category)
    books = Books.filter_books(location=location, category=category)
    return render_template('index.html', books=books)


@app.route('/about-us')
def about_us():
    return render_template('about_us.html')

@app.route('/tnc')
def show_tnc():
    return '''
1. We (team Share Kitaab) are not liable/ responsible for anything.
2. We have hosted this site on pythonanywhere.com with a beginner account, you can read their privacy policy and terms & conditions.
3. We have managed this domain( sharekitaab.in) with godadday.in, you can read their privacy policy and terms & conditions.
'''


@app.context_processor
def inject_stage_and_region():
    return dict(
        categories=CATEGORIES,
        locations=LOCATIONS,
        index_url="http://127.0.0.1:5000/"
    )

flask_profiler.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
