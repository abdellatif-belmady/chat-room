from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, join_room, leave_room, send
from flask_cors import CORS
import random
from string import ascii_uppercase
from flask_socketio import emit
import sqlite3
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["SECRET_KEY"] = "dtdrterttrtgfjkfghbkj"
socketio = SocketIO(app, cors_allowed_origins="*")

rooms = {}


# Only create the database if it doesn't exist
if not os.path.exists('chat.db'):
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()

    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL UNIQUE
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_code TEXT,
            name TEXT,
            message TEXT,
            FOREIGN KEY (room_code) REFERENCES rooms (code)
        )
    ''')

    conn.commit()
    conn.close()
    print("Database created successfully!")
else:
    print("Database already exists!")

def get_db():
    conn = sqlite3.connect('chat.db')
    conn.row_factory = sqlite3.Row
    return conn

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT code FROM rooms WHERE code = ?", (code,))
        if c.fetchone() is None:
            c.execute("INSERT INTO rooms (code) VALUES (?)", (code,))
            conn.commit()
            conn.close()
            break
    
    return code

@app.route("/", methods=["POST", "GET"])
def home():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name)

        if join != False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name)

        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": set(), "messages": []}
        elif code not in rooms:
            # Check if room exists in database
            conn = get_db()
            c = conn.cursor()
            c.execute("SELECT code FROM rooms WHERE code = ?", (code,))
            if c.fetchone() is None:
                conn.close()
                return render_template("home.html", error="Room does not exist.", code=code, name=name)
            conn.close()
            rooms[room] = {"members": set(), "messages": []}

        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html")

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None:
        return redirect(url_for("home"))

    return render_template("room.html", code=room)

@app.route("/get_chat_history/<room_code>")
def get_chat_history(room_code):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("""
            SELECT name, message 
            FROM messages 
            WHERE room_code = ? 
            ORDER BY id ASC
        """, (room_code,))
        messages = [{"name": row["name"], "message": row["message"]} for row in c.fetchall()]
        conn.close()
        return jsonify(messages)
    except Exception as e:
        print(f"Error fetching chat history: {e}")
        return jsonify({"error": "Failed to fetch chat history"}), 500

def get_users_in_room(room_code):
    if room_code in rooms:
        return list(rooms[room_code]["members"])
    return []

@app.route('/get_room_users/<room_code>')
def get_room_users(room_code):
    users = get_users_in_room(room_code)
    return jsonify(users)

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }

    # Store message in database
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("""
            INSERT INTO messages (room_code, name, message) 
            VALUES (?, ?, ?)
        """, (room, content["name"], content["message"]))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error storing message: {e}")

    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        rooms[room] = {"members": set(), "messages": []}

    join_room(room)
    rooms[room]["members"].add(name)
    emit("message", {
        "name": name,
        "message": f"{name} has entered the room",
        "system": True
    }, to=room, skip_sid=request.sid)
    print(f"{name} joined room {room}")

@app.route("/leave")
def leave():
    room = session.get("room")
    name = session.get("name")
    if room in rooms:
        rooms[room]["members"].discard(name)
        if len(rooms[room]["members"]) == 0:
            del rooms[room]
    session.clear()
    emit("message", {
        "name": name,
        "message": f"{name} has left the room",
        "system": True
    }, to=room, namespace="/")
    return redirect(url_for("home"))

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"].discard(name)
        if len(rooms[room]["members"]) == 0:
            del rooms[room]

    emit("message", {
        "name": name,
        "message": f"{name} has left the room",
        "system": True
    }, to=room)
    print(f"{name} has left the room {room}")

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)