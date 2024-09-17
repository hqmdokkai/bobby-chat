from flask import Flask, render_template, session, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, auth, firestore
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = '7x2mxTlL4aONKLM1nygDNNk2Wfnk31at'

# Cấu hình Firebase với file JSON của bạn
cred = credentials.Certificate('app-chat2014-firebase-adminsdk-ot8k4-ae22974eb0.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Firestore collections
users_ref = db.collection('users')
messages_ref = db.collection('messages')

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Lấy người dùng từ Firestore
        user_doc = users_ref.where('username', '==', username).limit(1).get()

        if user_doc:
            user = user_doc[0].to_dict()
            if user['password'] == password:
                session['username'] = username
                return redirect(url_for('chat'))
        return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Lưu người dùng vào Firestore mà không mã hóa mật khẩu
        users_ref.add({
            'username': username,
            'password': password
        })
        return redirect(url_for('login'))
    
    return render_template('register.html')
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        recipient = request.form['recipient']
        message = request.form['message']
        sender = session['username']

        # Lưu tin nhắn vào Firestore
        messages_ref.add({
            'sender': sender,
            'recipient': recipient,
            'message': message
        })

    # Lấy tất cả tin nhắn từ Firestore
    all_messages = messages_ref.stream()
    messages = [msg.to_dict() for msg in all_messages]

    # Lọc tin nhắn để phù hợp với người dùng hiện tại
    filtered_messages = []
    for message in messages:
        if message['sender'] == session['username'] or message['recipient'] == session['username']:
            filtered_messages.append(message)

    return render_template('chat.html', username=session['username'], messages=filtered_messages)
@app.route('/logout')
def logout():
    session.pop('username', None)  # Thay 'user_id' bằng 'username'
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
