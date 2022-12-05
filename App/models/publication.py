from App.database import db
from datetime import datetime
from .author import *
from .author_publication import *

class Publication(db.Model):
    __tablename__ = "publication"
    pubId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    author = db.Column(db.ForeignKey('author.authorId'))
    coauthors = db.relationship('Author', secondary=PublicationTree)
    link = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    publisher = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    

    def __init__(self, title, author, link, content, publisher, year):
        self.title = title
        self.author = author
        self.link = link
        self.content = content
        self.publisher = publisher
        self.year = year
    
    def toJSON(self):
        return{
            'pubId': self.pubId,
            'title': self.title, 
            'author': self.author,
            'coauthors': [coauthor.toJSON() for coauthor in self.coauthors],
            'link': self.link,
            'content': self.content,
            'publisher': self.publisher,
            'year': self.year,
        }

    def add_co_author(self, author):
        self.coauthors.append(author)

    def pubtree(self):
        print(f"Publication Tree for Publication {self.title}")
        for a in self.coauthors:
            a.pubtree()

