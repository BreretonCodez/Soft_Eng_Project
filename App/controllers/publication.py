from App.models import Author
from App.models import Publication
from App.database import db
from .author import *

''' Creates a new publication '''
def create_publication(title, author, link, content, publisher, year):
    newPub = Publication(title=title, author=author, link=link, content=content, publisher=publisher, year=year)
    db.session.add(newPub)
    db.session.commit()
    return newPub

''' Deletes a publication '''
def delete_publication(id):
    pub = get_pub_by_id(id)
    if pub:
        db.session.delete(pub)
        db.session.commit()
    return None

''' Updates a publication '''
def update_pub(id, title, author, content, citation):
    pub = get_pub_by_id(id)
    if pub:
        pub.title = title
        pub.author = author
        pub.content = content
        pub.citation = citation
        db.session.add(pub)
        return db.session.commit()
    return None

''' Add Publication Co-Author '''

def add_pub_co_author(id, co_author):
    pub = get_pub_by_id(id)
    if pub:
        author = get_author_by_id(co_author)
        pub.coauthors.append(author)
        db.session.add(pub)
        return db.session.commit()
    return None

''' Searches for a Publication '''
def search_pub(search):
    return Publication.query.filter(
        Publication.title.like( '%'+search+'%' )
    )

''' Publication Getters by parameter '''
def get_pub_by_id(id):
    return Publication.query.get(id)

def get_pub_by_title(title):
    return Publication.query.filter_by(title=title).first()

def get_pubs_by_author(author_id):
    pubs = Publication.query.filter_by(author=author_id).all()

    if not pubs:
        return []

    return pubs

def get_all_pubs():
    return Publication.query.all()

def get_all_pubs_json():
    pubs = Publication.query.all()
    if not pubs:
        return []

    pubs = [pub.toJSON() for pub in pubs]
    return pubs

def get_pub_tree(id):
    pub = get_pub_by_id(id)
    
    if pub:
        pubs1 = get_pubs_by_author(pub.author)
        if pub.coauthors:
            for coauthor in pub.coauthors:
                pubs2 += get_pubs_by_author(coauthor)
        pubs = pubs1 + pubs2
        return pubs
    return None