from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('login.html')

@main.route('/admin-dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return "Access Denied", 403
    return render_template('admin.html')

@main.route('/student-dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        return "Access Denied", 403
    return render_template('student.html')

@main.route('/fixer-dashboard')
@login_required
def fixer_dashboard():
    if current_user.role != 'fixer':
        return "Access Denied", 403
    return render_template('fixer.html')
