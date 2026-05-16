from flask import Flask, render_template, jsonify, request, redirect, session, send_from_directory
import os
import mysql.connector
from datetime import datetime, timedelta
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY", "secret123")
app.permanent_session_lifetime = timedelta(minutes=30)
ADMIN_EMAIL = "rashmivishwakarma613@gmail.com"

# ---------------- DATABASE ---------------- #

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ROOT",
        database="ai_exam_db"
    )

    return conn

SYLLABUS_DATA = {
    "Machine Learning": {
         "Unit 1": ["introduction", "scope", "limitations", "regression", "probability", "statistics", "linear algebra", "convex optimization", "data normalization", "design issues", "training data", "testing data"],
         "Unit 2": ["linearity", "sigmoid", "relu", "gradient descent", "back propagation", "auto encoders", "regularization", "multilayer network", "backpropagation"],
         "Unit 3": ["cnn", "convolutional", "padding", "pooling", "transfer learning", "pca", "dimension reduction", "tensor flow"],
         "Unit 4": ["rnn", "recurrent", "lstm", "gru", "bleu score", "reinforcement", "mdp", "q-learning", "actor-critic", "attention model", "markov decision"],
         "Unit 5": ["svm", "support vector", "bayesian", "nlp", "speech processing", "tokenization", "visualization", "data preprocessing", "batch normalization", "locally weighted", "model selection"]
    },

    "Computer Network": {
        "Unit 1": ["osi", "reference model", "topology", "connection oriented", "connectionless", "service primitives", "bandwidth", "data rate", "network architecture"],
        "Unit 2": ["data link", "go-back-n", "sliding window", "parity", "hamming", "stop and wait", "selective repeat", "bit stuffing", "byte stuffing", "arp", "fsm"],
        "Unit 3": ["csma", "aloha", "slotted", "collision", "mac layer", "transmission media", "guided", "unguided", "adaptive tree walk", "802 series", "limited-contention"],
        "Unit 4": ["network layer", "routing", "icmp", "ip address", "subnet", "ipv4", "ipv6", "bellman ford", "distance vector", "fragmentation", "least cost"],
        "Unit 5": ["tcp", "udp", "header", "throughput", "flow control", "congestion", "dns", "e-mail", "qos", "frame relay", "establishment", "rfc", "fddi", "broadband", "local loop"]
    },
     "Compiler Design": {
        "Unit 1": ["lexical", "tokens", "front-end", "back-end", "lex", "buffering", "compiler phases"],
        "Unit 2": ["syntax", "parsing", "cfg", "recursive descent", "lr parser", "syntax trees", "ll(1)"],
        "Unit 3": ["type checking", "storage", "symbol table", "error detection"],
        "Unit 4": ["intermediate code", "dag", "peephole", "code generation"],
        "Unit 5": ["optimization", "dead code", "loop optimization"]
    },

     "Project Management": {
        "Unit 1": ["conventional", "software economics", "team effectiveness"],
        "Unit 2": ["life cycle", "inception", "elaboration", "artifacts", "workflows"],
        "Unit 3": ["iterative", "organisations", "metrics", "indicators"]
    }
}

def init_db():

    conn = get_db_connection()
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        password TEXT
    )
    """)

    # SUBJECTS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        id INT AUTO_INCREMENT PRIMARY KEY,
        semester VARCHAR(20),
        name VARCHAR(100)
    )
    """)

    # UNITS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS units (
        id INT AUTO_INCREMENT PRIMARY KEY,
        subject_id INT,
        name VARCHAR(100)
    )
    """)

    # QUESTIONS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT,
    semester VARCHAR(20),
    subject VARCHAR(100),
    unit VARCHAR(100),
    question TEXT,
    repeat_count INT DEFAULT 1
                   )
""")
    
     # LOGS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255),
    action VARCHAR(50),
    login_time DATETIME,
    logout_time DATETIME,
    status VARCHAR(50)
)
""")
    conn.commit()
    cursor.close()
    conn.close()


 


def seed_data():

    conn = get_db_connection()

    cursor = conn.cursor()

    subjects = [
        ("Semester 6", "Machine Learning"),
        ("Semester 6", "Computer Network"),
        ("Semester 6", "Compiler Design"),
        ("Semester 6", "Project Management")
    ]

    for sem, sub in subjects:

        cursor.execute(
            "SELECT * FROM subjects WHERE name=%s",
            (sub,)
        )

        subject = cursor.fetchone()

        if not subject:

            cursor.execute(
                "INSERT INTO subjects (semester, name) VALUES (%s, %s)",
                (sem, sub)
            )

    conn.commit()

    cursor.close()
    conn.close()
# ---------------- SMART UNIT FINDER ---------------- #
# LOGS TABLE
def auto_assign_unit(subject, question_text):
    if subject in SYLLABUS_DATA:
        text = question_text.lower()

        for unit, keywords in SYLLABUS_DATA[subject].items():
            if any(word in text for word in keywords):
                return unit

    return "General"

# ---------------- INITIALIZE DB ---------------- #

init_db()
seed_data()

# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    return render_template("index.html")




# -------------------teacher------------------#

@app.route('/teacher/add-question', methods=['POST'])
def teacher_add_question():
    data = request.json

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pending_questions 
        (teacher_name, year, semester, subject, unit, question)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        data['teacher_name'],
        data['year'],
        data['semester'],
        data['subject'],
        data['unit'],
        data['question']
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Question sent for approval"})
# ---------------- AUTH ---------------- #

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user['password'], password):

            session['user'] = user['email']
            session.permanent = True

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO logs (email, action, login_time, status)
                VALUES (%s, %s, %s, %s)
            """, (
                user['email'],
                'LOGIN',
                datetime.now(),
                'ACTIVE'
            ))

            conn.commit()

            cursor.close()
            conn.close()

            return redirect('/dashboard')

        return "Invalid credentials ❌"

    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/register', methods=['POST'])
