from sqlalchemy import func, text

from shared import dtutil

from . import APP, db
from .api import return_json
from .data import match


@APP.route('/stats.json')
@APP.route('/stats')
def stats():
    val = {}
    last_switcheroo = match.Match.query.filter(match.Match.has_unexpected_third_game == True).order_by(match.Match.id.desc()).first().start_time
    val['last_switcheroo'] = dtutil.dt2ts(last_switcheroo)

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
        val['formats'][f.name]['last_week'] = {}
        val['formats'][f.name]['last_week']['num_matches'] = m[1]
        stmt = text("""select b.* from user as b
                        inner join (
                            select user.id from user
                            left join match_players
                            ON match_players.user_id = user.id
                            left join `match`
                            on `match`.id = match_players.match_id
                            where `match`.format_id = :fid and `match`.start_time is not null and
                            `match`.start_time > date_sub(now(), interval 7 DAY)
                            group by user.id
                        ) as a on a.id = b.id
                        """)
        players = db.db.session.query(db.User).from_statement(stmt).params(fid=f.id).all()
        val['formats'][f.name]['last_week']['recent_players'] = [p.name for p in players]
    last_month = dtutil.now() - dtutil.ts2dt(30 * 24 * 60 * 60)
    for m in base_query.group_by(match.Match.format_id).filter(match.Match.start_time > last_month).order_by(func.count(match.Match.format_id).desc()).all():
        f = m[0].format
        val['formats'][f.name]['last_month'] = {}
        val['formats'][f.name]['last_month']['num_matches'] = m[1]
        stmt = text("""select b.* from user as b
                        inner join (
                            select user.id from user
                            left join match_players
                            ON match_players.user_id = user.id
                            left join `match`
                            on `match`.id = match_players.match_id
                            where `match`.format_id = :fid and `match`.start_time is not null and
                            `match`.start_time > date_sub(now(), interval 30 DAY)
                            group by user.id
                        ) as a on a.id = b.id
                        """)
        players = db.db.session.query(db.User).from_statement(stmt).params(fid=f.id).all()
        val['formats'][f.name]['last_month']['recent_players'] = [p.name for p in players]
    return return_json(val)
