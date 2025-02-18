from flask import request, jsonify, flash, redirect, url_for, render_template
from flask_login import login_user, login_required, logout_user, current_user
import re
from email_validator import validate_email, EmailNotValidError
from hashlib import sha256
from datetime import datetime, timedelta

from config import Config
from app.auth import bp
from app.extensions import db
from app.models.user import User, OnlineUser
from app.auth.forms import LoginForm, RegisterForm

@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        ipaddress = request.headers.get('X-Forwarded-For', request.headers.get('X-Real-IP', request.remote_addr))
        online_ip = OnlineUser.query.filter_by(ipaddress=ipaddress).first()
        online_user = OnlineUser.query.filter_by(user_id=current_user.id).first()
        if online_user:
            return redirect(url_for("user.dashboard"))

    if request.method == 'POST' and form.validate_on_submit(): #validation check
        password = form.password.data
        if is_email(form.email_or_phone.data):
            user = User.query.filter_by(email=form.email_or_phone.data).first()
        elif is_phone_number(form.email_or_phone.data):
            user = User.query.filter_by(phone_number=form.email_or_phone.data).first()
        else:
            flash('Please Enter a Valid Email or Phone Number!', "error")  
            return render_template('auth/login.html', form=form), 200
        
        if user and user.check_password(password):
            online_user = OnlineUser.query.filter_by(user_id=user.id).first()
            
            if not online_user:
                ipaddress = request.headers.get('X-Forwarded-For', request.headers.get('X-Real-IP', request.remote_addr))
                online_ip = OnlineUser.query.filter_by(ipaddress=ipaddress).first()
        
                if not online_ip:            
                    db.session.add(OnlineUser(user_id=user.id, ipaddress=ipaddress, logindatetime=datetime.utcnow()))
                    db.session.commit()
                    flash('Logged in Successfully!', "success")
                    login_user(user)
                    return redirect(url_for("user.dashboard"))
                else:
                    flash('IP Already Online!', "error")  
            else:
                flash('Already Logged In!', "error")
        else:
            flash('Invalid Credentials!', "error")
            
    return render_template('auth/login.html', form=form), 200

@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                flash('Email already registered!', "error")
            else:
                db.session.add(User(birthdate=form.birthdate.data, phone_number=form.phone_number.data, firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, password=form.password.data))
                db.session.commit()

                flash('Registered Successfully!', "success")
                return redirect(url_for("auth.login"))
        elif form.errors:
            flash(form.errors["password"][0], "error")

    return render_template("auth/register.html", form=form), 200

@bp.route("/logout", methods=["GET"])
@login_required
def logout():
    user = OnlineUser.query.filter_by(user_id=current_user.id).first()

    if user:
        flash('Successfully Logged Out!', "success")
        db.session.delete(user)
        db.session.commit()
        logout_user()
        return redirect("/auth/login")

    return jsonify(status="not logged in yet")

def is_email(identifier):
    try:
        validate_email(identifier)  # Tries to validate email
        return True
    except EmailNotValidError:
        return False
    
def is_phone_number(identifier):
    return re.fullmatch(r'^\+?\d{10}$', identifier) is not None