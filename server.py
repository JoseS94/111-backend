from flask import Flask, jsonify, request
import sqlite3
from datetime import date

app = Flask(__name__)

DB_NAME = "budget_manager.db"

def init_db():
    conn = sqlite3.connect(DB_NAME) #Opens a connection to the database file named 'budget_manager.db'
    cursor = conn.cursor() # Creates a cursor/Tool that lets us send commands(SELECT,INSERT)
    
    #USERS TABLE
    cursor.execute("""
     CREATE TABLE IF NOT EXISTS users (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         username TEXT UNIQUE NOT NULL,
         password TEXT NOT NULL
     )
    """)
    
    #-------EXPENSES TABLE -------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT NOT NULL,
        amount INT NOT NULL,
        date TEXT OT NULL,
        category TEXT NOT NULL,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )             
    """)

    conn.commit() # Saves changes
    conn.close()

# @app.route("/api/health", methods=["GET"])
# def health_check():
# return jsonify




@app.get("/api/health")
def health_check():
    return jsonify({"status": "OK"}), 200

# ------ USERS -------
@app.post("/api/register")
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    #----Inserts new users to DB -------
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit() # Save changes to the database
    conn.close()
    
    return jsonify({"message": "user registered successfully"}), 201
    
# print("Getting data...", data)
# return "xxxx"

# http://127.0.0.1:5000/api/users/1
@app.get("/api/users/<int:user_id>")
def get_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    return jsonify({"id": row["id"], "username": row["username"]}), 200


# http://127.0.0.1:5000/api/users/2
@app.put("/api/users/<int:user_id>")
def update_user(user_id):
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * from users where id=?", (user_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"message": "User not found"}), 404
    
    cursor.execute("UPDATE users SET username=?, password=? WHERE id=?", (username, password, user_id))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "User updated successfully"}), 200


@app.delete("/api/users/<int:user_id>")
def delete_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    #xxxx
    cursor.execute("SELECT * from users where id=?", (user_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"message": "User not found"}), 404
    
    
    
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "User deleted successfully"}), 200


@app.get("/api/users")
def get_users():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Allows column values to be retrived by name, row["username"]
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall() # Retrives all rows from the reslut of the query,  returns a list of tuples
    conn.close()
    
    users = []
    for row in rows:
        user = {"id": row["id"], "username": row["username"], "password": row["password"]}
        users.append(user)
        
    return  jsonify(users), 200
    


@app.post("/api/expenses")
def create_expense():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    amount = data.get("amount")
    category = data.get("category")
    user_id = data.get("user_id")
    date_str = date.today()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO expenses (title, description, amount, date, category, user_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, description, amount, date_str, category, user_id)
    )
    
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Expense created successfully"}), 200





if __name__ == "__main__":
    init_db()
    app.run(debug=True)