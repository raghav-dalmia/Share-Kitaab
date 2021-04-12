import os
import urllib.request

UPLOAD_FOLDER_PATH = "/home/raghav/Desktop/Share_Kitaab/static/images/books"
UPLOAD_PROFILE_FOLDER_PATH = "/home/raghav/Desktop/Share_Kitaab/static/images/profiles"


def save_profile_image(imageFile, imageFilename):
    imagePath = os.path.join(UPLOAD_PROFILE_FOLDER_PATH, imageFilename)
    imageFile.save(imagePath)


def delete_profile_image(imageFilename):
    if imageFilename != "avtar-image.jpg":
        imagePath = os.path.join(UPLOAD_PROFILE_FOLDER_PATH, imageFilename)
        os.remove(imagePath)


def save_image(imageFile, imageFilename):
    imagePath = os.path.join(UPLOAD_FOLDER_PATH, imageFilename)
    imageFile.save(imagePath)


def delete_image(imageFilename):
    if imageFilename != "book.jpg":
        imagePath = os.path.join(UPLOAD_FOLDER_PATH, imageFilename)
        os.remove(imagePath)


def download_image(url, imageFilename):
    imagePath = os.path.join(UPLOAD_PROFILE_FOLDER_PATH, imageFilename)
    urllib.request.urlretrieve(url, imagePath)
