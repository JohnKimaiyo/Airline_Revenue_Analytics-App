from flask import Blueprint, render_template, redirect, request
from flask_login import login_user
from werkzeug.security import check_password_hash
from app.database import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username='admin').first()
        if user and check_password_hash(user.password, 'admin1234'):
            login_user(user)
            return redirect('/dashboard')
    return render_template('login.html')
