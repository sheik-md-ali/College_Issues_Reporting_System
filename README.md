# 📌 College_Issues_Reporting_System

The **College Issues Reporting System** is a web-based application built using **HTML, CSS, JavaScript, Python (Flask), and SQL**. It provides a streamlined way for students to report issues within the college, allowing the admin to assign these issues to designated fixers who will resolve them efficiently.

---

## ✨ Key Features

- **Student Issue Reporting:** Students can submit complaints or issues related to campus facilities, academic concerns, or other college-related matters.  
- **Admin Dashboard:** The admin has full control to review, categorize, and assign reported issues to the appropriate fixer.  
- **Fixer Role:** Assigned fixers receive issue notifications, work on resolving them, and update the status once completed.  
- **Real-time Status Tracking:** Students and admins can track the progress of reported issues from submission to resolution.  
- **User Authentication:** Secure login system for students, admins, and fixers to ensure authorized access.  
- **Database Integration:** All issues, user details, and status updates are stored in a structured SQL database for efficient management.

---

## 📦 Project Setup

### 🔁 Clone the Repository

```bash
git clone https://github.com/sheik-md-ali/College_Issues_Reporting_System.git
cd College_Issues_Reporting_System
```

### 🐍 (Optional) Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # On macOS/Linux
venv\Scripts\activate         # On Windows
```

### 📦 Install Python Dependencies

```bash
pip install -r requirements.txt
```

Make sure your `requirements.txt` contains the following:

```
Flask
Flask-Login
Flask-SQLAlchemy
mysql-connector-python
Werkzeug
SQLAlchemy
```

---

## 🛠️ Configure Database Credentials

Open `website/__init__.py` and update the following configuration with your actual MySQL credentials:


Make sure your database credentials match:

- **DB_NAME:** `clgissue`
- **DB_USER:** `root`
- **DB_PASSWORD:** `passowrd$$`
- **DB_HOST:** `localhost`

You can create the database in MySQL with:

```sql
CREATE DATABASE clgissue;
```

---

## 🚀 Run the Application

After installing the dependencies and configuring the database:

```bash
python app.py
```

Then open your browser and go to:  
📍 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📂 Project Structure

```
College_Issues_Reporting_System/
│
├── app.py                  # Entry point of the Flask app
├── requirements.txt        # Project dependencies
├── website/                # Main application package
│   ├── __init__.py         # Initializes Flask app and DB
│   ├── models.py           # Database models (User, Issue, Feedback, etc.)
│   ├── auth.py             # Authentication routes
│   ├── views.py            # Main view routes
│   ├── templates/          # HTML templates
│   └── static/             # Static assets (CSS, JS, Images)
```

---

## 🚀 Future Enhancements

- **Email & SMS Notifications** for updates on issue status.  
- **Priority-Based Issue Handling** to ensure critical issues are resolved faster.  
- **Feedback System** for students to rate the resolution process.  
- **Analytics Dashboard** for admins to track trends and improve response times.  

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request.

---

## 📧 Contact

If you face any issues or want to suggest improvements, feel free to open an issue in this repository.
