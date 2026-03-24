from flask import Flask, render_template, jsonify, request, redirect, session
import sqlite3
import os
import datetime   

app = Flask(__name__)

app.secret_key = "secret123"
ADMIN_EMAIL = "rashmivishwakarma613@gmail.com"  # 👉 apna email daalo

# --- DATABASE CONNECTION ---
def get_db_connection():
    conn = sqlite3.connect('rgpv_data.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- CREATE USERS TABLE (IMPORTANT) ---
def create_user_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT

        )
    ''')
    conn.commit()
    conn.close()

create_user_table()

# --- CREATE LOG TABLE (👉 YE YAHAN AAYEGA) ---
def create_log_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            time TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_log_table()

# --- ROUTES ---

@app.route('/')
def login():
    return render_template('login.html')

# ✅ SIGNUP PAGE
@app.route('/signup')
def signup():
    return render_template('signup.html')

# ✅ REGISTER (CREATE ACCOUNT)
@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

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

# ✅ LOGIN CHECK
@app.route('/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    ).fetchone()
    conn.close()
    import datetime  

    if user:
      session['user'] = user['email']

      conn = get_db_connection()
      conn.execute(
        "INSERT INTO logs (email, time) VALUES (?, ?)",
        (email, str(datetime.datetime.now()))
       )
      conn.commit()
      conn.close()

      return redirect('/dashboard')
    else:
      return "❌ Invalid Email or Password"

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/analysis')
def analysis():
    is_admin = session.get('user') == ADMIN_EMAIL
    return render_template('analysis.html', is_admin=is_admin)

@app.route('/logs')
def view_logs():
    if session.get('user') != ADMIN_EMAIL:
        return "❌ Access Denied"

    conn = get_db_connection()
    logs = conn.execute("SELECT * FROM logs ORDER BY id DESC").fetchall()
    conn.close()

    return render_template('logs.html', logs=logs)



# ✅ DELETE QUESTION
@app.route('/delete-question/<int:id>')
def delete_question(id):

    if session.get('user') != ADMIN_EMAIL:
        return "❌ Access Denied"

    conn = get_db_connection()
    conn.execute("DELETE FROM questions WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return "Deleted"

# ✅ UPDATE QUESTION
# ✅ ADD QUESTION PAGE
@app.route('/add-question')
def add_question_page():
    if session.get('user') != ADMIN_EMAIL:
        return "❌ Access Denied"
    return render_template('add_question.html')

# ✅ SAVE QUESTION
@app.route('/add-question', methods=['POST'])
def save_question():
    if session.get('user') != ADMIN_EMAIL:
      return "❌ Access Denied"
    subject = request.form['subject']
    unit = request.form['unit']
    question = request.form['question']
    repeats = request.form['repeats']
    probability = request.form['probability']
    answer = request.form['answer']

    conn = get_db_connection()
    conn.execute("""
        INSERT INTO questions (subject, unit, question, repeats, probability, answer)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (subject, unit, question, repeats, probability, answer))

    conn.commit()
    conn.close()

    return redirect('/dashboard')
# ✅ UPDATE QUESTION (ALAG FUNCTION)
@app.route('/update-question/<int:id>', methods=['POST'])
def update_question(id):

    if session.get('user') != ADMIN_EMAIL:
        return "❌ Access Denied"

    question = request.form['question']
    answer = request.form['answer']

    conn = get_db_connection()
    conn.execute(
        "UPDATE questions SET question=?, answer=? WHERE id=?",
        (question, answer, id)
    )
    conn.commit()
    conn.close()

    return "Updated"


# --- API ENDPOINTS ---

@app.route('/api/subjects/<semester>')
def get_subjects(semester):
    subjects = {
        "Semester 1": ["Engineering Physics", "Mathematics-I", "Basic Civil Engg."],
        "Semester 2": ["1", "Mathematics-II", "Basic Civil Engg.,4,5"],
        "Semester 3": ["3", "4", "3","4","5"],
        "Semester 4": ["3", "4", "3","4","5"],
        "Semester 5": ["3", "4", "3","4","5"],
        "Semester 6": ["Machine Learning", "Compiler Design", "Computer Networks"],
        "Semester 7": ["3", "4", "3","4","5"],
        "Semester 8": ["3", "4", "3","4","5"]
    }
    return jsonify(subjects.get(semester, []))

@app.route('/api/units/<subject>')
def get_units(subject):
    conn = get_db_connection()
    units = conn.execute(
        'SELECT DISTINCT unit FROM questions WHERE subject = ?', 
        (subject,)
    ).fetchall()
    conn.close()
    return jsonify([row['unit'] for row in units])

@app.route('/api/questions/<subject>/<unit>')
def get_unit_questions(subject, unit):
    conn = get_db_connection()
    questions = conn.execute(
        'SELECT * FROM questions WHERE subject = ? AND unit = ?', 
        (subject, unit)
    ).fetchall()
    conn.close()
    
    output = []
    for q in questions:
       output.append({
           'id': q['id'],   # ✅ ADD THIS
           'q': q['question'],
           'repeats': q['repeats'],
           'prob': q['probability'],
           'ans': q['answer']
})
    return jsonify(output)

# --- RUN ---
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
