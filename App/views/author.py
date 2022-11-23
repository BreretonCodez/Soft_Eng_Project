from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required

from App.controllers import (
    create_author, 
    get_all_authors,
    get_all_authors_json,
)

author_views = Blueprint('author_views', __name__, template_folder='../templates')

@author_views.route('/signup', methods=['GET','POST'])
def create_user_route():
    data = request.get_json()
    if not data:
        return "Missing request body.", 400
    firstName = data['fistname']
    lastName = data['lastname']
    email = data['email']
    username = data['username']
    password = data['password']
    if not username or not password or not email or not firstName or not lastName:
        return "You are missing a field, please ensure that all fields are used", 400
    user = create_user(firstName,lastName,username,email,password)
    if not user:
        return "Failed to create.", 400
    return user.toJSON(), 201


@author_views.route('/login',methods=['POST'])
def login_user():
    data = request.get_json()
    email = data['email']
    password = data['password']
    if not email or not password:
        return "Please enter both an email and password",400
    author = Author.query.filter_by(email).first()
    if author and author.check_password():
        return "User logged in",201


@author_views.route('/authors', methods=['GET'])
def get_authors_page():
    authors = get_all_authors()
    return render_template('authors.html', authors=authors)

@author_views.route('/author/<id>', methods=['GET'])
def author_profile(id):
    author = get_author(id)
    return render_template('profile.html', author=author)

# JS Routes
@author_views.route('/static/authors')
def static_author_page():
  return send_from_directory('static', 'static-user.html')

# API Routes
@author_views.route('/api/authors', methods=['GET'])
def get_all_authors_action():
    authors = get_all_authors_json()
    return jsonify(authors)

@author_views.route('/api/authors/id', methods=['GET'])
def get_author_action():
    data = request.json
    author = get_author(data['id'])
    if author:
        return author.toJSON()
    return jsonify({"message":"Author not found!"})

@author_views.route('/api/authors', methods=['POST'])
def create_author_action():
    data = request.json
    if get_author_email(data['email']):
        return jsonify({"message":"Author email already exists!"})
    author = create_author(data['fname'], data['lname'], data['email'], data['password'])
    return jsonify({"message":"Author created successfully!"})

@author_views.route('/api/authors', methods=['PUT'])
def update_author_action():
    data = request.json
    author = get_author(data['id'])
    if author:
        update_author(data['id'], data['fname'], data['lname'], data['email'], data['password'])
        return jsonify({"message":"Author updated successfully!"})
    return jsonify({"message":"Author not found!"})

@author_views.route('/api/authors', methods=['DELETE'])
def delete_author_action():
    data = request.json
    author = get_author(data['id'])
    if author:
        delete_author(data['id'])
        return jsonify({"message":"Author deleted successfully!"})
    return jsonify({"message":"Author not found!"})