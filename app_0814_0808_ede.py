# 代码生成时间: 2025-08-14 08:08:41
// 导入bottle框架和sqlite3数据库模块
from bottle import Bottle, run, request, response, HTTPError
import sqlite3

# 初始化bottle应用
app = Bottle()

# 数据库连接配置
DB_FILE = 'your_database.db'

# 数据库初始化函数
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )""")
    conn.commit()
    conn.close()

# 数据库查询函数
def get_user(id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
    user = cursor.fetchone()
    conn.close()
    return user

# 数据库插入函数
def create_user(username, email, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        conn.rollback()
        return False
    finally:
        conn.close()

# 数据库更新函数
def update_user(id, username, email, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET username = ?, email = ?, password = ? WHERE id = ?", (username, email, password, id))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        conn.rollback()
        return False
    finally:
        conn.close()

# 数据库删除函数
def delete_user(id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE id = ?", (id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        conn.rollback()
        return False
    finally:
        conn.close()

# Bottle路由和视图函数
@app.route('/users', method='GET')
def get_users():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return {"users": users}

@app.route('/users/<id:int>', method='GET')
def get_user_by_id(id):
    user = get_user(id)
    if user:
        return {"user": user}
    else:
        raise HTTPError(404, "User not found")

@app.route('/users', method='POST')
def create_user_handler():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    if create_user(username, email, password):
        response.status = 201
        return {"message": "User created successfully"}
    else:
        raise HTTPError(400, "Username already exists")

@app.route('/users/<id:int>', method='PUT')
def update_user_handler(id):
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    if update_user(id, username, email, password):
        return {"message": "User updated successfully"}
    else:
        raise HTTPError(404, "User not found")

@app.route('/users/<id:int>', method='DELETE')
def delete_user_handler(id):
    if delete_user(id):
        return {"message": "User deleted successfully"}
    else:
        raise HTTPError(404, "User not found")

# 初始化数据库
init_db()

# 运行应用
run(app, host='localhost', port=8080)