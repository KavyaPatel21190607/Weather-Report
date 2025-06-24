import os
import json
import logging
import uuid
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
import openai_service
import weather
import farming_data
from database import db, ChatMessage, WeatherRequest

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create and configure the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Load and validate database URL
database_uri = os.environ.get("DATABASE_URL", "sqlite:///kissan_kalyan.db")
app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

logger.debug(f"Using database URI: {database_uri}")

# Initialize the database with the app
db.init_app(app)

# Ensure all tables are created
with app.app_context():
    try:
        db.create_all()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")

@app.route('/')
def index():
    return render_template('index.html')

# ✅ New route for chatbot UI
@app.route('/chatbot')
def chatbot_ui():
    return render_template('chatbot.html')  # <-- Make sure this file exists in /templates

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())

        response = openai_service.generate_response(user_message)

        try:
            chat_entry = ChatMessage(
                session_id=session.get('session_id'),
                user_message=user_message,
                bot_response=response
            )
            db.session.add(chat_entry)
            db.session.commit()
            logger.info(f"Chat saved to database with ID: {chat_entry.id}")
        except Exception as db_error:
            logger.error(f"Database error saving chat: {db_error}")

        return jsonify({'response': response})
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({'error': 'Failed to process your message. Please try again.'}), 500

@app.route('/api/weather', methods=['GET'])
def get_weather():
    try:
        location = request.args.get('location', 'Delhi')
        weather_data = weather.get_weather_data(location)

        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())

        try:
            if 'current' in weather_data and isinstance(weather_data['current'], dict):
                weather_entry = WeatherRequest(
                    session_id=session.get('session_id'),
                    location=location,
                    temperature=weather_data['current'].get('temperature'),
                    humidity=weather_data['current'].get('humidity'),
                    description=weather_data['current'].get('description')
                )
                db.session.add(weather_entry)
                db.session.commit()
                logger.info(f"Weather data saved to database for location: {location}")
        except Exception as db_error:
            logger.error(f"Database error saving weather data: {db_error}")

        return jsonify(weather_data)
    except Exception as e:
        logger.error(f"Error fetching weather data: {e}")
        return jsonify({'error': 'Failed to fetch weather data. Please try again.'}), 500

@app.route('/api/farming/techniques', methods=['GET'])
def get_farming_techniques():
    try:
        category = request.args.get('category', 'all')
        techniques = farming_data.get_farming_techniques(category)
        return jsonify(techniques)
    except Exception as e:
        logger.error(f"Error fetching farming techniques: {e}")
        return jsonify({'error': 'Failed to fetch farming techniques. Please try again.'}), 500

@app.route('/api/farming/schemes', methods=['GET'])
def get_government_schemes():
    try:
        schemes = farming_data.get_government_schemes()
        return jsonify(schemes)
    except Exception as e:
        logger.error(f"Error fetching government schemes: {e}")
        return jsonify({'error': 'Failed to fetch government schemes. Please try again.'}), 500

@app.route('/api/farming/laws', methods=['GET'])
def get_farming_laws():
    try:
        laws = farming_data.get_farming_laws()
        return jsonify(laws)
    except Exception as e:
        logger.error(f"Error fetching farming laws: {e}")
        return jsonify({'error': 'Failed to fetch farming laws. Please try again.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
