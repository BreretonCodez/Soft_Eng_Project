from App.models import Author
from App.database import db

''' Creates a new Author '''
def create_author(fname, lname, email, password):
    newAuthor = Author(fname=fname, lname=lname, email=email, password=password)
    db.session.add(newAuthor)
    db.session.commit()
    return new_author

''' Deletes an Author '''
def delete_author(id):
    author = get_author_by_id(id)
    if author:
        db.session.delete(author)
        db.session.commit()
    return None

''' Searches for an Author '''
def search_author(search):
    return Author.query.filter(
        Author.name.like( '%'+search+'%')
    )

''' Author Getters by parameter '''

def get_author_by_id(id):
    return Author.query.get(id)

def get_author_by_fname(fname):
    return Author.query.filter_by(fname=fname)

def get_author_by_lname(lname):
    return Author.query.filter_by(lname=lname)

def get_author_by_email(email):
    author = Author.query.filter_by(email=email)

    if not author:
        create_author("New", "Author", email, "newAuthor123!")
        author = Author.query.filter_by(email=email)
    
    return author

def get_all_authors():
    return Author.query.all()

def get_all_authors_json():
    authors = Author.query.all()
    if not Author:
        return []
    authors = [author.toJSON() for author in authors]
    return authors

'''def get_author_publications(id):
    author = get_author(id)
    if not author:
        return []
    return author.get_publications()

def getpublicationtree(id):
    author = get_author(id)
    if not author:
        return []
    return author.get_publications()'''
    