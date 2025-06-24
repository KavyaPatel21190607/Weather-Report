"""Database setup and models for the farming chatbot."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

class ChatMessage(db.Model):
    """Model for storing chat messages."""
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, session_id, user_message, bot_response):
        self.session_id = session_id
        self.user_message = user_message
        self.bot_response = bot_response

class WeatherRequest(db.Model):
    """Model for storing weather requests."""
    __tablename__ = 'weather_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Float, nullable=True)
    humidity = db.Column(db.Float, nullable=True)
    description = db.Column(db.String(100), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, session_id, location, temperature=None, humidity=None, description=None):
        self.session_id = session_id
        self.location = location
        self.temperature = temperature
        self.humidity = humidity
        self.description = description