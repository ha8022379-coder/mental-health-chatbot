from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sentiment import detect_emotion
from groq import Groq
from config import GROQ_API_KEY
from datetime import datetime
import os
import requests

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = "mentalhealth2024secretkey"

# Groq AI client
client = Groq(api_key=GROQ_API_KEY)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---- DATABASE MODELS ----

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user_message = db.Column(db.String(500))
    emotion = db.Column(db.String(50))
    bot_response = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

# ---- AI FUNCTION ----

def get_ai_response(user_message, emotion):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": f"""You are a compassionate mental health support chatbot.
                    The user is feeling {emotion}.
                    Follow these rules strictly:
                    1. DO NOT always start with I'm sorry
                    2. Give PRACTICAL advice or tips when possible
                    3. Suggest real solutions like breathing exercises, talking to someone, taking a walk, journaling etc
                    4. Be warm and human-like but also HELPFUL
                    5. Sometimes validate feelings, sometimes give advice, sometimes share a helpful tip
                    6. Ask ONE follow up question at the end
                    7. Keep response to 3-4 sentences maximum
                    8. Never give medical diagnoses
                    9. For serious issues always recommend professional help
                    10. Vary your responses - don't follow same pattern every time"""
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=150
        )
        response = completion.choices[0].message.content
        print(f"Groq Response: {response}")
        return response
    except Exception as e:
        print(f"Groq Error: {e}")
        return "I'm here for you 💙 Can you tell me more about how you're feeling?"

# ---- AUTH ROUTES ----

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name', '')
    email = data.get('email', '')
    password = data.get('password', '')

    if not name or not email or not password:
        return jsonify({"error": "All fields are required!"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already registered!"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    session['user_id'] = new_user.id
    session['user_name'] = new_user.name

    return jsonify({
        "message": "Account created successfully!",
        "name": new_user.name
    })

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email', '')
    password = data.get('password', '')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password!"}), 401

    session['user_id'] = user.id
    session['user_name'] = user.name

    return jsonify({
        "message": "Login successful!",
        "name": user.name
    })

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully!"})

@app.route('/check-session', methods=['GET'])
def check_session():
    if 'user_id' in session:
        return jsonify({
            "logged_in": True,
            "name": session['user_name']
        })
    return jsonify({"logged_in": False})

# ---- CHAT ROUTE ----

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')

    emotion = detect_emotion(user_message)
    bot_response = get_ai_response(user_message, emotion)

    chat = ChatHistory(
        user_id=session.get('user_id'),
        user_message=user_message,
        emotion=emotion,
        bot_response=bot_response
    )
    db.session.add(chat)
    db.session.commit()

    return jsonify({
        "emotion": emotion,
        "response": bot_response
    })

# ---- PAGES ----

# Admin credentials
ADMIN_EMAIL = "admin@mindcare.com"
ADMIN_PASSWORD = "admin123"

@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    if data.get('email') == ADMIN_EMAIL and data.get('password') == ADMIN_PASSWORD:
        session['is_admin'] = True
        return jsonify({"message": "Admin login successful!"})
    return jsonify({"error": "Invalid admin credentials!"}), 401

@app.route('/admin/data', methods=['GET'])
def admin_data():
    if not session.get('is_admin'):
        return jsonify({"error": "Access denied!"}), 403

    users = User.query.all()
    chats = ChatHistory.query.order_by(ChatHistory.timestamp.desc()).limit(50).all()

    emotion_count = {}
    crisis_count = 0
    for chat in ChatHistory.query.all():
        emotion_count[chat.emotion] = emotion_count.get(chat.emotion, 0) + 1
        if chat.emotion == 'crisis':
            crisis_count += 1

    top_emotion = max(emotion_count, key=emotion_count.get) if emotion_count else '-'

    return jsonify({
        "total_users": len(users),
        "total_chats": ChatHistory.query.count(),
        "top_emotion": top_emotion,
        "crisis_count": crisis_count,
        "users": [{
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "created_at": u.created_at.strftime("%Y-%m-%d %H:%M")
        } for u in users],
        "recent_chats": [{
            "user_name": User.query.get(c.user_id).name if c.user_id else "Guest",
            "user_message": c.user_message,
            "emotion": c.emotion,
            "timestamp": c.timestamp.strftime("%Y-%m-%d %H:%M")
        } for c in chats]
    })

@app.route('/admin/delete-user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not session.get('is_admin'):
        return jsonify({"error": "Access denied!"}), 403

    user = User.query.get(user_id)
    if user:
        ChatHistory.query.filter_by(user_id=user_id).delete()
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted!"})
    return jsonify({"error": "User not found!"}), 404

@app.route('/admin-panel')
def admin_panel():
    return send_from_directory('.', 'admin.html')
@app.route('/admin-login')
def admin_login_page():
    return send_from_directory('.', 'admin_login.html')
@app.route('/')
def home():
    return send_from_directory('.', 'login.html')
@app.route('/history', methods=['GET'])
def history():
    user_id = session.get('user_id')
    if user_id:
        chats = ChatHistory.query.filter_by(user_id=user_id).all()
    else:
        chats = ChatHistory.query.all()
    return jsonify([{
        "user_message": c.user_message,
        "emotion": c.emotion,
        "bot_response": c.bot_response,
        "timestamp": c.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    } for c in chats])

@app.route('/chat-page')
def chat_page():
    return send_from_directory('.', 'index.html')
@app.route('/history-page')
def history_page():
    return send_from_directory('.', 'history.html')
@app.route('/mood-page')
def mood_page():
    return send_from_directory('.', 'mood.html')
@app.route('/urdu-tts')
def urdu_tts():
    text = request.args.get('text', '')
    url = f'https://translate.googleapis.com/translate_tts?ie=UTF-8&q={requests.utils.quote(text)}&tl=ur&client=gtx'
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    from flask import Response
    return Response(response.content, mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(debug=True)