import subprocess

from flask import Flask
from flask_babel import Babel

APP = Flask(__name__)
babel = Babel(APP)

from . import main, api, localization # pylint: disable=wrong-import-position, unused-import

APP.config['commit-id'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'])

