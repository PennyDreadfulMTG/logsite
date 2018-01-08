import urllib
from collections import Counter

from flask import session, url_for

from . import APP, template

# pylint: disable=no-self-use, too-many-public-methods
class View:
    def template(self):
        return self.__class__.__name__.lower()

    def content(self):
        return template.render(self)

    def page(self):
        return template.render_name('page', self)

    def home_url(self):
        return url_for('home')

    def css_url(self):
        return 'https://pennydreadfulmagic.com/static/css/pd.css'

    def tooltips_url(self):
        return None
        # return url_for('static', filename='js/tooltips.js', v=self.commit_id())

    def js_url(self):
        return 'https://pennydreadfulmagic.com/static/js/pd.js'

    def menu(self):
        needs_tagging_badge = None
        menu = [
            {'name': 'Home', 'url': url_for('home')},
            {'name': 'About', 'url': url_for('about')},
        ]
        return menu

    def prepare(self):
        pass

    def favicon_url(self):
        return url_for('favicon', rest='.ico')

    def favicon_152_url(self):
        return url_for('favicon', rest='-152.png')

    def title(self):
        if not self.subtitle():
            return 'PDBot Logs'
        return '{subtitle} – PDBot Logs'.format(subtitle=self.subtitle())

    def subtitle(self):
        return None

    def commit_id(self):
        return APP.config['commit-id']
