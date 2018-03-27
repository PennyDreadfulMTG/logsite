import random

from logsite.view import View


# pylint: disable=no-self-use
class InternalServerError(View):
    def __init__(self, exception):
        self.exception = str(exception)
        # self.card = random.choice(oracle.load_cards(['Erratic Explosion', 'Curse of Chaos', 'Anarchy']))
        self.card = None
        self.cards = [self.card]

    def message(self):
        return 'Something went wrong.'

    def template(self):
        return 'error'

    def subtitle(self):
        return 'Internal Server Error'
