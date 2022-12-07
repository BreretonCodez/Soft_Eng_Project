from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db
from .author import *
from .publication import *

class User(db.Model, UserMixin):
    userId = db.Column(db.Integer, primary_key=True)
    authorId = db.Column(db.Integer, db.ForeignKey('author.authorId'), nullable=False)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(128), nullable=False)
    author=db.relationship('Author')

    def __init__(self, username, password, fname, lname, email, author=None):
        if author:
            return None
        author = Author(fname=fname, lname=lname, email=email)
        db.session.add(author)
        db.session.commit()
        self.authorId = author.authorId
        self.username = username
        self.set_password(password)

    def toJSON(self):
        return{
            'userId': self.userId,
            'authorId': self.authorId,
            'username': self.username,
            'author': self.author.toJSON(),
        }

    def __repr__(self):
        return f"<user {self.userId} {self.username}>"  

    def set_password(self, password):
        '''Create hashed password.'''
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        '''Check hashed password.'''
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.userId)