from sqlalchemy import func

from . import db, APP
from .data import match
from .api import return_json
from shared import dtutil

@APP.route('/stats/')
def stats():
    val = {}
    val['formats'] = {}
    base_query = db.db.session.query(match.Match, func.count(match.Match.format_id))
    for m in base_query.group_by(match.Match.format_id).order_by(func.count(match.Match.format_id).desc()).all():
        f = m[0].format
        val['formats'][f.name] = {}
        val['formats'][f.name]['name'] = f.get_name()
        val['formats'][f.name]['num_matches'] = m[1]
    last_week = dtutil.now() - dtutil.ts2dt(7 * 24 * 60 * 60)
    for m in base_query.group_by(match.Match.format_id).filter(match.Match.start_time > last_week).order_by(func.count(match.Match.format_id).desc()).all():
        f = m[0].format
        val['formats'][f.name]['last_week'] = m[1]
    last_month = dtutil.now() - dtutil.ts2dt(30 * 24 * 60 * 60)
    for m in base_query.group_by(match.Match.format_id).filter(match.Match.start_time > last_month).order_by(func.count(match.Match.format_id).desc()).all():
        f = m[0].format
        val['formats'][f.name]['last_month'] = m[1]
    # for u in db.db.session.query(): #users where mathc in last month
        # val['formats'][f.name]['recent_players']


    return return_json(val)

