from flask_restful import Resource, Api, original_flask_make_response, reqparse
from flask import render_template, Blueprint, flash, redirect
from flask_login import current_user, login_required
from message.Credentials import me

book_request_blueprint = Blueprint('book_request_api', __name__, template_folder='templates', static_folder='static')
api = Api(book_request_blueprint)

from dao.models.UserModel import User
from dao.models.BookModel import Books
from dao.models.RequestBookModel import Requests
from message.EmailMessage import sendMessage, format_request_message


class RequestBook(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('request_bookid', help="this feild is mandatory", required=True)
        self.parser.add_argument('request_reason', help="this feild is mandatory", required=True)

    @login_required
    def post(self):
        data = self.parser.parse_args()
        userid = int(current_user.get_id())
        bookid = int(data['request_bookid'])

        if Requests.is_requested(bookid, userid):
            flash('You have already requested for this book. Please wait for owner\'s response or contact us at {}'.format(me))
            return original_flask_make_response(redirect('/book/{}'.format(bookid)))

        new_request = Requests(
            userid=userid,
            bookid=bookid,
            reason=data['request_reason'],
        )

        try:
            book = Books.find_book_by_id(bookid)
            owner_user = User.find_user_by_id(book.userid)
            interested_user = User.find_user_by_id(userid)

            book.add_request()
            new_request.add()

            print(owner_user, interested_user)

            try:
                sendMessage(
                    owner_user.email,
                    "Request for {} book".format(book.title),
                    format_request_message(
                        owner_user.email,
                        book.title,
                        interested_user.name,
                        interested_user.phone,
                        interested_user.email,
                        data['request_reason']
                    )
                )
            except:
                pass

            flash('We have sent your request to the book owner.', 'alert-success')
        except:
            flash('Error occur. Please try again after sometime.', 'alert-warning')

        return original_flask_make_response(redirect('/book/{}'.format(bookid)))


api.add_resource(RequestBook, '/request')