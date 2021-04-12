from datetime import datetime
from flask import render_template, Blueprint, redirect, flash, request
from flask_login import current_user, login_required

profile_blueprint = Blueprint('profile_blueprint', __name__, template_folder='templates', static_folder='static')

from dao.models.UserModel import User
from dao.models.BookModel import Books
from dao.dao import save_profile_image, delete_profile_image


@profile_blueprint.route('/profile/<int:id>')
def show_profile(id):
    user = User.find_user_by_id(id)
    if not bool(user):
        flash('User doesn\'t exists', 'alert-warning')
        return redirect('/')
    books = Books.find_book_by_user_id(id)
    return render_template('show_profile.html', user=user, books=books)


@profile_blueprint.route('/profile/<int:id>/image', methods=['POST'])
@login_required
def update_profile_image(id):

    if id != int(current_user.get_id()):
        flash("You don\'t have to update this profile.", "alert-warning")
        return redirect("/profile/{}".format(id))

    imageFile = request.files['profile_pic_image']

    try:
        if imageFile.filename == "":
            imageFilename = "avtar-image.jpg"
        else:
            imageFilename = datetime.now().strftime("%d_%b_%Y_%H:%M:%S") + "_{}.jpg".format(id)
            save_profile_image(imageFile, imageFilename)
    except:
        imageFilename = "avtar-image.jpg"

    try:
        user = User.find_user_by_id(id)
        delete_profile_image(user.profile_image_path)
        user.update_profile_pic(imageFilename)
        flash("Profile picture updated successfully.", "alert-success")
    except:
        flash("Please try again later.", "alert-warning")

    return redirect("/profile/{}".format(id))