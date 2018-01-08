from logsite.view import View

# pylint: disable=no-self-use
class Home(View):
    def __init__(self, matches):
        self.matches = matches

    def subtitle(self):
        return None
