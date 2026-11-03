import sqlite3

def init_db():
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    # User aur Chatbot ki conversation save karne ke liye table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            bot_response TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_chat(user_msg, bot_msg):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO logs (user_message, bot_response) VALUES (?, ?)', (user_msg, bot_msg))
    conn.commit()
    conn.close()