import json, subprocess

from flask import Response, request, session, url_for

from . import APP, importing
from .data import match, game
from shared import configuration
from shared.serialization import extra_serializer

@APP.route('/api/admin/')
def admin():
    return return_json(session.get('admin'))

@APP.route('/api/matchExists/<match_id>')
def match_exists(match_id):
    local = match.get_match(match_id)
    if local is not None:
        final: game.Game = local.games[-1]
        return return_json("Match Winner" in final.log)
    return return_json(False)

@APP.route('/api/upload', methods=['POST'])
def upload():
    error = validate_api_key()
    if error:
        return error
    match_id = int(request.form['match_id'])
    lines = request.form['lines']
    importing.import_log(lines.split('\n'), match_id)
    return return_json({'success': True})

@APP.route('/api/gitpull', methods=['GET', 'POST'])
def gitpull():
    subprocess.check_output(['git', 'pull'])
    try:
        import uwsgi
        uwsgi.reload()
    except ImportError:
        pass
    return return_json(APP.config['commit-id'])

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
