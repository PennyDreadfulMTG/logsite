from werkzeug import exceptions
import os
import traceback
import subprocess

from flask import make_response, redirect, request, send_file, send_from_directory, session, url_for

from . import APP
from . import views, db, importing
from .data import match

@APP.route('/')
def home():
    importing.load_from_file()
    view = views.Home(match.get_recent_matches())
    return view.page()

@APP.route('/about/')
def about():
    view = views.About()
    return view.page()

@APP.route('/match/<id>/')
def show_match(id):
    pass

@APP.route('/favicon<rest>')
def favicon(rest):
    return send_from_directory(os.path.join(APP.root_path, 'static/images/favicon'), 'favicon{rest}'.format(rest=rest))

@APP.route('/api/gitpull', methods=['GET', 'POST'])
def gitpull():
    subprocess.check_output(['git', 'pull'])
    try:
        import uwsgi
        uwsgi.reload()
    except ImportError:
        pass
    view = views.About()
    return view.page()

@APP.route('/reset/db/')
def reset_db():
    db.db.drop_all()
    db.db.create_all()
    return home()

@APP.errorhandler(exceptions.NotFound)
def not_found(e):
    traceback.print_exception(e, e, None)
    view = views.NotFound(e)
    return view.page(), 404

@APP.errorhandler(exceptions.InternalServerError)
def internal_server_error(e):
    traceback.print_exception(e, e, None)
    view = views.InternalServerError(e)
    return view.page(), 500

@APP.teardown_request
def teardown_request(response):
    return response
