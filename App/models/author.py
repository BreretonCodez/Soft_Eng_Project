from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from datetime import *
from .publication import *

class Author(db.Model):
    __tablename__ = "author"
    id = db.Column(db.Integer, primary_key=True)
    fname =  db.Column(db.String, nullable=False)
    lname =  db.Column(db.String, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    qualifications = db.Column(db.String(120), nullable=True)
    institution = db.Column(db.String, nullable=True)
    publications = db.relationship("Publication", backref='Author', lazy='select')

    def __init__(self, fname, lname, username, email, password):
        self.fname = fname
        self.lname = lname
        self.username = username
        self.email = email
        self.set_password(password)

    def toJSON(self):
        return{
            'id': self.id,
            'fname': self.fname,
            'lname': self.lname,
            'username': self.username,
            'email': self.email,
            'qualifications': self.qualifications,
            'institution': self.institution,
            'publications': [publication.toJSON() for publication in self.publications],
        }

    def pubtree(self, coauthors):
        print(f"Publication Tree of Author: {self.fname} {self.lname}")
        for p in self.publications:
            for a in p.coauthors:
                a.pubtree

    def get_publications(self):
        return [publication.toJSON() for publication in self.publications]

    def set_password(self, password):
        '''Create hashed password.'''
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        '''Check hashed password.'''
        return check_password_hash(self.password, password)