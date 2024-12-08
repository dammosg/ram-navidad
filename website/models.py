from flask import render_template, flash, g
from werkzeug.security import generate_password_hash
import pyodbc
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func, desc
import secrets
import sqlite3

DATABASE = 'instance/christmas.db'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(150))
    full_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    gift_to = db.Column(db.Integer)
    first_time = db.Column(db.Boolean, default=True)

class sortedUsers(db.Model):
    user_id = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)


class dbFunctions:
    def query_db(query, args=(), one=False):
        cur = dbFunctions.get_db_dict().execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv

    def make_dicts(cursor, row):
        return dict((cursor.description[idx][0], value)
                    for idx, value in enumerate(row))
    
    def get_db():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
        return db
    
    def get_db_dict():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = dbFunctions.make_dicts
        return db
    


    def getBosses():
        return Users.query.filter(Users.user_level > 1, Users.user_level < 5).all()
    
