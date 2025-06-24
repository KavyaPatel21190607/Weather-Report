import os
import requests
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Weather API configuration (using OpenWeatherMap as an example)
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY", "")
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_API_URL = "https://api.openweathermap.org/data/2.5/forecast"

def get_weather_data(location):
    """
    Get current weather data for a specific location.
    
    Args:
        location (str): The name of the location to get weather data for
        
    Returns:
        dict: Weather data including current conditions and farming recommendations
    """
    try:
        # Check if the API key is available
        if not WEATHER_API_KEY:
            logger.warning("Weather API key is not available. Using mock data.")
            return get_fallback_weather_data(location)
        
        # Get current weather
        params = {
            'q': location,
            'appid': WEATHER_API_KEY,
            'units': 'metric'  # Use metric units (Celsius)
        }
        
        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()  # Raise an exception for 4XX/5XX responses
        
        weather_data = response.json()
        
        # Get 5-day forecast
        forecast_params = {
            'q': location,
            'appid': WEATHER_API_KEY,
            'units': 'metric',
            'cnt': 40  # Get 40 data points (5 days, every 3 hours)
        }
        
        forecast_response = requests.get(FORECAST_API_URL, params=forecast_params)
        forecast_response.raise_for_status()
        
        forecast_data = forecast_response.json()
        
        # Process and extract relevant weather information
        processed_data = process_weather_data(weather_data, forecast_data)
        
        return processed_data
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather data: {e}")
        return get_fallback_weather_data(location)

def process_weather_data(current_data, forecast_data):
    """
    Process raw weather data into a format useful for farmers.
    
    Args:
        current_data (dict): Current weather data from the API
        forecast_data (dict): Forecast weather data from the API
        
    Returns:
        dict: Processed weather data with farming recommendations
    """
    # Extract current weather information
    current_temp = current_data['main']['temp']
    current_humidity = current_data['main']['humidity']
    current_wind_speed = current_data['wind']['speed']
    current_weather_desc = current_data['weather'][0]['description']
    current_weather_icon = current_data['weather'][0]['icon']
    
    # Extract forecast information (next 5 days)
    forecast_days = []
    date_processed = set()
    
    for item in forecast_data['list']:
        # Extract date (without time)
        date_str = item['dt_txt'].split(' ')[0]
        
        # Only process each date once
        if date_str not in date_processed and len(date_processed) < 5:
            date_processed.add(date_str)
            
            forecast_days.append({
                'date': date_str,
                'temp': item['main']['temp'],
                'humidity': item['main']['humidity'],
                'description': item['weather'][0]['description'],
                'icon': item['weather'][0]['icon']
            })
    
    # Generate farming recommendations based on weather conditions
    farming_recommendations = generate_farming_recommendations(current_data, forecast_data)
    
    # Prepare the final weather data
    processed_data = {
        'location': current_data['name'],
        'country': current_data['sys']['country'],
        'current': {
            'temperature': current_temp,
            'humidity': current_humidity,
            'wind_speed': current_wind_speed,
            'description': current_weather_desc,
            'icon': f"http://openweathermap.org/img/wn/{current_weather_icon}@2x.png"
        },
        'forecast': forecast_days,
        'farming_recommendations': farming_recommendations
    }
    
    return processed_data

def generate_farming_recommendations(current_data, forecast_data):
    """
    Generate farming recommendations based on weather conditions.
    
    Args:
        current_data (dict): Current weather data
        forecast_data (dict): Forecast weather data
        
    Returns:
        list: Farming recommendations based on weather conditions
    """
    recommendations = []
    
    # Check current temperature
    current_temp = current_data['main']['temp']
    if current_temp > 35:
        recommendations.append("High temperature alert! Ensure crops have adequate water. Consider overhead sprinkling for cooling effect.")
    elif current_temp < 10:
        recommendations.append("Low temperature alert! Protect sensitive crops from frost. Use covers or heaters if available.")
    
    # Check humidity
    current_humidity = current_data['main']['humidity']
    if current_humidity > 80:
        recommendations.append("High humidity detected. Monitor for fungal diseases and mildew. Apply fungicides if necessary.")
    elif current_humidity < 30:
        recommendations.append("Low humidity detected. Increase irrigation and consider mulching to retain soil moisture.")
    
    # Check for rain in the forecast
    rain_expected = False
    for item in forecast_data['list'][:8]:  # Check next 24 hours
        if 'rain' in item:
            rain_expected = True
            break
    
    if rain_expected:
        recommendations.append("Rain expected in the next 24 hours. Hold off on applying fertilizers or pesticides.")
    else:
        recommendations.append("No significant rain expected in the next 24 hours. Good opportunity for field operations.")
    
    # Check wind conditions
    current_wind = current_data['wind']['speed']
    if current_wind > 5:  # Wind speed in m/s
        recommendations.append("Moderate to high winds expected. Avoid spraying operations and secure young plants.")
    
    # Add seasonal recommendation based on current month
    month = datetime.now().month
    if 3 <= month <= 5:  # Spring (Northern Hemisphere)
        recommendations.append("Spring season: Good time for planting summer crops. Prepare fields and ensure adequate nutrition.")
    elif 6 <= month <= 8:  # Summer
        recommendations.append("Summer season: Monitor irrigation needs carefully. Consider shade for sensitive crops.")
    elif 9 <= month <= 11:  # Fall
        recommendations.append("Fall season: Prepare for harvest operations. Monitor storage conditions for harvested crops.")
    else:  # Winter
        recommendations.append("Winter season: Focus on winter crops and preparation for spring planting. Protect soil from erosion.")
    
    return recommendations

def get_fallback_weather_data(location):
    """
    Provide fallback weather data when the API call fails.
    
    Args:
        location (str): The location name
        
    Returns:
        dict: Basic weather information with a message about the API failure
    """
    return {
        'location': location,
        'country': 'Unknown',
        'current': {
            'temperature': 'N/A',
            'humidity': 'N/A',
            'wind_speed': 'N/A',
            'description': 'Weather data unavailable',
            'icon': ''
        },
        'forecast': [],
        'error': 'Unable to fetch weather data. Please try again later.',
        'farming_recommendations': [
            "Weather data is currently unavailable. Please check your local weather service for accurate forecasts.",
            "In the absence of weather data, monitor your fields regularly and follow standard seasonal practices."
        ]
    }
