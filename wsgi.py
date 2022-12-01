import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import create_db, get_migrate
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, get_user_by_id, get_user_by_username )
# from App.controllers import ( create_author, get_all_authors_json, get_all_authors, get_author_by_id )
from App.controllers import ( create_publication, get_pub_by_id, get_all_pubs_json, add_pub_co_author )

from datetime import date

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

'''
Generic Commands
'''

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    create_db(app)
    print('database intialized')

# This command creates initial database objects
@app.cli.command("setup", help="Creates the database objects")
def initialize():
    create_db(app)
    create_user("whiteStar", "Password123!", "Mike", "Whitmore", "mwhitmore@gmail.com")
    create_user("Snickdx", "mendez15cool!", "Nicholas", "Mendez", "nmendez@gmail.com")
    create_user("Kingmb", "micah15cool!", "Micah", "Brereton", "mbrereton@gmail.com")
    create_user("zanedottxt", "zane15cool!", "Zane", "Amour", "zamour@gmail.com")
    create_user("danz", "danz15cool!", "Daniel", "Suite", "dsuite@gmail.com")
    create_user("kelz", "kella15cool!", "Michaela", "Noel", "mnoel@gmail.com")
    create_user("kota", "kota15cool!", "Dakota", "Sharma", "dsharma@gmail.com")
    create_user("pandaban", "mouseplushi23!", "Emily", "Phillips", "ephillips@gmail.com")

    create_publication("A random fact about Software Engineering.", 2, "https://nicholasmendez.dev/", "Something random about Software Engineering I chose to share randomly!", "UWI Educational Publishers", 2022)
    create_publication("Leveraging Kubernetes for Businesses Processes", 3, "https://micahb.icu/blog/", "Kubernetes, a feature of DevOps is facet that can significantly improve your business systems and activity", "WordPress", 2022)
    create_publication("How To NOT Suck at Gaming", 4, "https://zaneis.smart", "Gaming is quite simple actually", "The Game Blog", 2022)
    create_publication("Cloud and Big Data", 3, "https://micahb.icu/blog/", "Leveraging Cloud for stability of business systems when dealing with Big Data...", "WordPress", 2022)
    create_publication("The Perfect Shot", 5, "https://danz.jpeg", "New state of the art lenses developed by myself that can have amazing impact on your photos", "UWI Educational Publishers", 2022)
    create_publication("New Applications in UI/UX", 8, "https://emzz.design", "UI/UX are important facets of any system design", "The Designer's Magazine", 2022)
    create_publication("Random Envi Facts", 6, "https://kelztells.blog", "Environmental Science facts everyone should know", "UWI Educational Publishers", 2022)

    add_pub_co_author(6, 5)

    print('database setup')


# User Commands

user_cli = AppGroup('user', help='User object commands') 

@user_cli.command("create", help="Creates a new user")
@click.argument("username", default="cobratate")
@click.argument("password", default="topg23!")
@click.argument("fname", default="Andrew")
@click.argument("lname", default="Tate")
@click.argument("email", default="cobratate@gmail.com")
def create_user_command(username, password, fname, lname, email):
    create_user(username, password, fname, lname, email)
    print(f'{username} created!')

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli)


# Publication Commands

pub_cli = AppGroup('pub', help='Publication object commands') 

@pub_cli.command("create", help="Creates a publication")
@click.argument("title", default="Unleashing Ultimate Masculinity")
@click.argument("author", default="9")
@click.argument("link", default="https://cobratate.com")
@click.argument("content", default="We are all in a simulation. To become your ultimate best self and find true happiness, you must break out of the simulation.")
@click.argument("publisher", default="Wudan Publishers")
@click.argument("year", default="2022")
def create_publication_command(title, author, link, content, publisher, year):
    create_publication(title, author, link, content, publisher, year)
    print(f'{title} created!')

@pub_cli.command("list", help="Lists al publications")
def list_pubs():
    pubs = get_all_pubs_json()
    print(pubs)

@pub_cli.command("add_co_author", help="Adds a co-author to a publication")
@click.argument("id")
@click.argument("co_author")
def add_pub_co_author_command(id, co_author):
    add_pub_co_author(id, co_author)
    print(f'CoAuthor {co_author} added to Publication {get_pub_by_id(id).title}!')


@pub_cli.command("create_names")
@click.option("--author_names", "-A", multiple=True)
@click.option("--coauthor_names", "-CA", multiple=True)
@click.argument("title", default="Computer Science 1st Edition")
def create_publication_command(title, author_names, coauthor_names):
    authors = sum ( [get_author_by_name(name) for name in author_names], [] )
    print(authors)
    coauthors = sum ( [get_author_by_name(name) for name in coauthor_names], [] )
    print(coauthors)
    # a = get_author(author_ids)
    create_publication(title, authors, coauthors)
    print(f'{title} created!')


app.cli.add_command(pub_cli)


'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "User"]))

@test.command("author", help="Run Author tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "AuthorUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "AuthorIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "Author"]))

@test.command("publication", help="Run Publication tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "PublicationUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "PublicationIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "Publication"]))
    

app.cli.add_command(test)



