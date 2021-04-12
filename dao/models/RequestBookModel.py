from app import db
from datetime import datetime


class Requests(db.Model):
    __tabelname__ = "requests"

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    bookid = db.Column(db.Integer, db.ForeignKey('books.id'))
    reason = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now())
    isDeleted = db.Column(db.Boolean, default=False)

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_requests_by_book_id(cls, bookid):
        return cls.query.filter_by(bookid=bookid, isDeleted=False).order_by(cls.timestamp.asc()).all()

    @classmethod
    def get_requests_by_user_id(cls, userid):
        return cls.query.filter_by(userid=userid, isDeleted=False).order_by(cls.timestamp.asc()).all()

    @classmethod
    def is_requested(cls, bookid, userid):
        request = cls.query.filter_by(bookid=bookid, userid=userid, isDeleted=False).first()
        return bool(request)

    def delete(self):
        self.isDeleted = True

    def delete_commit(self):
        self.isDeleted = True
        db.session.commit()
