import sqlite3, os
DB = os.path.join(os.path.dirname(__file__), "vocab.db")
conn = sqlite3.connect(DB)
c = conn.cursor()

# Create tables
c.execute("""
CREATE TABLE IF NOT EXISTS vocabulary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT NOT NULL,
    meaning TEXT NOT NULL,
    topic TEXT NOT NULL
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS grammar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    example TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS sentence_patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pattern TEXT NOT NULL,
    usage TEXT NOT NULL,
    example TEXT
)
""")

conn.commit()
conn.close()
print("✅ init_db: tables created (if they did not exist). DB file:", DB)
