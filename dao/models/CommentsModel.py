from app import db
from datetime import datetime

class Comments(db.Model):
    __tabelname__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    bookid = db.Column(db.Integer, db.ForeignKey('books.id'))
    comment = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now())
    isDeleted = db.Column(db.Boolean, default=False)

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments_by_book_id(cls, bookid):
        return cls.query.filter_by(bookid=bookid, isDeleted=False).order_by(cls.timestamp.asc()).all()

    def delete(self):
        self.isDeleted = True

    def delete_commit(self):
        self.isDeleted = True
        db.session.commit()