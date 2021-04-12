from app import db
from datetime import datetime
from dao.models.RequestBookModel import Requests


class Books(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(30), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    imageName = db.Column(db.String(30), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now())
    isDeleted = db.Column(db.Boolean, default=False)
    numComments = db.Column(db.Integer, default=0)
    numRequests = db.Column(db.Integer, default=0)

    def add_book(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_book_by_id(cls, _id):
        return cls.query.filter_by(id=_id, isDeleted=False).first()

    @classmethod
    def find_book_by_user_id(cls, userid):
        return cls.query.filter_by(userid=userid, isDeleted=False).order_by(cls.timestamp.asc()).all()

    @classmethod
    def get_all_books(cls):
        return cls.query.filter_by(isDeleted=False).order_by(cls.timestamp.asc()).all()

    @classmethod
    def modify_filter_value(cls, value):
        if not value or value == "select":
            return None
        else:
            value = str(value).strip()
            return None if value == "" else value

    @classmethod
    def filter_books(cls, location, category):
        location = cls.modify_filter_value(location)
        category = cls.modify_filter_value(category)
        if not location and not category:
            return cls.query.filter_by(isDeleted=False).order_by(cls.timestamp.asc()).all()
        elif not location:
            return cls.query.filter_by(isDeleted=False, category=category).order_by(cls.timestamp.asc()).all()
        elif not category:
            return cls.query.filter_by(isDeleted=False, location=location).order_by(cls.timestamp.asc()).all()
        else:
            return cls.query.filter_by(isDeleted=False, location=location, category=category).order_by(
                cls.timestamp.asc()).all()

    def delete(self):
        requests = Requests.get_requests_by_book_id(self.id)
        for request in requests:
            request.delete()
        self.isDeleted = True
        db.session.commit()

    def add_comment(self):
        self.numComments = self.numComments + 1

    def add_request(self):
        self.numRequests = self.numRequests + 1
