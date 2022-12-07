from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, session, redirect, flash, url_for
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
    get_pubs_by_author,
    update_author,
    update_user,
    delete_user,
)

from App.controllers import *

user_views = Blueprint('user_views', __name__, template_folder='../templates')

# AUTHENTICATED ROUTES

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
            return redirect("/profile/@" + str(usern))

        else:
            flash('Invalid username or password') # send message to next page

    return render_template('login.html')


@user_views.route("/logout", methods=["GET"])
@login_required
def logout():
    log_out_user()
    flash('Logged out successfully.') # send message to next page
    return redirect("/login")

@user_views.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        form = request.form
        user = create_user(form["username"], form["password"], form["fname"], form["lname"], form["email"])
        if not user:
            flash("Author already exists.")
            return render_template("register.html")
        flash("User account succesfully created.")
        return redirect("/login")
    else: 
        return render_template("register.html")

@user_views.route("/profile/@<username>/edit", methods=['GET', 'POST'])
@login_required
def edit_user_backend(username):
    user = get_user_by_username(username)
    author = get_author_by_id(user.authorId)
    data = request.form
    if "update-author" in data and request.method == 'POST':
        update_author(author.authorId, data['fname'], data['lname'], data['email'], data['institution'], data['qualifications'])
        flash('Profile updated successfully!')
        return render_template('/protected/edit-user.html', user=user, author=author)

    
    return render_template('/protected/edit-user.html', user=user, author=author)

'''@user_views.route('/signup', methods=["POST"])
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
    return user.toJSON(), 201'''


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
    author = get_author_by_id(user.authorId)
    publications = get_pubs_by_author(user.authorId)
    return render_template('/protected/profile.html', user=user, author=author, publications=publications)

# API ROUTES

@user_views.route('/api/users', methods=['GET'])
def get_all_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users/id', methods=['GET'])
def get_user_action():
    data = request.json
    user = get_user_by_id(data['id'])
    return jsonify(user)

@user_views.route('/api/users', methods=['POST'])
def create_user_action():
    data = request.json
    if get_user_by_username(data['username']):
        return jsonify({"message":"Username already exists!"})
    user = create_user(data['username'], data['password'], data['fname'], data['lname'], data['email'])
    return jsonify({"message":"User created successfully!"})

@user_views.route('/api/users', methods=['PUT'])
def update_user_action():
    data = request.json
    user = get_user_by_id(data['id'])
    if user:
        update_user(data['id'], data['authorId'], data['username'], data['password'])
        return jsonify({"message":"User updated successfully!"})
    return jsonify({"message":"User not found!"})

@user_views.route('/api/users', methods=['DELETE'])
def delete_user_action():
    data = request.json
    user = get_user_by_id(data['id'])
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message":"User deleted successfully!"})
    return jsonify({"message":"User not found"})

@user_views.route('/user/author', methods=['GET'])
def get_user_author():
    data = request.json()
    user = get_user_by_id(data['id'])
    if user:
        ai = get_author_by_id(user.authorId)
        if ai:
            author = user.author.toJSON()
            return author
        jsonify({"message":"User has no author!"})
    return jsonify({"message":"User not found!"})

    
    
    
    
    
    
'''try:
    new_author = create_author(data['name'], data['dob'], data['qualifications'])
except Exception as e:
    return f'Could not create due to exception: {e.__class__}', 400 
return new_author.toJSON(), 201'''

