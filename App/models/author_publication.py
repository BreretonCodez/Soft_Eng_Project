from App.database import db

PublicationTree = db.Table('publication_tree',
    db.Column('publication', db.ForeignKey("publication.pubId"), primary_key=True),
    db.Column('coauthors', db.ForeignKey("author.authorId"), primary_key=True)
)