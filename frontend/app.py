from flask import Flask, request, jsonify, send_from_directory
import os, json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- File paths ---
USERS_FILE = 'users.json'
WHISPERS_FILE = 'whispers.json'
CHAT_DIR = 'chats'

# --- Ensure required files/folders exist ---
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump({}, f)

if not os.path.exists(WHISPERS_FILE):
    with open(WHISPERS_FILE, 'w') as f:
        json.dump([], f)

if not os.path.exists(CHAT_DIR):
    os.makedirs(CHAT_DIR)

# --- Utils ---
def load_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(data):
    with open(USERS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_whispers():
    with open(WHISPERS_FILE, 'r') as f:
        return json.load(f)

def save_whispers(data):
    with open(WHISPERS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_chat_path(room_id):
    return os.path.join(CHAT_DIR, f"{room_id}.json")

# --- Authentication Routes ---
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    nickname = data.get("nickname")
    password = data.get("password")
    if not nickname or not password:
        return jsonify({"success": False, "message": "Missing fields"})
    users = load_users()
    if nickname in users:
        return jsonify({"success": False, "message": "Nickname already exists"})
    users[nickname] = password
    save_users(users)
    return jsonify({"success": True})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    nickname = data.get("nickname")
    password = data.get("password")
    users = load_users()
    if users.get(nickname) == password:
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Invalid credentials"})

# --- Whisper Routes ---
@app.route("/submitFeeling", methods=["POST"])
def submit_feeling():
    data = request.get_json()
    message = data.get("message", "").strip()
    mood = data.get("mood", "")
    nickname = data.get("nickname", "")
    target = data.get("target", "wall")
    if not message:
        return jsonify({"success": False, "message": "Empty message"})
    whisper = {
        "message": message,
        "mood": mood,
        "nickname": nickname,
        "target": target
    }
    whispers = load_whispers()
    whispers.append(whisper)
    save_whispers(whispers)
    return jsonify({"success": True})

@app.route("/getWhispers", methods=["GET"])
def get_whispers():
    whispers = load_whispers()
    return jsonify(whispers[-100:])  # latest 100 messages

# --- Real-time Chat Routes ---
@app.route("/chat/<room_id>", methods=["GET"])
def get_chat(room_id):
    path = get_chat_path(room_id)
    if not os.path.exists(path):
        return jsonify({"messages": []})
    with open(path, "r") as f:
        messages = json.load(f)
    return jsonify({"messages": messages})

@app.route("/chat/<room_id>", methods=["POST"])
def post_chat(room_id):
    data = request.get_json()
    msg = {
        "from": data.get("from", "unknown"),
        "text": data.get("text", "").strip()
    }
    if not msg["text"]:
        return jsonify({"success": False, "message": "Empty message"}), 400
    path = get_chat_path(room_id)
    if os.path.exists(path):
        with open(path, "r") as f:
            messages = json.load(f)
    else:
        messages = []
    messages.append(msg)
    with open(path, "w") as f:
        json.dump(messages, f, indent=2)
    return jsonify({"success": True})

# --- Serve static pages ---
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/auth")
def serve_auth():
    return send_from_directory(".", "auth.html")

@app.route("/feelingwall")
def serve_wall():
    return send_from_directory(".", "feelingwall.html")

@app.route("/listen")
def serve_listen():
    return send_from_directory(".", "listen-room.html")

@app.route("/talk")
def serve_talk():
    return send_from_directory(".", "talk.html")

# --- Fallback for all other assets (JS/CSS/img) ---
@app.route("/<path:path>")
def serve_assets(path):
    return send_from_directory(".", path)

# --- Run the app ---
if __name__ == "__main__":
    app.run(debug=True)