from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from .models import Users, dbFunctions
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userID = request.form.get('user')
        password = request.form.get('password')
        user = Users.query.filter_by(id=userID).first()
        if user:
            if user.password == password:
                flash("Logged in successfully.", category="success")
                login_user(user)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password.", category="error")
        else:
            flash("User does not exists.", category="error")
    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            id = request.form.get('id')
            pwd = secrets.token_hex(12)
            full_name = request.form.get('full_name')
            email = request.form.get('email')

            new_user = Users(id=id, password=pwd, full_name=full_name, email=email)
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            flash(f'Error: {e}, usuario no agregado a la base de datos.', category='error')
        finally:
            return redirect(url_for('auth.register'))
    return render_template('register.html')

