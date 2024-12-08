from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from sqlalchemy.sql import text
from .models import Users, sortedUsers, dbFunctions
from . import db
from random import randrange

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user, gift_user=Users.query.get(current_user.gift_to))

@views.route('/working')
def working():
    return render_template('working.html')

@views.route('/users')
def users():
    users = Users.query.all()
    return render_template('users.html', users=users, user=current_user)

@views.route('/get-person')
def get_person():
    current_user.first_time = 0
    db.session.commit()
    if current_user.gift_to:
        return redirect(url_for('views.home'))
    gift_users = dbFunctions.query_db('SELECT * FROM sorted_users')
    gift_to = None
    for count, u in enumerate(gift_users):
        if len(gift_users) == 2:
            users_not_sorted = Users.query.filter_by(gift_to=None).all()
            for uns in users_not_sorted:
                if uns.id == u['user_id']:
                    gift_to = gift_users[count]
                    break
            if gift_to != None:
                break
        elif u['user_id'] == current_user.id:
            gift_users.pop(count)
            break
    if gift_to == None:
        gift_to = gift_users[randrange(len(gift_users))]
    
    current_user.gift_to = gift_to['user_id']
    sortedUsers.query.filter_by(user_id=gift_to['user_id']).delete()
    db.session.commit()

    return redirect(url_for('views.home'))