def register():

    name = request.form['name']
    email = request.form['email']

    password = generate_password_hash(
        request.form['password']
    )

    conn = get_db_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
           "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
            )

        conn.commit()

        cursor.close()

    except:
        return "User already exists ❌"

    finally:
        conn.close()

    return redirect('/login')

@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect('/login')

    return render_template('dashboard.html')


# ---------------- PYQ ROUTES ---------------- #

@app.route('/pyq/<subject>')
def pyq(subject):

    folder_name = subject.replace(" ", "_")

    folder_path = os.path.join(
    'static',
    'papers',
    folder_name
)
    pdf_files = []

    if os.path.exists(folder_path):

        for file in os.listdir(folder_path):

            if file.endswith('.pdf'):
                pdf_files.append(file)

    return render_template(
        'pyq_list.html',
        subject=subject,
        pdf_files=pdf_files
    )
# ---------------- TEACHER PAGE ---------------- #

@app.route("/teacher/add-question")
def teacher_page():
    return render_template("teacher.html")
# ---------------question--------------------#
@app.route('/questions')
def questions():

    conn = get_db_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT year, semester, subject, unit, question
        FROM questions
    """)

    data = cursor.fetchall()
    print(data)
    cursor.close()
    conn.close()

    return render_template("questions.html", questions=data)
# ---------------- APIs ----------------   #

@app.route('/api/subjects/<semester>')
def get_subjects(semester):

    conn = get_db_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
    "SELECT DISTINCT name FROM subjects WHERE semester=%s",
    (semester,)
)

    subjects = cursor.fetchall()

    cursor.close()

    conn.close()

    return jsonify([row["name"] for row in subjects])

@app.route('/api/units/<subject>')
def get_units(subject):

    conn = get_db_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT DISTINCT u.name
    FROM units u
    JOIN subjects s ON u.subject_id = s.id
    WHERE s.name=%s
""", (subject,))

    units = cursor.fetchall()

    cursor.close()

    conn.close()

    unit_names = [row["name"] for row in units]

    if not unit_names and subject in SYLLABUS_DATA:
        return jsonify(list(SYLLABUS_DATA[subject].keys()))

    return jsonify(unit_names)




@app.route('/api/questions/<subject>/<unit>')
def get_questions(subject, unit):

    conn = get_db_connection()

    cursor = conn.cursor(dictionary=True)

    # "Unit 2" -> 2
    unit_number = unit.replace("Unit ", "")

    print("Subject:", subject)
    print("Unit:", unit_number)

    cursor.execute("""
        SELECT question, repeat_count
        FROM questions
        WHERE subject=%s AND unit=%s
    """, (subject, int(unit_number)))

    data = cursor.fetchall()

    print(data)

    cursor.close()
    conn.close()

    return jsonify([
        {
            "q": row["question"],
            "repeat": row["repeat_count"],
            "probability": f"{min(row['repeat_count'] * 20, 100)}%"
        }
        for row in data
    ])

@app.route('/api/ask-ai', methods=['POST'])
def ask_ai():

    data = request.json

    return jsonify({
        "answer": f"AI Response for: {data.get('question')}"
    })

# ---------------- ADMIN ---------------- #

@app.route('/admin')
def admin_panel():

    if session.get('user') != ADMIN_EMAIL:
        return "Access Denied"

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")

    total_users = cursor.fetchone()[0]

    cursor.close()

    conn.close()

    return render_template(
        "admin.html",
        total_users=total_users
    )

# ---------------- LOGOUT ---------------- #

@app.route('/logout')
def logout():

    email = session.get('user')

    if email:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE logs
            SET logout_time=%s,
                action=%s,
                status=%s
            WHERE email=%s
            AND status='ACTIVE'
            ORDER BY id DESC
            LIMIT 1
        """, (
            datetime.now(),
            'LOGOUT',
            'LOGOUT',
            email
        ))

        conn.commit()

        cursor.close()
        conn.close()

    session.clear()

    return redirect('/')


# ------------------logs route-----------

@app.route('/logs')
def logs():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM logs
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('logs.html', logs=data)

# ---------------------teacher-----------------#
@app.route('/admin/pending-questions')
def pending_questions():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM pending_questions WHERE status='pending'")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("pending_questions.html", questions=data)

# -----------------Approve API:----------------#


@app.route('/admin/approve-question/<int:id>')
def approve_question(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM pending_questions WHERE id=%s", (id,))
    q = cursor.fetchone()

    if q:
        cursor.execute("""
            INSERT INTO questions (year, semester, subject, unit, question)
            VALUES (%s,%s,%s,%s,%s)
        """, (q['year'], q['semester'], q['subject'], q['unit'], q['question']))

        cursor.execute("UPDATE pending_questions SET status='approved' WHERE id=%s", (id,))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/admin/pending-questions')

@app.route('/leave', methods=['POST'])
def leave():

    email = session.get('user')

    if email:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE logs
            SET logout_time=%s,
                action=%s,
                status=%s
            WHERE email=%s
            AND status='ACTIVE'
            ORDER BY id DESC
            LIMIT 1
        """, (
            datetime.now(),
            'LEFT PAGE',
            'LEFT',
            email
        ))

        conn.commit()

        cursor.close()
        conn.close()

    return '', 204


# ---------------- RUN ---------------- #

if __name__ == '__main__':
    app.run(debug=True)
