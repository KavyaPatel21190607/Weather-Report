# 

## Overview

Kissan Kalyan (Partner) is a comprehensive farming assistant chatbot designed to provide farmers with expert knowledge, weather updates, and information about government schemes and regulations. Built with a user-friendly interface, this application aims to support farmers with practical information and empathetic responses.

## Features

- **Interactive Chatbot**: Provides information on farming techniques, crops, and best practices with an empathetic approach
- **Real-time Weather Data**: Displays current weather information and forecasts for any location with farming-specific recommendations
- **Government Schemes**: Offers details about agricultural subsidies, loans, and support programs
- **Farming Laws**: Explains regulations and legal aspects of farming in simple terms
- **Light/Dark Mode**: User-friendly interface with theme toggle for comfortable viewing in any environment
- **Database Integration**: PostgreSQL database to store chat history and weather queries
- **Mobile Responsive**: Works smoothly on both desktop and mobile devices

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript (No frameworks)
- **Backend**: Python with Flask
- **Database**: PostgreSQL
- **APIs**:
  - OpenAI API for intelligent chatbot responses
  - OpenWeatherMap API for weather data

## Installation

### Prerequisites

- Python 3.11 or later
- PostgreSQL database
- OpenAI API key
- OpenWeatherMap API key

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/kissan-kalyan-partner.git
   cd kissan-kalyan-partner
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txtKissan Kalyan (Partner) - Farming Chatbot
   ```

3. Set up environment variables:
   Create a `.env` file with the following variables:
   ```
   OPENAI_API_KEY=your_openai_api_key
   WEATHER_API_KEY=your_openweathermap_api_key
   DATABASE_URL=your_database_url
   SESSION_SECRET=your_session_secret
   ```

4. Initialize the database:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. Run the application:
   ```
   python main.py
   ```

6. Access the application in your browser at `http://localhost:5000`

## Usage

### Chatbot

- Ask questions about farming techniques, crops, or agricultural practices
- Inquire about government schemes and subsidies available for farmers
- Get information about farming laws and regulations
- Receive weather-based farming recommendations

### Weather Widget

- View current weather conditions for any location
- Get farming-specific recommendations based on weather
- See a 5-day forecast to help plan farming activities

### Quick Links

- Use the quick links in the sidebar to get immediate information on specific topics
- Access common farming queries with a single click

## Fallback Mechanism

The application includes a robust fallback system that ensures responses even when the OpenAI API is unavailable or rate-limited. This guarantees farmers can always access essential information.

## Database Schema

The application uses a PostgreSQL database with the following main tables:

- **ChatMessage**: Stores conversation history between users and the chatbot
- **WeatherRequest**: Records weather queries and data for analysis

## Project Structure

```
kissan-kalyan-partner/
├── static/                # Static assets
│   ├── chatbot.js         # Frontend JavaScript for chatbot functionality  
│   └── style.css          # CSS styling for the application
├── templates/             # HTML templates
│   └── index.html         # Main application page
├── app.py                 # Flask application and routes
├── database.py            # Database models and configuration
├── farming_data.py        # Farming information data source
├── main.py                # Application entry point
├── openai_service.py      # Integration with OpenAI API
├── weather.py             # Weather data processing and recommendations
└── README.md              # Project documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing the GPT models that power the chatbot
- OpenWeatherMap for weather data API
- All contributors and farming experts who helped improve the content

---

Created with ❤️ for farmers