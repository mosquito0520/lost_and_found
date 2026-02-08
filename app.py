from flask import Flask, render_template, request, redirect, session
import sqlite3
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # 隨機 secret key

# ✅ 寫死帳號和密碼
users = {
    "admin": {"password": "1234", "role": "admin"},  # 管理員帳號
    "student1": {"password": "1111", "role": "user"}, # 一般使用者
    "student2": {"password": "2222", "role": "user"}  # 一般使用者
}

# 登入頁
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and password == users[username]["password"]:
            session["role"] = users[username]["role"]  # 記錄身份
            return redirect("/")
        else:
            return "帳號或密碼錯誤！"

    return render_template("login.html")

# 首頁
@app.route("/")
def home():
    if "role" not in session:
        return redirect("/login")

    conn = sqlite3.connect('lost_and_found.db')
    c = conn.cursor()
    c.execute("SELECT * FROM items")
    items = c.fetchall()
    conn.close()

    if session["role"] == "admin":
        return render_template("index_admin.html", items=items)
    else:
        return render_template("index_user.html", items=items)

# 新增失物（管理員）
@app.route("/add", methods=["POST"])
def add():
    if session.get("role") != "admin":
        return "你沒有權限", 403

    name = request.form["name"]
    place = request.form["place"]

    conn = sqlite3.connect('lost_and_found.db')
    c = conn.cursor()
    c.execute("INSERT INTO items (name, place, status) VALUES (?, ?, ?)",
              (name, place, "未領取"))
    conn.commit()
    conn.close()

    return redirect("/")

# 標記已領取（管理員）
@app.route("/claim/<int:item_id>", methods=["POST"])
def claim(item_id):
    if session.get("role") != "admin":
        return "你沒有權限", 403

    conn = sqlite3.connect('lost_and_found.db')
    c = conn.cursor()
    c.execute("UPDATE items SET status = '已領取' WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

    return redirect("/")

# 登出
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
