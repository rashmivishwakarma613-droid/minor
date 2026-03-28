import sqlite3
import pandas as pd
import os

def create_db_from_excel():
    # Purani file delete karein taaki fresh start ho
    if os.path.exists('rgpv_data.db'):
        os.remove('rgpv_data.db')
        print("🗑️ Old database deleted.")

    conn = sqlite3.connect('rgpv_data.db')
    cursor = conn.cursor()

    # Tables Create Karein
    cursor.execute("CREATE TABLE semesters (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
    cursor.execute("CREATE TABLE subjects (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, semester_id INTEGER)")
    cursor.execute("CREATE TABLE units (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, subject_id INTEGER)")
    cursor.execute("CREATE TABLE questions (id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT, answer TEXT, unit_id INTEGER, year INTEGER)")

    # Excel Load Karein
    df = pd.read_excel("data.xlsx")
    df.columns = [c.strip().lower() for c in df.columns]
    df = df.ffill() # Empty cells ko bharta hai

    sem_map = {}
    sub_map = {}
    unit_map = {}

    for _, row in df.iterrows():
        # Clean Data
        sem_name = str(row['semester']).strip()
        sub_name = str(row['subject']).strip()
        unit_name = str(row['unit']).strip()
        ques = str(row['question']).strip()
        ans = str(row['answer']).strip()
        year = int(row['year']) if not pd.isna(row['year']) else 0

        # 1. Insert Semester
        if sem_name not in sem_map:
            cursor.execute("INSERT INTO semesters (name) VALUES (?)", (sem_name,))
            sem_map[sem_name] = cursor.lastrowid
        
        sem_id = sem_map[sem_name]

        # 2. Insert Subject (Sem_id ke saath check karein taaki subjects mix na hon)
        sub_key = (sem_id, sub_name.lower())
        if sub_key not in sub_map:
            cursor.execute("INSERT INTO subjects (name, semester_id) VALUES (?, ?)", (sub_name, sem_id))
            sub_map[sub_key] = cursor.lastrowid
        
        sub_id = sub_map[sub_key]

        # 3. Insert Unit
        unit_key = (sub_id, unit_name.lower())
        if unit_key not in unit_map:
            cursor.execute("INSERT INTO units (name, subject_id) VALUES (?, ?)", (unit_name, sub_id))
            unit_map[unit_key] = cursor.lastrowid
        
        unit_id = unit_map[unit_key]

        # 4. Insert Question
        cursor.execute("INSERT INTO questions (question, answer, unit_id, year) VALUES (?, ?, ?, ?)", 
                       (ques, ans, unit_id, year))

    conn.commit()
    conn.close()
    print("✅ Database Freshly Updated! All 3 subjects in Sem 6 should be there.")

if __name__ == "__main__":
    create_db_from_excel()
