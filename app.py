from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3, os

app = Flask(__name__)
app.secret_key = "dev-secret-key"

DB_PATH = os.path.join(os.path.dirname(__file__), "vocab.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET","POST"])
def index():
    conn = get_db_connection()
    topics = [r['topic'] for r in conn.execute("SELECT DISTINCT topic FROM vocabulary").fetchall()]
    query = ""
    results = []
    if request.method == "POST":
        query = request.form.get("search","").strip()
        selected_topics = request.form.getlist("topics")
        if query:
            sql = "SELECT * FROM vocabulary WHERE word LIKE ? OR meaning LIKE ? ORDER BY topic, word"
            params = (f'%{query}%', f'%{query}%')
            results = conn.execute(sql, params).fetchall()
        elif selected_topics:
            placeholders = ",".join("?" for _ in selected_topics)
            sql = f"SELECT * FROM vocabulary WHERE topic IN ({placeholders}) ORDER BY topic, word"
            results = conn.execute(sql, selected_topics).fetchall()
    conn.close()
    return render_template("index.html", topics=topics, results=results, query=query)

@app.route("/vocabulary")
def vocabulary():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM vocabulary ORDER BY topic, word").fetchall()
    conn.close()
    return render_template("vocabulary.html", data=rows)

@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        word = request.form.get("word","").strip()
        meaning = request.form.get("meaning","").strip()
        topic = request.form.get("topic","").strip()
        if not word or not topic:
            flash("Word and topic are required.", "danger")
            return redirect(url_for("add"))
        conn = get_db_connection()
        conn.execute("INSERT INTO vocabulary (word, meaning, topic) VALUES (?, ?, ?)", (word, meaning, topic))
        conn.commit()
        conn.close()
        flash("Added vocabulary.", "success")
        return redirect(url_for("vocabulary"))
    return render_template("add.html")

@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):
    conn = get_db_connection()
    item = conn.execute("SELECT * FROM vocabulary WHERE id = ?", (id,)).fetchone()
    if not item:
        conn.close()
        flash("Not found.", "warning")
        return redirect(url_for("vocabulary"))
    if request.method == "POST":
        word = request.form.get("word","").strip()
        meaning = request.form.get("meaning","").strip()
        topic = request.form.get("topic","").strip()
        if not word or not topic:
            flash("Word and topic are required.", "danger")
            return redirect(url_for("edit", id=id))
        conn.execute("UPDATE vocabulary SET word=?, meaning=?, topic=? WHERE id=?", (word, meaning, topic, id))
        conn.commit()
        conn.close()
        flash("Updated.", "success")
        return redirect(url_for("vocabulary"))
    conn.close()
    return render_template("edit.html", item=item)

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM vocabulary WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("Deleted.", "success")
    return redirect(url_for("vocabulary"))

@app.route("/grammar")
def grammar():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM grammar ORDER BY id").fetchall()
    conn.close()
    return render_template("grammar.html", data=rows)

@app.route("/patterns")
def patterns():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM sentence_patterns ORDER BY id").fetchall()
    conn.close()
    return render_template("patterns.html", data=rows)

if __name__ == "__main__":
    # If port 5000 fails on your PC, change port argument (e.g., port=5001)
    app.run(debug=True, host="127.0.0.1", port=5000)
