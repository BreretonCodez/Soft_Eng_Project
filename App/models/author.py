from App.database import db
from .publication import *

class Author(db.Model):
    __tablename__ = "author"
    authorId = db.Column(db.Integer, primary_key=True)
    fname =  db.Column(db.String, nullable=False)
    lname =  db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    qualifications = db.Column(db.String(120), nullable=True)
    institution = db.Column(db.String, nullable=True)
    publications = db.relationship("Publication", backref='Author', lazy='select')

    def __init__(self, fname, lname, email):
        self.fname = fname
        self.lname = lname
        self.email = email

    def toJSON(self):
        return{
            'authorId': self.authorId,
            'fname': self.fname,
            'lname': self.lname,
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