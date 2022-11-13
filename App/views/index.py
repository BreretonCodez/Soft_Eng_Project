from flask import Blueprint, redirect, render_template, request, send_from_directory

from App.controllers import (
    get_all_pubs,
    get_all_authors,
)

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    search = request.args.get('search')
    if search:
        publications = search_pub(search)
        authors = get_all_authors()
        return render_template('index.html', publications=publications, authors=authors)
    else:
        publications = get_all_pubs()
        authors = get_all_authors()
        return render_template('index.html', publications=publications, authors=authors)