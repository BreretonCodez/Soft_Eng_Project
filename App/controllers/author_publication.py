from App.models import AuthorPublication
from App.database import db
'''get all items in the form of a json'''
def get_all_items_json():
    rows = AuthorPublication.query.all()
    if not rows:
        return []
    rows = [row.toJSON() for row in rows]
    return rows 
