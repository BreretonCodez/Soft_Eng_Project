from flask import Blueprint, render_template, jsonify, request, send_from_directory, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_jwt import jwt_required


from App.controllers import (
    create_publication,
    get_pub_by_id,
    get_all_pubs,
    get_all_authors,
    get_all_users,
    update_pub,
    get_all_users,
    add_pub_co_author,
    del_pub_co_author,
    get_all_pubs_json,
    get_author_by_id,
    get_author_by_email,
    get_all_authors,
    get_user_by_author,
    get_user_by_username,
    get_pubs_by_author,
    delete_publication,
    search_pub,
)

pub_views = Blueprint('pub_views', __name__, template_folder='../templates')

# Jinja Routes

@pub_views.route('/publications', methods=['GET'])
def get_pub_page():
    search = request.args.get('search')
    publications = get_all_pubs()
    authors = get_all_authors()
    users = get_all_users()
    if search:
        publications = search_pub(search)
    return render_template('publications.html', publications=publications, authors=authors, users=users)

@pub_views.route('/publication/<id>')
def pub_info(id):
    publication = get_pub_by_id(id)
    author = get_author_by_id(publication.author)
    user = get_user_by_author(author.authorId)
    users = get_all_users()
    return render_template('pub-info.html', publication=publication, author=author, user=user, us=users)

# AUTHENTICATED ROUTES

@pub_views.route('/profile/publication/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_pub(id):
    pub = get_pub_by_id(id)
    user = get_user_by_author(pub.author)
    data = request.form
    if "update-pub" in data and request.method == 'POST':
        if not data['title'] or not data['content'] or not data['link'] or not data['publisher'] or not data['year']:
            flash('Please fill all data fields!')
            redirect(url_for('.edit_pub', id=id))
        update_pub(id, data['title'], user.authorId, data['content'], data['link'], data['publisher'], data['year'])

    if "add-co" in data and request.method == 'POST':
        email = data['email']
        coa = get_author_by_email(email)
        if not coa:
            flash('Invalid Co-Author!')
            redirect(url_for('.edit_pub', id=id))
        add_pub_co_author(id, coa.authorId)
        flash('Co-Author added successfully!')

    if "del-co" in data and request.method == 'POST':
        email = data['email']
        if email:
            coa = get_author_by_email(email)
            if not coa:
                flash('Invalid Co-Author!')
                redirect(url_for('.edit_pub', id=id))
            del_pub_co_author(id, coa.authorId)
            flash('Co-Author added successfully!')
            
    if "del-pub" in data and request.method == 'POST':
        delete_publication(pub.pubId)
        flash('Publication deleted successfully!')
        redirect(url_for('.get_all_pubs_backend', username=user.username))

    author = get_author_by_id(pub.author)
    cas = pub.coauthors
    return render_template('/protected/edit-pub.html', pub=pub, author=author, cas=cas, user=user)

@pub_views.route('/profile/@<username>/publications', methods=['GET', 'PUT', 'POST'])
@login_required
def get_all_pubs_backend(username):
    user = get_user_by_username(username)
    author = get_author_by_id(user.authorId)
    pubs = get_pubs_by_author(author.authorId)
    return render_template('/protected/all-pubs.html', pubs=pubs, author=author, user=user)

@pub_views.route('/profile/@<username>/publication/add', methods=['GET', 'POST'])
@login_required
def add_pub_backend(username):
    user = get_user_by_username(username)
    author = get_author_by_id(user.authorId)
    if request.method == 'POST':
        data = request.form
        if not data['title'] or data['link'] or data['content'] or data['publisher'] or data['year']:
            flash('Please enter data for all fields!')

        create_publication(data['title'], user.authorId, data['link'], data['content'], data['publisher'], data['year'])
        return redirect(url_for('.get_all_pubs_backend', username=user.username))

    flash('Publication added successfully!')
    return render_template('/protected/add-pub.html', user=user, author=author)


# JS Routes

'''@pub_views.route('/static/authors')
def static_user_page():
  return send_from_directory('static', 'static-user.html')'''

# API Routes

@pub_views.route('/api/publications', methods=['GET'])
def get_all_pubs_action():
    publications = get_all_pubs_json()
    return jsonify(publications)

@pub_views.route('/api/publications', methods=['POST'])
def create_pub_action():
    data = request.json
    pub = create_publication(data['name'], data['author'], data['content'], data['citation'])
    return jsonify({"message":"Publication created successfully!"})

@pub_views.route('/api/publications', methods=['PUT'])
def update_pub_action():
    data = request.json
    pub = get_pub_by_id(data['id'])
    if pub:
        update_pub(data['id'], data['name'], data['author'], data['content'], data['citation'])
        return jsonify({"message":"Publication updated successfully!"})
    return jsonify({"message":"Publication not found!"})

@pub_views.route('/api/publications', methods=['DELETE'])
def delete_pub_action():
    data = request.json
    pub = get_pub_by_id(data['id'])
    if pub:
        delete_publication(data['id'])
        return jsonify({"message":"Publication deleted successfully!"})
    return jsonify({"message":"Publication not found!"})

@pub_views.route('/api/publications/author', methods=['GET'])
def get_author_pubs_action():
    data = request.json
    author = get_author_by_id(data['author'])
    if author:
        pubs = get_pub_by_author(data['author'])
        return jsonify(pubs)
    return jsonify({"message":"Author not found!"})

@pub_views.route('/api/publications/id', methods=['GET'])
def get_pub_action():
    data = request.json
    pub = get_pub_by_id(data['id'])
    if pub:
        return pub.toJSON()
    return jsonify({"message":"Publication not found!"})

@pub_views.route('/api/publication/add-co-author', methods=['PUT'])
def add_co_author_action():
    data = request.json
    pub = get_pub_by_id(data['id'])
    if pub:
        add_pub_co_author(data['id'], data['author'])
        return jsonify({"message":"Co-Author added to Publication successfully!"})
    return jsonify({"message":"Publication not found!"})