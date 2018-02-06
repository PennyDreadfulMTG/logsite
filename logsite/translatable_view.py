from . import APP, babel
from flask_babel import gettext
from flask import request

LANGUAGES = [str(locale) for locale in babel.list_translations()]

@babel.localeselector
def get_locale():
    result = request.accept_languages.best_match(LANGUAGES)
    return result

# pylint: disable=no-self-use
class TranslatableView:
    def TT_LATEST_MATCHES(self):
        return gettext("Latest Matches")

    def TT_MORE_MATCHES(self):
        return gettext("More matches…")
