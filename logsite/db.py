from typing import List

from flask import url_for
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa

from . import APP
from shared import configuration

APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{user}:{password}@{host}:{port}/{db}'.format(
    user=configuration.get('mysql_user'),
    password=configuration.get('mysql_passwd'),
    host=configuration.get('mysql_host'),
    port=configuration.get('mysql_port'),
    db=configuration.get('mysql_database'))

db = SQLAlchemy(APP)

match_players = db.Table('match_players',
    db.Column('match_id', db.Integer, db.ForeignKey('match.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

match_modules = db.Table('match_modules',
                         db.Column('match_id', db.Integer, db.ForeignKey('match.id'), primary_key=True),
                         db.Column('module_id', db.Integer, db.ForeignKey('module.id'), primary_key=True)
                        )

class Match(db.Model):
    __tablename__ = 'match'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=False)
    format_id = sa.Column(sa.Integer, sa.ForeignKey('format.id'))
    comment = sa.Column(sa.String(200))
    start_time = db.Column(sa.DateTime)
    end_time = db.Column(sa.DateTime)
    players = db.relationship('User', secondary=match_players)
    modules = db.relationship('Module', secondary=match_modules)
    games = db.relationship('Game', backref='match')
    format = db.relationship('Format')

    def url(self):
        return url_for('show_match', match_id=self.id)

    def format_name(self):
        return self.format.get_name()

    def host(self):
        return self.players[0]

    def other_players(self):
        return self.players[1:]

    def other_player_names(self):
        return [p.name for p in self.other_players()]

class Game(db.Model):
    __tablename__ = 'game'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=False)
    match_id = sa.Column(sa.Integer, db.ForeignKey('match.id'), nullable=False)
    log = sa.Column(sa.Text)

class User(db.Model):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(60))
    discord_id = sa.Column(sa.String(200))

class Format(db.Model):
    __tablename__ = 'format'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(40))
    friendly_name = sa.Column(sa.String(20))

    def get_name(self):
        if self.friendly_name:
            return self.friendly_name
        return self.name

class Module(db.Model):
    __tablename__ = 'module'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50))

def Commit():
    return db.session.commit()

def Add(item):
    return db.session.add(item)

def Delete(item):
    return db.session.delete(item)

def get_or_insert_format(name: str) -> Format:
    local = Format.query.filter_by(name=name).one_or_none()
    if local is not None:
        return local
    local = Format(name=name)
    Add(local)
    Commit()
    return local

def get_or_insert_module(name: str) -> Module:
    local = Module.query.filter_by(name=name).one_or_none()
    if local is not None:
        return local
    local = Module(name=name)
    Add(local)
    Commit()
    return local

def get_or_insert_user(name: str) -> User:
    local = User.query.filter_by(name=name).one_or_none()
    if local is not None:
        return local
    local = User(name=name)
    Add(local)
    Commit()
    return local

def insert_game(game_id, match_id, game_lines) -> None:
    local = Game(id=game_id, match_id=match_id, log=game_lines)
    Add(local)
    Commit()
