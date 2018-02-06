from flask import request, url_for

from logsite.view import View

# pylint: disable=no-self-use
class Matches(View):
    def __init__(self, matches):
        self.matches = matches.items
        self.has_next = matches.has_next
        self.has_prev = matches.has_prev
        if matches.has_next:
            self.next_url = url_for(request.endpoint, page=matches.next_num)
        if matches.has_prev:
            self.prev_url = url_for(request.endpoint, page=matches.prev_num)

    def subtitle(self):
        return None
