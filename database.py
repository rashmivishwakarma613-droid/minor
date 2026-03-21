import sqlite3

def create_db():
    # 1. Database file se connect karein (Ye 'rgpv_data.db' naam ki file bana dega)
    conn = sqlite3.connect('rgpv_data.db')
    cursor = conn.cursor()

    # 2. Agar purani table hai toh use hata dein (Fresh start ke liye)
    cursor.execute('DROP TABLE IF EXISTS questions')

    # 3. Table Structure banayein
    cursor.execute('''
        CREATE TABLE questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            unit TEXT,
            question TEXT,
            repeats TEXT,
            probability TEXT,
            answer TEXT
        )
    ''')

    # 4. Aapka Data (Yahan aap apne 30-30 sawal niche isi format mein add kar sakti hain)
    # Format: ('Subject Name', 'Unit Number', 'Question Text', 'Years', 'Prob %', 'Detailed Answer')
    questions_list = [
        # --- MACHINE LEARNING - UNIT 1 ---
        ('Machine Learning', 'Unit 1', 'What is Supervised Learning?', '2021, 2023, 2024', '95%', 'Supervised learning is a type of ML where the model is trained on labeled data...'),
        ('Machine Learning', 'Unit 1', 'Explain Reinforcement Learning', '2020, 2022', '80%', 'It is an area of machine learning concerned with how intelligent agents ought to take actions...'),
        ('Machine Learning', 'Unit 1', 'Difference between Classification and Regression', '2019, 2023', '85%', 'Classification predicts discrete labels, while Regression predicts continuous quantities...'),
        
        # --- MACHINE LEARNING - UNIT 2 ---
        ('Machine Learning', 'Unit 2', 'What is a Decision Tree?', '2021, 2022', '75%', 'A decision tree is a non-parametric supervised learning method used for classification...'),
        ('Machine Learning', 'Unit 2', 'Explain Overfitting and Underfitting', '2018, 2020, 2024', '90%', 'Overfitting happens when a model learns noise; Underfitting is when it cannot capture the trend...'),

        # --- AAP YAHAN AUR BHI SUBJECTS/UNITS ADD KAR SAKTI HAIN ---
        # ('Compiler Design', 'Unit 1', 'Question here...', '2023', '70%', 'Answer here...')
    ]

    # 5. Data ko Database mein Insert karein
    cursor.executemany('''
        INSERT INTO questions (subject, unit, question, repeats, probability, answer) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', questions_list)
    
    # 6. Save karke close karein
    conn.commit()
    conn.close()
    print("--------------------------------------------------")
    print("SUCCESS: 'rgpv_data.db' ban gayi hai aur data load ho gaya hai!")
    print("--------------------------------------------------")

if __name__ == "__main__":
    create_db()
    input("\nKaam ho gaya! Enter dabayein band karne ke liye...") # Ye line add karein