import sqlite3
import datetime

DB_NAME = 'bot_clara.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    # Tabela para histórico básico (apenas para registro)
    conn.execute('CREATE TABLE IF NOT EXISTS history (user_id INTEGER, role TEXT, content TEXT, timestamp TIMESTAMP)')
    # Tabela para controle de leads
    conn.execute('CREATE TABLE IF NOT EXISTS leads (user_id INTEGER PRIMARY KEY, last_msg_time TIMESTAMP, status TEXT)')
    conn.commit()
    conn.close()

def save_interaction(user_id, role, content):
    conn = sqlite3.connect(DB_NAME)
    now = datetime.datetime.now()
    conn.execute('INSERT INTO history (user_id, role, content, timestamp) VALUES (?, ?, ?, ?)', (user_id, role, content, now))
    conn.commit()
    conn.close()

def update_lead_status(user_id, status):
    conn = sqlite3.connect(DB_NAME)
    now = datetime.datetime.now().timestamp()
    conn.execute('INSERT OR REPLACE INTO leads (user_id, last_msg_time, status) VALUES (?, ?, ?)', (user_id, now, status))
    conn.commit()
    conn.close()

def get_lead_status(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT status FROM leads WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def get_chat_history(user_id, limit=10):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT role, content FROM history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?", (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    # Retorna em ordem cronológica (mais antigo para mais novo)
    return [{"role": role, "content": content} for role, content in reversed(rows)]
