import json

from flask import Response, request, session, url_for

from . import APP
from shared import configuration
from shared.serialization import extra_serializer

@APP.route('/api/admin/')
def admin():
    return return_json(session.get('admin'))

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
