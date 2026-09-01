#!/usr/bin/env python3
"""
MIU V153 — CEREBRO LOCAL
Memoria persistente en SQLite. No se borra al cerrar Termux.
"""
import sqlite3, json, time, os
from pathlib import Path

DB_PATH = Path("/data/data/com.termux/files/home/miu-ecosistema/miu_brain.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT, source TEXT, content TEXT,
        tags TEXT, phi REAL, importance REAL DEFAULT 1.0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT, user TEXT, message TEXT,
        response TEXT, model TEXT, phi_delta REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS system_state (
        key TEXT PRIMARY KEY, value TEXT, updated TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS commands (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT, command TEXT, output TEXT,
        status TEXT, source TEXT)''')
    conn.commit()
    conn.close()

def remember(content, source="user", tags="", phi=2874.62, importance=1.0):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO memories VALUES (NULL,?,?,?,?,?,?)",
        (time.strftime("%Y-%m-%dT%H:%M:%SZ"), source, content, tags, phi, importance))
    conn.commit()
    conn.close()

def recall(query="", limit=10, tags=""):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if tags:
        c.execute("SELECT * FROM memories WHERE tags LIKE ? ORDER BY importance DESC, timestamp DESC LIMIT ?",
            (f"%{tags}%", limit))
    elif query:
        c.execute("SELECT * FROM memories WHERE content LIKE ? ORDER BY timestamp DESC LIMIT ?",
            (f"%{query}%", limit))
    else:
        c.execute("SELECT * FROM memories ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def log_conversation(user, message, response, model="local", phi_delta=0):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO conversations VALUES (NULL,?,?,?,?,?,?)",
        (time.strftime("%Y-%m-%dT%H:%M:%SZ"), user, message, response, model, phi_delta))
    conn.commit()
    conn.close()

def set_state(key, value):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO system_state VALUES (?,?,?)",
        (key, json.dumps(value), time.strftime("%Y-%m-%dT%H:%M:%SZ")))
    conn.commit()
    conn.close()

def get_state(key, default=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT value FROM system_state WHERE key=?", (key,))
    row = c.fetchone()
    conn.close()
    return json.loads(row[0]) if row else default

def log_command(cmd, output, status="ok", source="local"):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO commands VALUES (NULL,?,?,?,?,?)",
        (time.strftime("%Y-%m-%dT%H:%M:%SZ"), cmd, output, status, source))
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM memories")
    memories = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM conversations")
    conversations = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM commands")
    commands = c.fetchone()[0]
    conn.close()
    return {"memories": memories, "conversations": conversations, "commands": commands}

# Inicializar al importar
init_db()
