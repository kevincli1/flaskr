from datetime import datetime
from flaskr import db, login_manager
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    posts = db.relationship('Post', backref='user')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    title = db.Column(db.String(140), nullable=False)
    body = db.Column(db.String(140), nullable=False)


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))
