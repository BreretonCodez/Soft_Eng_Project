from App.models import Author, User
from App.database import db

''' Creates a new User '''
def create_user(username, password, fname, lname, email):
    user = User(username=username, password=password, fname=fname, lname=lname, email=email)
    db.session.add(user)
    db.session.commit()
    return user

def update_user(userId, authorId, username, password):
    user = get_user_by_id(userId)
    if user:
        check = get_user_by_username(username)
        if check == None:
            user.username = username
            user.authorId = authorId
            user.password = password
            db.session.add(user)
            return db.session.commit()
    return None

''' Deletes a User '''
def delete_user(id):
    user = get_user_by_id(id)
    if user:
        delete_author(user.authorId)
        db.session.delete(user)
        db.session.commit()
    return None

''' Searches for a User '''
def search_user(search):
    return User.query.filter(
        User.username.like( '%'+search+'%')
    )

''' Author Accessors by parameter '''

def get_user_by_id(id):
    return User.query.filter_by(id=id).first()

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user_by_author(authorId):
    return User.query.filter_by(authorId=authorId).first()

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not User:
        return []
    users = [user.toJSON() for user in users]
    return users
