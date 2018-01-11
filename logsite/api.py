import json

from flask import Response, request, session, url_for

from . import APP, importing
from .data import match
from shared import configuration
from shared.serialization import extra_serializer

@APP.route('/api/admin/')
def admin():
    return return_json(session.get('admin'))

@APP.route('/api/matchExists/<match_id>')
def match_exists(match_id):
    return return_json(match.get_match(match_id) is not None)

@APP.route('/api/upload')
def upload():
    error = validate_api_key()
    if error:
        return error
    match_id = int(request.form['match_id'])
    if match.get_match(match_id) is not None:
        return generate_error('already_imported', 'Match is already in DB')
    lines = request.form['lines']
    importing.import_log(lines, match_id)
    return return_json({'success': True})


def generate_error(code, msg):
    return {'error': True, 'code': code, 'msg': msg}

def return_json(content, status=200):
    content = json.dumps(content, default=extra_serializer)
    r = Response(response=content, status=status, mimetype="application/json")
    return r

def validate_api_key():
    if request.form.get('api_token', None) == configuration.get('pdbot_api_token'):
        return None
    return return_json(generate_error('UNAUTHORIZED', 'Invalid API key'), status=403)
