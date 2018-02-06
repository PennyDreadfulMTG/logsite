from flask import url_for
from flask_babel import gettext

from logsite.view import View

# pylint: disable=no-self-use
class Home(View):
    def __init__(self, matches):
        self.matches = matches
        self.matches_url = url_for('matches')

    def subtitle(self):
        return None

    def TT_LATEST_MATCHES(self):
        return gettext("Latest Matches")

    def TT_MORE_MATCHES(self):
        return gettext("More matches…")
