from flask import request, url_for

from logsite.view import View
from logsite.data import match

# pylint: disable=no-self-use
class Matches(View):
    def __init__(self, person=None):
        if person is None:
            matches = match.get_recent_matches(None)
        else:
            matches = match.get_recent_matches_by_player(person)

        self.matches = matches.items
        self.has_next = matches.has_next
        self.has_prev = matches.has_prev
        if matches.has_next:
            self.next_url = url_for(request.endpoint, person=person, page=matches.next_num)
        if matches.has_prev:
            self.prev_url = url_for(request.endpoint, person=person, page=matches.prev_num)

    def subtitle(self):
        return None
