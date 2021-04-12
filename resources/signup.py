from flask_restful import Resource, Api, original_flask_make_response, reqparse
from flask import render_template, Blueprint, flash, redirect
from werkzeug.security import generate_password_hash
from flask_login import current_user, logout_user, login_user
from datetime import datetime

CLIENT_ID = "560673026852-4lpuc9bn9m8olniphlb4gukboiac2co4.apps.googleusercontent.com"

signup_blueprint = Blueprint('signup_api', __name__, template_folder='templates', static_folder='static')
api = Api(signup_blueprint)

from dao.models.UserModel import User
from dao.dao import download_image


class Signup(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('signup_name', help="this feild is mandatory", required=True)
        self.parser.add_argument('signup_email', help="this feild is mandatory", required=True)
        self.parser.add_argument('signup_phone', help="this feild is mandatory", required=True)
        self.parser.add_argument('signup_password', help="this feild is mandatory", required=True)

    def get(self):

        if current_user.is_authenticated:
            flash("Already login.", "alert-warning")
            return original_flask_make_response(redirect('/'))

        headers = {'Content-Type': 'text/html'}
        return original_flask_make_response(render_template('signup.html'))

    def post(self):

        if current_user.is_authenticated:
            flash("Already login.", "alert-warning")
            return original_flask_make_response(redirect('/'))

        data = self.parser.parse_args()

        if User.is_user_exists(data['signup_email']):
            flash("User with {} email already exists.".format(data['signup_email']), "alert-warning")
            return original_flask_make_response(redirect('/signup'))
        else:
            new_user = User(
                name=data['signup_name'],
                email=data['signup_email'],
                phone=data['signup_phone'] if data['signup_phone'] != "" else None,
                password=generate_password_hash(data['signup_password'])
            )
            try:
                new_user.add_user()
                login_user(new_user)
                flash("User register successfully.", "alert-success")
                return original_flask_make_response(redirect('/'))
            except:
                flash("Error occur! please try again later.", "alert-danger")
                return original_flask_make_response(redirect('/signup'))


class GoogleSignup(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('g_signup_name', help="this feild is mandatory", required=True)
        self.parser.add_argument('g_signup_email', help="this feild is mandatory", required=True)
        self.parser.add_argument('g_signup_id', help="this feild is mandatory", required=True)
        self.parser.add_argument('g_signup_image_url', help="this feild is mandatory", required=True)
        # self.parser.add_argument('g_signup_token', help="this feild is mandatory", required=True)

    def post(self):

        if current_user.is_authenticated:
            flash("Already login.", "alert-warning")
            return '/'

        data = self.parser.parse_args()

        if User.is_g_user_exists(data['g_signup_id']):
            user = User.find_user_by_gid(data['g_signup_id'])
            login_user(user)
            flash('Login successfully!', 'alert-success')
            return '/'
        elif bool(User.find_user_by_email(data['g_signup_email'])):
            flash('user with email {} already exists. Please login with password.', 'alert-warning')
            return '/login'
        else:
            new_user = User(
                gid=data['g_signup_id'],
                name=data['g_signup_name'],
                email=None if data['g_signup_email'] == "null" else data['g_signup_email'],
                profile_image_path=datetime.now().strftime("%d_%b_%Y_%H:%M:%S") + "_{}.jpg".format(id),
                is_g_user=True
            )
            new_user.add_user()
            login_user(new_user)
            try:
                download_image(data['g_signup_image_url'], new_user.profile_image_path)
            except:
                new_user.profile_image_path = "avtar-image.jpg"
            flash('user registered successfully.', 'alert-success')
            return '/'


api.add_resource(GoogleSignup, '/signup/google')
api.add_resource(Signup, '/signup')
