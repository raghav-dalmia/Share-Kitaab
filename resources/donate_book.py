from flask import render_template, Blueprint
from flask_login import current_user, login_required

donate_book_blueprint = Blueprint('donate_book_blueprint', __name__, template_folder='templates',
                                  static_folder='static')

from dao.models.UserModel import User


@donate_book_blueprint.route('/donate-book', methods=['GET'])
@login_required
def donate_book():
    return render_template('donate_book.html')
