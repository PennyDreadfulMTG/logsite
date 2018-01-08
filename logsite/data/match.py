from typing import List

from .. import db
from ..db import Match

def create_match(match_id: int, format_name: str, comment: str, modules: List[str], players: List[str]) -> Match:
    format_id = db.get_or_insert_format(format_name).id
    local = Match(id=match_id, format_id=format_id, comment=comment)
    modules = [db.get_or_insert_module(mod) for mod in modules]
    local.modules = modules
    local.players = [db.get_or_insert_user(user) for user in players]
    db.Add(local)
    db.Commit()
    return local

def get_match(match_id: int) -> Match:
    return Match.query.filter_by(id=match_id).one_or_none()

def get_recent_matches(count: int=10) -> List[Match]:
    return Match.query.order_by(Match.id.desc()).limit(count).all()
