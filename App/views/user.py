from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, session
from flask_login import login_required, current_user
from flask_jwt import jwt_required
# for exceptions
import sys

from App.controllers import (
    create_user,
    get_user_by_id,
    get_user_by_username, 
    get_all_users,
    get_all_users_json,
)

from App.controllers import *

user_views = Blueprint('user_views', __name__, template_folder='../templates')

# AUTHENTICATION ROUTES

@user_views.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        data = request.form
        usern = data['username']
        passw = data['password']

        if not usern or not passw:
            flash('Please enter both an username and password')
            return render_template('login.html')

        user = authenticate(usern, passw)

        if user: # check credentials
            flash('Logged in successfully.') # send message to next page
            log_in_user(user, True) # login the user
            return redirect('/profile/@' + str(user.username))

        else:
            flash('Invalid username or password') # send message to next page

    return render_template('login.html')

@user_views.route('/signup', methods=["POST"])
def create_user_route():
    data = request.get_json()
    if not data:
        return "Missing request body.", 400
    username = data['username']
    password = data['password']
    if not username or not password:
        return "Missing username or password parameter.", 400
    user = create_user(username, password)
    if not user:
        return "Failed to create.", 400
    return user.toJSON(), 201


@user_views.route('/login',methods=['POST'])
def login_u():
    data = request.get_json()
    email = data['email']
    password = data['password']
    if not email or not password:
        return "Please enter both an email and password",400
    author = Author.query.filter_by(email).first()
    if author and author.check_password():
        return "User logged in",201

# JINJA ROUTES

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/static/users')
def static_user_page():
  return send_from_directory('static', 'static-user.html')

@user_views.route('/profile/@<username>', methods=['GET'])
@login_required
def user_profile(username):
    user = get_user_by_username(username)
    return render_template('/protected/profile.html', user=user)

# API ROUTES

@user_views.route('/api/users')
def client_app():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/publications', methods=["GET"])
def get_publications():
    args = request.args
    if not args:
        pubs = get_all_publications_json()
        return jsonify(pubs), 200
    author_id = args.get("author")
    query = args.get("query")
    pubs = []
    if author_id:
        pubs = get_author_publications(author_id)
    if query:
        query = query.lower()
        print(query)
        pubs = filter(lambda pub: query in pub['title'].lower(), pubs)
    return jsonify(list(pubs)), 200
        

@user_views.route('/publications', methods=["POST"])
@jwt_required()
def post_publication():
    data = request.get_json()
    author_names = data['authors']
    coauthor_names = data['coauthors']
    authors = sum ( [get_author_by_name(name) for name in author_names], [] )
    coauthors = sum ( [get_author_by_name(name) for name in coauthor_names], [] )
    # return jsonify(author_names)
    try:
        new_pub = create_publication(data['title'], authors, coauthors)
    except Exception as e:
        return f'Could not create due to exception: {e.__class__}', 400
    return new_pub.toJSON(), 201

@user_views.route('/author', methods=["POST"])
@jwt_required()
def create_author_profile():
    data = request.get_json()
    # return jsonify(data)
    try:
        new_author = create_author(data['name'], data['dob'], data['qualifications'])
    except Exception as e:
        return f'Could not create due to exception: {e.__class__}', 400 
    return new_author.toJSON(), 201

@user_views.route('/author', methods=["GET"])
def get_author_profile():
    authors = get_all_authors_json()
    return jsonify(authors)

@user_views.route('/pubtree', methods=['GET'])
def get_pub_tree():
    args = request.args
    author_id = args.get('author_id')
    if not author_id:
        return "Must provide ID.", 400

    pubs = get_author_publications(author_id)
    return jsonify(pubs)
