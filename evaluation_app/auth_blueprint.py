from flask import Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from flask import render_template, request, url_for, redirect, flash
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash, generate_password_hash
from utils import save_action
import os

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            global root_dfd_folder
            root_dfd_folder = "static/dfd/" + str(current_user.id)
            
            # Check if the folder exists, if not, create it
            if not os.path.exists(root_dfd_folder):
                os.makedirs(root_dfd_folder)
                
            save_action("login")
            flash('You have successfully logged in!')
            return redirect(url_for('index'))
        
        flash('Invalid username or password')
        
    return render_template('login.html')
  
@auth_blueprint.route('/logout')
@login_required
def logout():
    save_action("logout")
    logout_user()
    root_dfd_folder = "static/dfd"
    flash('You have successfully logged out!')
    return redirect(url_for('auth.login'))


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_confirmation = request.form['password_confirmation']
        consent = request.form.get('consent')
        if not consent:
            flash('You must agree to the informed consent form to register.')
            return redirect(url_for('auth.register'))
        if password != password_confirmation:
            flash('Passwords do not match')
            return redirect(url_for('auth.register'))
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('This username is already taken')
            return redirect(url_for('auth.register'))
        
            
        user = User(username=username, email=email, password=generate_password_hash(password), is_active=True, has_consented=True)
        db.session.add(user)
        db.session.commit()
        
        flash('You have successfully registered!')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')