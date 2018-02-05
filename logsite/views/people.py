from flask import url_for

from logsite.view import View
from .. import db

# pylint: disable=no-self-use
class People(View):
    def __init__(self):
        people = db.User.query.order_by(db.User.name.asc()).paginate(per_page=50)
        self.people = people.items
        self.has_next = people.has_next
        self.has_prev = people.has_prev
        if people.has_next:
            self.next_url = url_for('people', page=people.next_num)
        if people.has_prev:
            self.prev_url = url_for('people', page=people.prev_num)

    def subtitle(self):
        return None
