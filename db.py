from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    chats = db.relationship('ChatHistory', backref='user', lazy=True, cascade="all, delete-orphan")

    def __init__(self, name=None, email=None, password_hash=None, **kwargs):
        super().__init__(**kwargs)
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if password_hash is not None:
            self.password_hash = password_hash

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class ChatHistory(db.Model):
    __tablename__ = 'chat_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user_message = db.Column(db.Text, nullable=False)
    bot_reply = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id=None, user_message=None, bot_reply=None, **kwargs):
        super().__init__(**kwargs)
        if user_id is not None:
            self.user_id = user_id
        if user_message is not None:
            self.user_message = user_message
        if bot_reply is not None:
            self.bot_reply = bot_reply

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_message": self.user_message,
            "bot_reply": self.bot_reply,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }


def init_db(app):
    """Initialize database and create tables if they do not exist"""
    db.init_app(app)
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print("Database table initialization note:", e)
