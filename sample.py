from werkzeug.security import generate_password_hash
from website import create_app, db
from website.models import User

app = create_app()  # If using an app factory

with app.app_context():
    users_data = [
        {"email": "admin@example.com", "password": "admin123", "role": "admin"},
        {"email": "student@example.com", "password": "student123", "role": "student"},
        {"email": "fixer@example.com", "password": "fixer123", "role": "fixer"},
    ]

    for user_data in users_data:
        user = User.query.filter_by(email=user_data["email"]).first()
        hashed_password = generate_password_hash(user_data["password"], method="scrypt")

        if user:
            user.password_hash = hashed_password
            print(f"Updated password for {user_data['email']}")
        else:
            user = User(email=user_data["email"], password_hash=hashed_password, role=user_data["role"])
            db.session.add(user)
            print(f"Created new user: {user_data['email']} ({user_data['role']})")

    db.session.commit()
    print("User creation/update process completed.")
