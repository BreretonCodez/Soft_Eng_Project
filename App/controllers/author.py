from App.models import Author, User
from App.database import db

''' Creates a new Author '''
def create_author(fname, lname, username, email, password):
    newAuthor = Author(fname=fname, lname=lname, username=username, email=email, password=password)
    db.session.add(newAuthor)
    db.session.commit()
    return newAuthor

''' Deletes an Author '''
def delete_author(id):
    author = get_author_by_id(id)
    if author:
        db.session.delete(author)
        db.session.commit()
    return None

''' Updates an author '''
def update_author(id, fname, lname, email, institutions, qualifications):
    author = get_author_by_id(id)
    if author:
        author.fname = fname
        author.lname = lname
        author.email = email
        author.institution = institutions
        author.qualifications = qualifications
        db.session.add(author)
        return db.session.commit()
    return None

''' Searches for an Author '''
def search_author(search):
    return Author.query.filter(
        Author.name.like( '%'+search+'%')
    )

# Searches for User by Author ID
def find_user_by_author_id(id):
    return User.query.filter(
        User.authorId.like( '%'+id+'%' )
    )

''' Author Getters by parameter '''

def get_author_by_id(id):
    return Author.query.get(id)

def get_author_by_fname(fname):
    return Author.query.filter_by(fname=fname)

def get_author_by_lname(lname):
    return Author.query.filter_by(lname=lname)

def get_author_by_email(email):
    author = Author.query.filter_by(email=email).first()
    if not author:
        return None
    return author

def get_all_authors():
    return Author.query.all()

def get_all_authors_json():
    authors = Author.query.all()
    if not Author:
        return []
    authors = [author.toJSON() for author in authors]
    return authors

    