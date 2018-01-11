import subprocess

from flask import Flask
APP = Flask(__name__)

from . import main, api

APP.config['commit-id'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'])
