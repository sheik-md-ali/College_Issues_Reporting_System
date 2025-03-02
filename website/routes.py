from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, current_app, jsonify, send_from_directory
from flask_login import login_required, current_user
from website.models import Feedback,Issue, User
from . import db
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('login.html')

@main.route("/about")
def about():
    return render_template("about.html")

@main.route('/admin-dashboard')
def admin_dashboard():
    issues = Issue.query.all()
    fixers = User.query.filter_by(role='fixer').all()
    feedbacks = Feedback.query.all()  # Fetch all feedback entries
    total_issues = Issue.query.count()
    resolved_issues = Issue.query.filter_by(status='Resolved').count()
    pending_issues = total_issues - resolved_issues

    return render_template('admin.html', 
                           issues=issues, 
                           fixers=fixers,
                           feedbacks=feedbacks,  # Pass feedbacks to the template
                           total_issues=total_issues, 
                           resolved_issues=resolved_issues, 
                           pending_issues=pending_issues)

@main.route('/delete_fixer/<int:fixer_id>', methods=['POST'])
def delete_fixer(fixer_id):
    fixer = User.query.get(fixer_id)
    if fixer and fixer.role == 'fixer':
        db.session.delete(fixer)
        db.session.commit()
        return jsonify({"success": True, "message": "Fixer deleted successfully."})
    return jsonify({"success": False, "message": "Fixer not found or cannot be deleted."})


@main.route('/admin/assign_fixer', methods=['POST'])
def assign_fixer():
    issue_id = request.form.get('issue_id')
    fixer_id = request.form.get('fixer_id')

    issue = Issue.query.get(issue_id)
    fixer = User.query.get(fixer_id)

    if issue and fixer and fixer.role == 'fixer':
        issue.fixer_assigned = fixer.id
        db.session.commit()
        return jsonify({'success': True, 'message': 'Fixer assigned successfully'})

    return jsonify({'success': False, 'message': 'Failed to assign fixer'})

@main.route('/admin/resolve_issue/<int:issue_id>', methods=['POST'])
def resolve_issue(issue_id):
    issue = Issue.query.get(issue_id)
    if issue:
        issue.status = 'Resolved'
        db.session.commit()
        flash('Issue marked as resolved!', 'success')

    return redirect(url_for('main.admin_dashboard'))

@main.route('/admin/add_fixer', methods=['POST'])
@login_required
def add_fixer():
    if current_user.role != 'admin':
        return "Access Denied", 403

    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')  # Admin sets initial password
    hashed_password = generate_password_hash(password, method='scrypt')

    # Check if fixer already exists
    existing_fixer = User.query.filter_by(email=email).first()
    if existing_fixer:
        flash("Fixer already exists!", "danger")
        return redirect(url_for('main.admin_dashboard'))

    fixer = User(name=name, email=email, password_hash=hashed_password, role="fixer")
    db.session.add(fixer)
    db.session.commit()

    flash("Fixer added successfully!", "success")
    return redirect(url_for('main.admin_dashboard'))



@main.route('/fixer-dashboard', methods=['GET', 'POST'])
@login_required
def fixer_dashboard():
    # Ensure only fixers can access this route
    if current_user.role != 'fixer':
        return "Access Denied", 403

    # Fetch issues assigned to the logged-in fixer
    fixer_id = current_user.id
    issues = Issue.query.filter_by(fixer_assigned=fixer_id).all()

    # Handle status update
    if request.method == 'POST':
        issue_id = request.form.get('issue_id')
        new_status = request.form.get('status')
        
        # Update the issue status
        issue = Issue.query.get(issue_id)
        if issue and issue.fixer_assigned == fixer_id:  # Ensure the issue belongs to the fixer
            issue.status = new_status
            db.session.commit()
            flash('Issue status updated successfully!', 'success')
        else:
            flash('Invalid request or issue not found.', 'error')

        return redirect(url_for('main.fixer_dashboard'))

    return render_template('fixer.html', issues=issues)


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

    if 'media' in request.files and request.files['media'].filename != '':
        file = request.files['media']
        if allowed_file(file.filename):  
            filename = secure_filename(file.filename)  
            upload_folder = os.path.join(current_app.root_path, 'static/uploads')  
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)  
            file.save(os.path.join(upload_folder, filename))  
            media_filename = filename  
        else:
            flash("Invalid file type. Only images are allowed.", "danger")
            return redirect(url_for('main.student_dashboard'))

    # Store only the filename
    issue = Issue(
        student_id=current_user.id,
        issue_type=request.form.get('issue_type'),
        description=request.form.get('description'),
        severity=request.form.get('severity'),
        location=request.form.get('location'),
        media_filename=media_filename  # Store only filename
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

@main.route('/delete_issue/<int:issue_id>', methods=['POST'])
@login_required
def delete_issue(issue_id):
    issue = Issue.query.get(issue_id)

    # Allow admin to delete any issue
    if issue and (current_user.role == "admin" or issue.student_id == current_user.id):  
        if issue.media_filename:
            upload_folder = os.path.join(current_app.root_path, 'static/uploads')
            file_path = os.path.join(upload_folder, issue.media_filename)

            if os.path.exists(file_path):
                os.remove(file_path)

        db.session.delete(issue)
        db.session.commit()

        return jsonify({"success": True})

    return jsonify({"success": False}), 403



@main.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(current_app.root_path, 'static/uploads'), filename)
