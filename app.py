from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    conn = sqlite3.connect('lost_and_found.db')
    c = conn.cursor()
    c.execute("SELECT * FROM items")
    items = c.fetchall()  # 拿出所有資料
    conn.close()
    return render_template("index.html", items=items)  # ⚠️ 一定要傳 items

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    place = request.form["place"]
    conn = sqlite3.connect('lost_and_found.db')
    c = conn.cursor()
    c.execute("INSERT INTO items (name, place, status) VALUES (?, ?, ?)", (name, place, "未領取"))
    conn.commit()
    conn.close()
    return redirect("/")
    
if __name__ == "__main__":
    app.run(debug=True)

