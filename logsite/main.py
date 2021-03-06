import os
import subprocess
import traceback

from flask import (redirect, request, send_file, send_from_directory, session,
                   url_for)
from werkzeug import exceptions

from . import APP, db, importing, views
from .data import match


@APP.route('/')
def home():
    importing.load_from_file()
    view = views.Home()
    return view.page()

@APP.route('/about/')
def about():
    view = views.About()
    return view.page()

@APP.route('/people/')
def people():
    view = views.People()
    return view.page()

@APP.route('/people/<person>/')
def show_person(person=None):
    view = views.Matches(person=person)
    return view.page()

@APP.route('/matches/')
def matches():
    view = views.Matches()
    return view.page()

@APP.route('/match/<match_id>/')
def show_match(match_id):
    view = views.Match(match.get_match(match_id))
    return view.page()

@APP.route('/favicon<rest>')
def favicon(rest):
    return send_from_directory(os.path.join(APP.root_path, 'static/images/favicon'), 'favicon{rest}'.format(rest=rest))

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
