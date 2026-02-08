import sqlite3

conn = sqlite3.connect('lost_and_found.db')
c = conn.cursor()

# 建立資料表
c.execute('''
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    place TEXT NOT NULL,
    status TEXT NOT NULL
)
''')

conn.commit()
conn.close()
print("資料庫建立完成！")
