import glob
import os
import re
import shutil
from typing import List

from .data import game, match

REGEX_GAME_HEADER = r'== Game \d \((?P<id>\d+)\) =='
REGEX_SWITCHEROO = r'!! Warning, unexpected game 3 !!'

def load_from_file():
    """"Imports a log from an on-disk file"""
    files = glob.glob('import/queue/*.txt')
    for fname in files:
        match_id = int(os.path.basename(fname).split('.')[0])
        if match.get_match(match_id) is None:
            with open(fname) as fhandle:
                lines = fhandle.readlines()
                import_log(lines, match_id)
            shutil.move(fname, 'import/processed/{0}.txt'.format(match_id))
            return

def import_log(lines: List[str], match_id: int):
    """Processes a log"""
    lines = [line.strip('\r\n') for line in lines]
    print('importing {0}'.format(match_id))
    format_name = lines[0]
    comment = lines[1]
    modules = [mod.strip() for mod in lines[2].split(',')]
    players = [player.strip() for player in lines[3].split(',')]
    local = match.get_match(match_id)
    if local is None:
        local = match.create_match(match_id, format_name, comment, modules, players)
    if local.has_unexpected_third_game is None:
        local.has_unexpected_third_game = False
    lines = lines[4:]
    while lines[0] != '':
        lines = lines[1:]
    game_id = 0
    game_lines: List[str] = list()
    for line in lines:
        m = re.match(REGEX_GAME_HEADER, line)
        if m:
            new_id = int(m.group('id'))
            if game_id == 0:
                game_id = new_id
            elif new_id != game_id:
                game.insert_game(game_id, match_id, '\n'.join(game_lines))
                game_id = new_id
                game_lines = list()
        elif re.match(REGEX_SWITCHEROO, line):
            local.has_unexpected_third_game = True
            game_lines.append(line)
        else:
            game_lines.append(line)
    game.insert_game(game_id, match_id, '\n'.join(game_lines))
