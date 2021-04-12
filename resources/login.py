from flask_restful import Resource, Api, original_flask_make_response, reqparse
from flask import render_template, Blueprint, flash, redirect
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user

login_blueprint = Blueprint('login_api', __name__, template_folder='templates', static_folder='static')
api = Api(login_blueprint)

from dao.models.UserModel import User


class Login(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('login_email', help="this feild is mandatory", required=True)
        self.parser.add_argument('login_password', help="this feild is mandatory", required=True)

    def get(self):
        if current_user.is_authenticated:
            flash("Already login.", "alert-warning")
            return original_flask_make_response(redirect('/'))

        headers = {'Content-Type': 'text/html'}
        return original_flask_make_response(render_template('login.html', show_login_button=False))

    def post(self):
        if current_user.is_authenticated:
            print('authed')
            flash("Already login.", "alert-warning")
            return original_flask_make_response(redirect('/'))

        data = self.parser.parse_args()

        if not User.is_user_exists(data['login_email']):
            flash("Email or password is not valid.", "alert-danger")
            return original_flask_make_response(redirect('/login'))
        else:
            user = User.find_user_by_email(data['login_email'])
            if not check_password_hash(user.password, data['login_password']):
                flash("Email or password is not valid.", "alert-danger")
                return original_flask_make_response(redirect('/login'))
            else:
                login_user(user)
                return original_flask_make_response(redirect('/'))



api.add_resource(Login, '/login')
