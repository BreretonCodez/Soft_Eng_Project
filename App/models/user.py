from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from .author import *
from .publication import *

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    authorId = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
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

    def set_password(self, password):
        '''Create hashed password.'''
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        '''Check hashed password.'''
        return check_password_hash(self.password, password)