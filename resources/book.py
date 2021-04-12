import os
from dao.dao import save_image, delete_image
from datetime import datetime
from flask_restful import Resource, Api, original_flask_make_response, reqparse
from flask import render_template, Blueprint, flash, redirect, request
from flask_login import login_user, current_user, login_required

book_blueprint = Blueprint('book_api', __name__, template_folder='templates', static_folder='static')
api = Api(book_blueprint)

from dao.models.UserModel import User
from dao.models.BookModel import Books
from dao.models.CommentsModel import Comments
from dao.models.RequestBookModel import Requests


class Book(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('donate_title', help="this feild is mandatory", required=True)
        self.parser.add_argument('donate_category', help="this feild is mandatory", required=True)
        self.parser.add_argument('donate_location', help="this feild is mandatory", required=True)
        self.parser.add_argument('donate_description', help="this feild is mandatory", required=True)

    def get(self, id):
        book = Books.find_book_by_id(id)

        if not book or book.isDeleted:
            flash("This book doesn't exists", "alert-warning")
            return original_flask_make_response(redirect('/'))

        user = User.find_user_by_id(book.userid)
        comments = Comments.get_comments_by_book_id(id)
        requests = Requests.get_requests_by_book_id(id)
        try:
            isRequested = Requests.is_requested(id, int(current_user.get_id()))
        except:
            isRequested = False
        return original_flask_make_response(
            render_template('show_book.html', book=book, user=user, comments=comments, requests=requests, isRequested=isRequested))

    @login_required
    def post(self, id):

        if id != int(current_user.get_id()):
            flash("You don't have access to create a card. Please contact admins.", "alert-danger")
            return original_flask_make_response(redirect('/'))

        data = self.parser.parse_args()
        imageFile = request.files['donate_image']

        try:
            if imageFile.filename == "":
                imageFilename = "book.jpg"
            else:
                imageFilename = datetime.now().strftime("%d_%b_%Y_%H:%M:%S") + "_{}.jpg".format(id)
                save_image(imageFile, imageFilename)
        except:
            imageFilename = "book.jpg"

        new_book = Books(
            userid=current_user.get_id(),
            title=data['donate_title'],
            category=data['donate_category'],
            location=data['donate_location'],
            description=data['donate_description'],
            imageName=imageFilename,
        )

        try:
            new_book.add_book()
            flash("Card created successfully.", "alert-success")
            return original_flask_make_response(redirect('/book/{}'.format(new_book.id)))
        except:
            delete_image(imageFilename)
            flash("Error occur! Please try again.")
            return original_flask_make_response(redirect('/donate-book'))

    @login_required
    def delete(self, id):
        book = Books.find_book_by_id(id)

        if not book or book.userid != int(current_user.get_id()):
            flash("You don't have access to delete this card.", "alert-warning")
            return "/book/{}".format(id)

        try:
            book.delete()
            delete_image(book.imageName)
            flash("Card deleted successfully")
            return '/'
        except:
            flash("Please try again later", "alert-danger")
            return "/book/{}".format(id)


api.add_resource(Book, '/book/<int:id>')
