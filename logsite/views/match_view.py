from flask import url_for

from ..view import View
from ..db import Match as Model


# pylint: disable=no-self-use
class Match(View):
    def __init__(self, match: Model) -> None:
        self.match = match
        self.id = match.id
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
            self.game_three = match.games[3]

    def subtitle(self):
        return None
