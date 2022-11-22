from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required


from App.controllers import (
    create_publication, 
    get_all_pubs,
    get_all_pubs_json,
)

pub_views = Blueprint('pub_views', __name__, template_folder='../templates')


@pub_views.route('/publications', methods=['GET'])
def get_author_page():
    publications = get_all_pubs()
    return render_template('publications.html', publications=publications)

@pub_views.route('/api/publications')
def client_app():
    authors = get_all_pubs_json()
    return jsonify(publications)

@pub_views.route('/publication/<id>')
def pub_info(id):
    publication = get_pub(id)
    return render_template('pub-info.html', publication=publication)