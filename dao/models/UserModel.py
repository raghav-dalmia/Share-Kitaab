from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30))
    phone = db.Column(db.String(10))
    profile_image_path = db.Column(db.String(40), default="avtar-image.jpg")
    password = db.Column(db.String(100))
    numReports = db.Column(db.Integer, default=0)
    isReported = db.Column(db.Boolean, default=False)
    gid = db.Column(db.String(40))
    is_g_user = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "{} {}".format(self.email, self.name)

    def add_user(self):
        db.session.add(self)
        db.session.commit()

    def update_profile_pic(self, image_path):
        self.profile_image_path = image_path
        db.session.commit()

    @classmethod
    def find_user_by_id(cls, _id):
        return cls.query.filter_by(id=int(_id)).first()

    @classmethod
    def find_user_by_gid(cls, gid):
        return cls.query.filter_by(gid=gid, is_g_user=True).first()

    @classmethod
    def find_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def is_user_exists(cls, email):
        query = cls.query.filter_by(email=email).first()
        return bool(query)

    @classmethod
    def is_g_user_exists(cls, gid):
        query = cls.query.filter_by(gid=gid, is_g_user=True).first()
        return bool(query)
