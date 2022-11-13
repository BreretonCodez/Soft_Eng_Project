from App.database import db
from .author import *
from .author_publication import *

class Publication(db.Model):
    __tablename__ = "publication"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    author = db.Column(db.ForeignKey('author.id'))
    coauthors = db.relationship('Author', secondary=PublicationTree)
    content = db.Column(db.String, nullable=False)
    citation = db.Column(db.String, nullable=False)

    def __init__(self, title, author, content, citation):
        self.title = title
        self.author = author
        self.content = content
        self.citation = citation
    
    def toJSON(self):
        return{
            'id': self.id,
            'title': self.title, 
            'authors': self.author.toJSON(),
            'coauthors': [coauthor.toJSON() for coauthor in self.coauthors],
            'content': self.content,
            'citation': self.citation,
        }

