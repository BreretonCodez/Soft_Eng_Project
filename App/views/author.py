from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required

from App.controllers import (
    create_author, 
    get_all_authors,
    get_all_pubs,
    get_all_users,
    get_all_authors_json,
    get_author_by_id,
    get_author_by_email,
    update_author,
    search_author,
    delete_author,
    get_user_by_id,
    get_user_by_username,
)

author_views = Blueprint('author_views', __name__, template_folder='../templates')



# Jinja Routes
@author_views.route('/authors', methods=['GET'])
def get_authors_page():
    search = request.args.get('search')
    authors = get_all_authors()
    users = get_all_users()
    pubs = get_all_pubs()
    if search:
        authors = search_author(search)
    return render_template('authors.html', authors=authors, users=users, pubs=pubs)

@author_views.route('/author/@<username>', methods=['GET'])
def author_profile(username):
    user = get_user_by_username(username)
    author = get_author_by_id(user.authorId)
    pubs = author.publications
    cas = 0
    for pub in pubs:
        for ca in pub.coauthors:
            cas = cas + 1

    allp = get_all_pubs()
    app = 0
    for p in allp:
        for ca in p.coauthors:
            if author.authorId == ca.authorId:
                app = app + 1
    return render_template('profile.html', user=user, author=author, cas=cas, app=app)

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
    if get_author_by_email(data['email']):
        return jsonify({"message":"Author email already exists!"})
    author = create_author(data['fname'], data['lname'], data['email'])
    return jsonify({"message":"Author created successfully!"})

@author_views.route('/api/authors', methods=['PUT'])
def update_author_action():
    data = request.json
    author = get_author_by_id(data['id'])
    if author:
        update_author(data['id'], data['fname'], data['lname'], data['email'], "", "")
        return jsonify({"message":"Author updated successfully!"})
    return jsonify({"message":"Author not found!"})

@author_views.route('/api/authors', methods=['DELETE'])
def delete_author_action():
    data = request.json
    author = get_author_by_id(data['id'])
    if author:
        delete_author(data['id'])
        return jsonify({"message":"Author deleted successfully!"})
    return jsonify({"message":"Author not found!"})