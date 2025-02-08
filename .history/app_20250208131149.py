from flask import Flask # type: ignore
from flask_mysqldb import MySQL # type: ignore

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'college_issue_reporting'
mysql = MySQL(app)
from flask import Flask, jsonify, request # type: ignore
from flask_mysqldb import MySQL # type: ignore

app = Flask(__name__)

# Database Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'college_issue_reporting'

mysql = MySQL(app)

# Fetch All Issues
@app.route('/issues', methods=['GET'])
def get_issues():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM issues")
    issues = cur.fetchall()
    cur.close()
    return jsonify(issues)


if __name__ == '_main_':
 app.run(debug=True)
