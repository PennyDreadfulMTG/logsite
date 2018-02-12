from flask_babel import gettext

from .. import babel
from logsite.view import View

# pylint: disable=no-self-use
class About(View):
    def subtitle(self) -> str:
        return gettext('About')

    def languages(self) -> str:
        return ", ".join([locale.display_name for locale in babel.list_translations()])

    def TT_ABOUT_PDBOT(self) -> str:
        return gettext("About PDBot")

    def TT_ABOUT_DESC(self) -> str:
        return gettext("PDBot is a robot that observes people playing games on Magic Online, and provides the role of judge, informing players with legality and bug information")

    def TT_TRANSLATED_INTO(self) -> str:
        return gettext("This site is currently translated into:")

    def TT_HELP_TRANSLATE(self) -> str:
        return gettext("Help us translate the site into your language")
