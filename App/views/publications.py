from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required


from App.controllers import (
    create_publication,
    get_pub_by_id,
    get_all_pubs,
    get_all_pubs_json,
    get_author_by_id,
    get_user_by_author,
)

pub_views = Blueprint('pub_views', __name__, template_folder='../templates')

# Jinja Routes

@pub_views.route('/publications', methods=['GET'])
def get_pub_page():
    publications = get_all_pubs()
    return render_template('publications.html', publications=publications)

@pub_views.route('/publication/<id>')
def pub_info(id):
    publication = get_pub_by_id(id)
    author = get_author_by_id(publication.author)
    user = get_user_by_author(author.authorId)
    return render_template('pub-info.html', publication=publication, author=author, user=user)

# JS Routes

'''@pub_views.route('/static/authors')
def static_user_page():
  return send_from_directory('static', 'static-user.html')'''

# API Routes

@pub_views.route('/api/publications', methods=['GET'])
def get_all_pubs_action():
    publications = get_all_pubs_json()
    return jsonify(publications)

@pub_views.route('/api/publications/author', methods=['GET'])
def get_author_pubs_action():
    data = request.json
    author = get_author(data['author'])
    if author:
        pubs = get_pub_by_author(data['author'])
        return jsonify(pubs)
    return jsonify({"message":"Author not found!"})


@pub_views.route('/api/publications/id', methods=['GET'])
def get_pub_action():
    data = request.json
    pub = get_pub(data['id'])
    if pub:
        return pub.toJSON()
    return jsonify({"message":"Publication not found!"})

@pub_views.route('/api/publications', methods=['POST'])
def create_pub_action():
    data = request.json
    pub = create_publication(data['name'], data['author'], data['content'], data['citation'])
    return jsonify({"message":"Publication created successfully!"})

@pub_views.route('/api/publications', methods=['PUT'])
def update_pub_action():
    data = request.json
    pub = get_pub(data['id'])
    if pub:
        update_pub(data['id'], data['name'], data['author'], data['content'], data['citation'])
        return jsonify({"message":"Publication updated successfully!"})
    return jsonify({"message":"Publication not found!"})

@pub_views.route('/api/publications', methods=['DELETE'])
def delete_pub_action():
    data = request.json
    pub = get_pub(data['id'])
    if pub:
        delete_publication(data['id'])
        return jsonify({"message":"Publication deleted successfully!"})
    return jsonify({"message":"Publication not found!"})

@pub_views.route('/api/publication/add-co-author', methods=['PUT'])
def add_co_author_action():
    data = request.json
    pub = get_pub(data['id'])
    if pub:
        add_pub_co_author(data['id'], data['author'])
        return jsonify({"message":"Co-Author added to Publication successfully!"})
    return jsonify({"message":"Publication not found!"})