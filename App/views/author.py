from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required

from App.controllers import (
    create_author, 
    get_all_authors,
    get_all_authors_json,
    get_author_by_id,
    get_author_by_email,
    get_user_by_id,
    get_user_by_username,
)

author_views = Blueprint('author_views', __name__, template_folder='../templates')



# Jinja Routes
@author_views.route('/authors', methods=['GET'])
def get_authors_page():
    authors = get_all_authors()
    return render_template('authors.html', authors=authors)

@author_views.route('/author/@<username>', methods=['GET'])
def author_profile(username):
    user = get_user_by_username(username)
    author = get_author_by_id(user.authorId)
    return render_template('profile.html', user=user, author=author)

'''@author_views.route('/author/<id>', methods=['GET'])
def author_profile2(id):
    author1 = get_author_by_id(id)
    return render_template('profile.html', author=author1)'''

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
    author = get_author_by_id(data['id'])
    if author:
        return author.toJSON()
    return jsonify({"message":"Author not found!"})

@author_views.route('/api/authors', methods=['POST'])
def create_author_action():
    data = request.json
    get_author_by
    if get_author_by_email(data['email']):
        return jsonify({"message":"Author email already exists!"})
    author = create_author(data['fname'], data['lname'], data['email'])
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