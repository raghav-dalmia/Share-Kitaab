from flask_restful import Resource, Api, original_flask_make_response, reqparse
from flask import render_template, Blueprint, flash, redirect
from flask_login import login_required, logout_user

logout_blueprint = Blueprint('logout_api', __name__, template_folder='templates', static_folder='static')
api = Api(logout_blueprint)

class Logout(Resource):

    def __init__(self):
        pass

    @login_required
    def get(self):
        logout_user()
        flash("Logout successfully.", "alert-success")
        return original_flask_make_response(redirect('/login'))


api.add_resource(Logout, '/logout')


