from flask_restful import Resource, Api, original_flask_make_response, reqparse
from flask import render_template, Blueprint, flash, redirect
from flask_login import current_user, login_required

comment_blueprint = Blueprint('comment_api', __name__, template_folder='templates', static_folder='static')
api = Api(comment_blueprint)

from dao.models.CommentsModel import Comments
from dao.models.BookModel import Books


class Comment(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('comment_description', help="this field is mandatory", required=True)

    @login_required
    def post(self, id):
        data = self.parser.parse_args()

        new_comment = Comments(
            bookid=id,
            userid=int(current_user.get_id()),
            comment=data['comment_description']
        )

        try:
            book = Books.find_book_by_id(id)
            book.add_comment()
            new_comment.add()
            flash('comment posted', 'alert-success')
        except:
            flash('please try again later', 'alert-danger')

        return original_flask_make_response(redirect('/book/{}'.format(id)))


api.add_resource(Comment, '/book/<int:id>/comment')
