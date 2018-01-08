import json
import urllib.request

import requests

from cachecontrol import CacheControl
from cachecontrol.caches.file_cache import FileCache

from shared import configuration

SESSION = requests.Session()

def fetch(url, character_encoding=None, force=False):
    if SESSION is None:
        setup()
    headers = {}
    if force:
        headers['Cache-Control'] = 'no-cache'
    print('Fetching {url} ({cache})'.format(url=url, cache='no cache' if force else 'cache ok'))
    try:
        response = SESSION.get(url, headers=headers)
        if character_encoding is not None:
            response.encoding = character_encoding
        return response.text
    except (urllib.error.HTTPError, requests.exceptions.ConnectionError) as e:
        raise FetchException(e)


def fetch_json(url, character_encoding=None):
    try:
        blob = fetch(url, character_encoding)
        return json.loads(blob)
    except json.decoder.JSONDecodeError:
        print('Failed to load JSON:\n{0}'.format(blob))
        raise

class FetchException(Exception):
    pass

def store(url, filename):
    if SESSION is None:
        setup()
    print('Downloading {0}'.format(url))
    request = SESSION.get(url, stream=True)
    with open(filename, 'wb') as file:
        for chunk in request.iter_content(1024):
            file.write(chunk)

def setup():
    global SESSION
    SESSION = CacheControl(requests.Session())
