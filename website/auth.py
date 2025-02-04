from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Debugging: Print received email and password (Avoid printing password in production)
        print(f"Received login attempt - Email: {email}")

        user = User.query.filter_by(email=email).first()

        if user:
            print(f"User found: {user.email}, Role: {user.role}")
        else:
            print("No user found with this email")

        if user and user.check_password(password):
            print("Password matched!")
            login_user(user)
            flash("Login successful!", "success")

            if user.role == 'admin':
                print("Redirecting to admin dashboard")
                return redirect(url_for('main.admin_dashboard'))
            elif user.role == 'student':
                print("Redirecting to student dashboard")
                return redirect(url_for('main.student_dashboard'))
            else:
                print("Redirecting to fixer dashboard")
                return redirect(url_for('main.fixer_dashboard'))
        else:
            print("Invalid credentials")
            flash('Invalid credentials, please try again.', 'danger')

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    print("User logged out")
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))
