from flask import Flask, render_template, jsonify, request, redirect, session, url_for
import sqlite3
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"

ADMIN_EMAIL = "rashmivishwakarma613@gmail.com"
DB_NAME = "rgpv_data.db"

# ---------------- DB CONNECTION ----------------
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# 🔥 FIRST PAGE (Landing Page)
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- INIT TABLES ----------------
def init_tables():
    conn = get_db_connection()

    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    ''')

    conn.execute('''
       CREATE TABLE IF NOT EXISTS logs (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           email TEXT,
           login_time TEXT,
           logout_time TEXT,
           is_deleted INTEGER DEFAULT 0
    )
''')

    conn.commit()
    conn.close()

init_tables()

# ---------------- ROUTES ----------------

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

# -------- REGISTER --------
@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = generate_password_hash(request.form['password'])

    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        conn.commit()
    except:
        return "⚠️ Email already exists!"
    finally:
        conn.close()

    return redirect('/')

# -------- LOGIN --------
@app.route('/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    ).fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        session['user'] = user['email']

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO logs (email, login_time) VALUES (?, ?)",
            (email, str(datetime.datetime.now()))
        )
        conn.commit()
        conn.close()

        return redirect('/dashboard')

    return "❌ Invalid Email or Password"

# -------- DASHBOARD --------
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template('dashboard.html')

# -------- ANALYSIS --------
@app.route('/analysis')
def analysis():
    if 'user' not in session:
        return redirect('/')
    is_admin = session.get('user') == ADMIN_EMAIL
    return render_template('analysis.html', is_admin=is_admin)

# -------- LOGS --------
@app.route('/logs')
def view_logs():
    if session.get('user') != ADMIN_EMAIL:
        return "❌ Access Denied"

    conn = get_db_connection()
    logs = conn.execute("SELECT * FROM logs WHERE is_deleted=0 ORDER BY id DESC").fetchall()
    conn.close()

    return render_template('logs.html', logs=logs)

@app.route('/delete_log/<int:log_id>')
def delete_log(log_id):
    if session.get('user') != ADMIN_EMAIL:
        return "❌ Access Denied"

    conn = get_db_connection()
    conn.execute("UPDATE logs SET is_deleted=1 WHERE id=?", (log_id,))
    conn.commit()
    conn.close()

    return redirect('/logs')

# restore_log api
@app.route('/restore_log/<int:log_id>')
def restore_log(log_id):
    if session.get('user') != ADMIN_EMAIL:
        return "❌ Access Denied"

    conn = get_db_connection()
    conn.execute("UPDATE logs SET is_deleted=0 WHERE id=?", (log_id,))
    conn.commit()
    conn.close()

    return redirect('/logs')

@app.route('/admin')
def admin_panel():
    if session.get('user') != ADMIN_EMAIL:
        return "❌ Access Denied"

    conn = get_db_connection()

    total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    total_logs = conn.execute("SELECT COUNT(*) FROM logs WHERE is_deleted=0").fetchone()[0]

    conn.close()

    return render_template('admin.html', 
                           total_users=total_users,
                           total_logs=total_logs)

# -------- LOGOUT --------
@app.route('/logout')
def logout():
    if 'user' in session:
        email = session['user']

        conn = get_db_connection()
        conn.execute("""
            UPDATE logs 
            SET logout_time = ?
            WHERE email = ? AND logout_time IS NULL
        """, (str(datetime.datetime.now()), email))

        conn.commit()
        conn.close()

        session.pop('user', None)

    return redirect('/')

# ---------------- APIs ----------------

# ✅ SUBJECTS (Flexible Logic)
@app.route('/api/subjects/<semester>')
@app.route('/api/subjects/<semester>')
def get_subjects(semester):
    conn = get_db_connection()
    # Number nikalna: 'Semester 1' -> '1'
    sem_num = ''.join(filter(str.isdigit, semester)) 
    
    # Simple query jo Semester ke naam mein 1, 2, 6 etc dhoondti hai
    query = """
        SELECT DISTINCT s.name
        FROM subjects s
        JOIN semesters sem ON s.semester_id = sem.id
        WHERE sem.name LIKE ?
    """
    subjects = conn.execute(query, (f"%{sem_num}%",)).fetchall()
    conn.close()
    
    return jsonify([row['name'] for row in subjects])

# ✅ UNITS
@app.route('/api/units/<subject>')
def get_units(subject):
    conn = get_db_connection()
    units = conn.execute("""
        SELECT DISTINCT u.name
        FROM units u
        JOIN subjects s ON u.subject_id = s.id
        WHERE TRIM(LOWER(s.name)) = TRIM(LOWER(?))
    """, (subject,)).fetchall()
    conn.close()
    return jsonify([row['name'] for row in units])

# ✅ QUESTIONS
@app.route('/api/questions/<subject>/<unit>')
def get_questions(subject, unit):
    conn = get_db_connection()
    data = conn.execute("""
        SELECT 
            q.question,
            q.answer,
            COUNT(q.question) as repeat_count
        FROM questions q
        JOIN units u ON q.unit_id = u.id
        JOIN subjects s ON u.subject_id = s.id
        WHERE TRIM(LOWER(s.name)) = TRIM(LOWER(?))
        AND TRIM(LOWER(u.name)) = TRIM(LOWER(?))
        GROUP BY q.question
        ORDER BY repeat_count DESC
    """, (subject, unit)).fetchall()

    conn.close()

    result = []
    for row in data:
        probability = min(row['repeat_count'] * 20, 100)
        result.append({
            "q": row['question'],
            "ans": row['answer'],
            "repeat": row['repeat_count'],
            "probability": f"{probability}%"
        })

    return jsonify(result)

# ✅ IMPORTANT QUESTIONS
@app.route('/api/important/<subject>/<unit>')
def get_important(subject, unit):
    conn = get_db_connection()

    data = conn.execute("""
        SELECT 
            q.question,
            q.answer,
            COUNT(q.question) as repeat_count
        FROM questions q
        JOIN units u ON q.unit_id = u.id
        JOIN subjects s ON u.subject_id = s.id
        WHERE TRIM(LOWER(s.name)) = TRIM(LOWER(?))
        AND TRIM(LOWER(u.name)) = TRIM(LOWER(?))
        GROUP BY q.question
        HAVING repeat_count >= 2
        ORDER BY repeat_count DESC
    """, (subject, unit)).fetchall()

    conn.close()

    result = []
    for row in data:
        probability = min(row['repeat_count'] * 20, 100)
        result.append({
            "q": row['question'],
            "ans": row['answer'],
            "repeat": row['repeat_count'],
            "probability": f"{probability}%"
        })

    return jsonify(result)

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True, port=5000) # Debug mode on rehne dein
