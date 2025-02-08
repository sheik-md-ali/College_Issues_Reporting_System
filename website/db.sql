CREATE DATABASE college_issue_reporting;
USE college_issue_reporting;


CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('student', 'fixer', 'admin') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Issues Table (Stores Reported Issues)
CREATE TABLE issues (
    issue_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    issue_type VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    media VARCHAR(255) NULL, -- Stores file path (image, video, etc.)
    severity ENUM('Low', 'Medium', 'High', 'Critical') NOT NULL,
    location VARCHAR(255) NOT NULL,
    status ENUM('Pending', 'In Progress', 'Resolved', 'Closed') DEFAULT 'Pending',
    reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_fixer_id INT NULL,  -- Assigned Fixer (nullable initially)
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_fixer_id) REFERENCES users(user_id) ON DELETE SET NULL
);

-- Fixers Table (Stores Assigned Fixers and Their Details)
CREATE TABLE fixers (
    fixer_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    department VARCHAR(100) NOT NULL,
    expertise VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Issue Updates Table (Tracks Fixer Updates)
CREATE TABLE issue_updates (
    update_id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id INT NOT NULL,
    fixer_id INT NOT NULL,
    update_text TEXT NOT NULL,
    update_status ENUM('Investigating', 'Fixing', 'Resolved') NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (issue_id) REFERENCES issues(issue_id) ON DELETE CASCADE,
    FOREIGN KEY (fixer_id) REFERENCES fixers(fixer_id) ON DELETE CASCADE
);
SHOW DATABASES;
USE college_issue_reporting;
SHOW TABLES;
DESC users;
DESC issues;
DESC fixers;
DESC issue_updates;
INSERT INTO users (name, email, password, role) VALUES
('Alice Johnson', 'alice@student.com', 'hashedpassword1', 'student'),
('Bob Fixer', 'bob@fixer.com', 'hashedpassword2', 'fixer'),
('Admin User', 'admin@college.com', 'hashedpassword3', 'admin');
INSERT INTO fixers (user_id, department, expertise) VALUES
(2, 'Maintenance', 'Electrical Repairs');
INSERT INTO issues (student_id, issue_type, description, severity, location) VALUES
(1, 'Plumbing', 'Leaking pipe in the dormitory', 'High', 'Dormitory Block A');
INSERT INTO issue_updates (issue_id, fixer_id, update_text, update_status) VALUES
(1, 1, 'Checked the leak, need to replace the pipe', 'Investigating');