from flask import url_for
import inflect
import titlecase

from ..view import View
from ..data.match import Match as Model


# pylint: disable=no-self-use
class Match(View):
    def __init__(self, match: Model) -> None:
        self.match = match
        self.id = match.id
        self.comment = match.comment
        self.format_name = match.format_name()
        self.players_string = ' vs '.join([p.name for p in match.players])
        self.game_one = match.games[0]
        self.has_game_two = False
        self.has_game_three = False
        if len(match.games) > 1:
            self.has_game_two = True
            self.game_two = match.games[1]
        if len(match.games) > 2:
            self.has_game_three = True
            self.game_three = match.games[2]

    def subtitle(self):
        return None

    def og_title(self):
        return self.players_string

    def og_url(self):
        return url_for('show_match', match_id=self.id, _external=True)

    def og_description(self):
        p = inflect.engine()
        fmt = titlecase.titlecase(p.a(self.format_name))
        description = '{fmt} match.'.format(fmt=fmt)
        return description

