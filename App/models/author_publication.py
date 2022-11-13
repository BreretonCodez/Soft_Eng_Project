from App.database import db

PublicationTree = db.Table('publication_tree',
    db.Column('publication', db.ForeignKey("publication.id"), primary_key=True),
    db.Column('coauthors', db.ForeignKey("author.id"), primary_key=True)
)