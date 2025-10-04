from flask import Flask, jsonify, request
import sqlite3


app = Flask(__name__)

DB_NAME = "budget_manager.db"

def init_db():
    conn = sqlite3.connect(DB_NAME) #Opens a connection to the database file named 'budget_manager.db'
    cursor = conn.cursor() # Creates a cursor/Tool that lets us send commands(SELECT,INSERT)
    
    cursor.execute("""
     CREATE TABLE IF NOT EXISTS users (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         username TEXT UNIQUE NOT NULL,
         password TEXT NOT NULL
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

# ------ USER -------
@app.post("/api/register")
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO users (username,password) VALUES (?, ?)", (username, password))
    conn.commit() # Save changes to the database
    conn.close()
    
    return jsonify({"message": "user registered successfully"}), 201
    
# print("Getting data...", data)
# return "xxxx"

# http://127.0.0.1:5000/api/users/1
@app.get("/api/users/<int:user_id>")
def get_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    return jsonify({"id": row["id"], "username": row["username"]}), 200



if __name__ == "__main__":
    init_db()
    app.run(debug=True)