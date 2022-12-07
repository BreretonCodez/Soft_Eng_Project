import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import *

from App.main import create_app
from App.database import create_db
from App.models import User, Author, Publication
from App.controllers import (
    create_user,
    get_all_users_json,
    authenticate,
    get_user_by_id,
    get_user_by_username,
    update_user,
    create_publication,
    get_all_authors_json,
    create_author,
    create_publication,
    get_all_pubs_json,
    get_author_by_id
)

from wsgi import app


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("Bobman", "bobpass", "Bobby", "Franklin", "bfranklin@gmail.com")
        assert user.username == "Bobman"

    def test_user_toJSON(self):
        author = Author("Bobby", "Franklin", "bfranklin@gmail.com")
        user = User("Bobman", "bobpass", "Bobby", "Franklin", "bfranklin@gmail.com")
        user_json = user.toJSON()
        self.assertDictEqual(user_json, {"userId":None, "authorId": 1, "username":"Bobman", "password":"bobpass", "author":{"authorId": 1, "email": "bfranklin@gmail.com", "fname": "Bobby", "institution": null, "lname": "Franklin", "publications": [], "qualifications": null}})
    
    def test_hashed_password(self):
        password = "bobpass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("Bobman", "bobpass", "Bobby", "Franklin", "bfranklin@gmail.com")
        assert user.password != password

    def test_check_password(self):
        password = "bobpass"
        user = User("Bobman", "bobpass", "Bobby", "Franklin", "bfranklin@gmail.com")
        assert user.check_password(password)

class AuthorUnitTests(unittest.TestCase):

    def test_new_author(self):
        author = Author("James", "Bond", "jbond@spy.net")
        assert author.fname == "James" and author.lname == "Bond" and author.email == "jbond@spy.net"

    def test_author_toJSON(self):
        author =  Author("James", "Bond", "jbond@spy.net")
        author_json = author.toJSON()
        self.assertDictEqual(author_json, {
            "authorId": None,
            "fname": "James",
            "lname": "Bond",
            "email": "jbond@spy.net",
            "qualifications": None,
            "institution": None,
            "publications": []
        })

class PublicationUnitTests(unittest.TestCase):
    def test_new_publication(self):
        #(title, author, link, content, publisher, year)
        author = Author("James", "Bond", "jbond@spy.net")
        coauthor = Author("James", "Band", "jband@spy.net")
        publication = Publication("Intro to Computer Science", author, "comp.sci","Computer Science BSc","UWI",2022)
        publication.add_co_author(coauthor)
        assert (
            publication.title=="Intro to Computer Science"
            and publication.link=="comp.sci"
            and publication.content=="Computer Science BSc" 
            and publication.publisher=="UWI"
            and publication.author==author.author_id 
            and publication.coauthors==coauthor
        )

    def test_publication_toJSON(self):
        author = Author("James", "Bond", "jbond@spy.net")
        coauthor = Author("James", "Band", "jband@spy.net")
        publication = Publication("Intro to Computer Science", author, "comp.sci","Computer Science BSc","UWI",2022)
        publication.add_co_author(coauthor)
        publication_json = publication.toJSON()
        self.assertDictEqual(publication_json, {
            "pubid": None,
            "title": "Intro to Computer Science",
            "author": author.author_id,
            "coauthors": [coauthor.toJSON() for coauthor in coauthors],
            "link": "comp.sci",
            "content": "Computer Science BSc",
            "publisher": "UWI",
            "year": 2022
        })

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+'/App/test.db')

