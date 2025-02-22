from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, current_app
from flask_login import login_required, current_user
from website.models import Feedback,Issue
from . import db
from werkzeug.utils import secure_filename
import os
from flask import jsonify
import io

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


@main.route('/fixer-dashboard')
@login_required
def fixer_dashboard():
    if current_user.role != 'fixer':
        return "Access Denied", 403
    return render_template('fixer.html')


@main.route('/student-dashboard')
@login_required
def student_dashboard():
    issues = Issue.query.filter_by(student_id=current_user.id).all()
    return render_template('student.html', issues=issues)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



UPLOAD_FOLDER = "static/uploads"

@main.route('/submit_issue', methods=['POST'])
@login_required
def submit_issue():
    media_filename = None  
    media_path = None  

    if 'media' in request.files and request.files['media'].filename != '':
        file = request.files['media']
        if allowed_file(file.filename):  # Ensure valid file type
            filename = secure_filename(file.filename)  
            upload_folder = current_app.config['UPLOAD_FOLDER']  # Get upload folder from config
            media_path = os.path.join(upload_folder, filename).replace("\\", "/") 
            file.save(media_path)  
            media_filename = filename  
        else:
            flash("Invalid file type. Only images are allowed.", "danger")
            return redirect(url_for('main.student_dashboard'))

    # Create and store issue
    issue = Issue(
        student_id=current_user.id,
        issue_type=request.form.get('issue_type'),
        description=request.form.get('description'),
        severity=request.form.get('severity'),
        location=request.form.get('location'),
        media_path=media_path,  
        media_filename=media_filename  
    )
    db.session.add(issue)
    db.session.commit()
    
    flash("Issue submitted successfully!", "success")
    return redirect(url_for('main.student_dashboard'))


@main.route('/submit_feedback', methods=['POST'])
@login_required
def submit_feedback():
    rating_str = request.form.get('rating')  # Get the rating value as a string
    rating = int(rating_str.split()[0]) if rating_str else None  # Extract the numeric part and convert to int

    feedback = Feedback(
        student_id=current_user.id,
        rating=rating,
        feedback_text=request.form.get('feedback')
    )
    db.session.add(feedback)
    db.session.commit()
    flash("Feedback submitted successfully!", "success")
    return redirect(url_for('main.student_dashboard'))

from flask import send_from_directory

@main.route('/get_image/<int:issue_id>')
@login_required
def get_image(issue_id):
    issue = Issue.query.get(issue_id)
    if issue and issue.media_path:
        return send_from_directory(UPLOAD_FOLDER, issue.media_filename)
    return "No Image", 404


@main.route('/delete_issue/<int:issue_id>', methods=['POST'])
@login_required
def delete_issue(issue_id):
    issue = Issue.query.get(issue_id)
    if issue and issue.student_id == current_user.id:
        db.session.delete(issue)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False}), 403