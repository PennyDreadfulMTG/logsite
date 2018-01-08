from shared import fetcher_internal

IGNORED_SETS = ['sum', 'chr', 'ath']

def card_by_mtgo(id):
    results = fetcher_internal.fetch_json('https://api.scryfall.com/cards/mtgo/{0}'.format(id))
    return results

def card_by_id(id):
    results = fetcher_internal.fetch_json('https://api.scryfall.com/cards/{0}'.format(id))
    return results

def all_cards_named(name):
    uri = 'https://api.scryfall.com/cards/search?q=%2B%2B{0}'.format(name)
    return fetch_paginated_list(uri)

def all_sets():
    return fetch_paginated_list('https://api.scryfall.com/sets')

def all_cards_from_set(setcode):
    if setcode in IGNORED_SETS:
        return []
    return fetch_paginated_list('https://api.scryfall.com/cards/search?q=%2B%2Be%3A{0}'.format(setcode))

def fetch_paginated_list(uri):
    results = fetcher_internal.fetch_json(uri)
    data = results['data']
    while results['has_more']:
        uri = results['next_page']
        results = fetcher_internal.fetch_json(uri)
        data += results['data']
    return data
