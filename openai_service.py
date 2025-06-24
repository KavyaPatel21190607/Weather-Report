import os
import json
import logging
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the OpenAI client
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
client = OpenAI(api_key=OPENAI_API_KEY)

# System message to guide the AI's responses
SYSTEM_MESSAGE = """
You are a helpful, empathetic farming assistant dedicated to supporting farmers. Your role is to:
1. Provide accurate, practical information about farming techniques, crops, and best practices
2. Explain government schemes and policies that benefit farmers in a clear, accessible way
3. Clarify farming laws and regulations in simple terms
4. Show empathy and understanding when farmers express challenges or frustrations
5. Offer weather-related advice for farming activities
6. Always be respectful and considerate of traditional farming knowledge

Respond in a warm, supportive tone while maintaining accuracy and providing actionable advice.
Keep responses concise yet comprehensive, focusing on practical information farmers can apply.
"""

def generate_response(user_message):
    """
    Generate a response to the user's message using OpenAI's GPT model or fallback to static responses.
    
    Args:
        user_message (str): The message from the user
        
    Returns:
        str: The generated response
    """
    try:
        # Check if the API key is available
        if not OPENAI_API_KEY:
            logger.error("OpenAI API key is not available.")
            return get_fallback_response(user_message)
        
        # Detect if the user is asking about specific farming categories
        farming_keywords = {
            'weather': ['weather', 'rain', 'forecast', 'temperature', 'climate', 'monsoon', 'humidity'],
            'crops': ['crop', 'plant', 'seed', 'harvest', 'cultivation', 'grow', 'yield'],
            'schemes': ['scheme', 'subsidy', 'government', 'loan', 'grant', 'support', 'policy', 'program'],
            'laws': ['law', 'regulation', 'legal', 'act', 'rule', 'compliance', 'guideline']
        }
        
        category = 'general'
        for key, keywords in farming_keywords.items():
            if any(keyword in user_message.lower() for keyword in keywords):
                category = key
                break
        
        # Add category-specific guidance to the prompt
        additional_context = ""
        if category == 'weather':
            additional_context = "Focus on weather implications for farming and practical advice related to the current weather conditions."
        elif category == 'crops':
            additional_context = "Provide detailed, practical information about crop cultivation, care, and best practices."
        elif category == 'schemes':
            additional_context = "Explain relevant government schemes for farmers clearly, including eligibility criteria and application process."
        elif category == 'laws':
            additional_context = "Explain farming laws and regulations in simple, accessible language, focusing on practical implications."
        
        # Create the complete prompt
        content = f"{additional_context}\n\nFarmer's message: {user_message}"
        
        try:
            # Try with gpt-4o first
            # The newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": SYSTEM_MESSAGE},
                    {"role": "user", "content": content}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            return response.choices[0].message.content.strip()
        except Exception as api_error:
            logger.error(f"Error with OpenAI API: {api_error}")
            # Fall back to static responses
            return get_fallback_response(user_message)
    
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return get_fallback_response(user_message)

def get_fallback_response(user_message):
    """
    Provide a fallback response when OpenAI API is unavailable.
    
    Args:
        user_message (str): The message from the user
        
    Returns:
        str: A relevant fallback response based on the message content
    """
    user_message = user_message.lower()
    
    # Check for common greeting patterns
    if any(greeting in user_message for greeting in ['hello', 'hi', 'hey', 'greetings', 'namaste']):
        return "Hello! I'm your farming assistant. I can provide information about farming techniques, crops, government schemes, and weather-related advice. How can I help you today?"
    
    # Check for farming techniques related queries
    if any(keyword in user_message for keyword in ['technique', 'farming method', 'how to farm', 'cultivat', 'agriculture']):
        return """Here are some common farming techniques:

1. **Organic Farming**: Uses natural methods without synthetic chemicals, focusing on soil health and biodiversity.

2. **Conservation Agriculture**: Minimizes soil disturbance, maintains permanent soil cover, and practices crop rotation.

3. **Precision Farming**: Uses technology to optimize inputs based on field variability.

4. **Integrated Farming**: Combines crop production with livestock, fishery, or poultry for efficient resource use.

5. **Crop Rotation**: Growing different crops in sequence to maintain soil health and prevent pest buildup.

Would you like more specific information about any of these techniques?"""
    
    # Check for crop related queries
    if any(keyword in user_message for keyword in ['crop', 'plant', 'seed', 'harvest', 'grow']):
        return """Common crops and growing tips:

1. **Rice**: Requires flooded conditions, transplanting in puddled soil, and proper water management.

2. **Wheat**: Needs well-drained soil, timely sowing, and 4-5 irrigations during the growing season.

3. **Cotton**: Requires deep, well-drained soil, regular pest monitoring, and proper spacing.

4. **Pulses**: Generally drought-resistant, benefit from Rhizobium inoculation, and improve soil fertility.

For specific crop advice, please provide more details about your region and growing conditions."""
    
    # Check for government scheme related queries
    if any(keyword in user_message for keyword in ['scheme', 'subsidy', 'government', 'loan', 'support']):
        return """Key government schemes for farmers:

1. **PM-KISAN**: Provides income support of ₹6,000 per year to eligible farmer families.

2. **Pradhan Mantri Fasal Bima Yojana**: Crop insurance scheme that covers losses due to natural calamities.

3. **Kisan Credit Card**: Offers credit at subsidized interest rates for cultivation and other farm needs.

4. **Pradhan Mantri Krishi Sinchayee Yojana**: Focuses on improving irrigation efficiency and water conservation.

5. **National Mission for Sustainable Agriculture**: Promotes sustainable farming practices and climate resilience.

For application procedures and eligibility criteria, please contact your local agriculture office."""
    
    # Check for weather related queries
    if any(keyword in user_message for keyword in ['weather', 'rain', 'climate', 'monsoon']):
        return """Weather plays a crucial role in farming. Here are some general weather-related farming tips:

1. Keep track of local weather forecasts to plan field operations.

2. Avoid applying fertilizers or pesticides before expected rainfall.

3. In high temperatures, ensure adequate irrigation and consider mulching.

4. During high humidity periods, monitor for fungal diseases.

5. Have contingency plans ready for extreme weather events.

For location-specific weather information, please use the weather widget in the sidebar."""
    
    # Default response if no specific topic is detected
    return """I'm here to help with farming-related questions. I can provide information about:

• Farming techniques and crop information
• Government schemes for farmers
• Farming laws and regulations
• Weather-related farming advice

Please ask a specific question about any of these topics, and I'll do my best to assist you."""

def get_farming_information(topic, query):
    """
    Get specific farming information using OpenAI's GPT model.
    
    Args:
        topic (str): The general farming topic (techniques, schemes, laws)
        query (str): The specific query about the topic
        
    Returns:
        dict: The structured information about the topic
    """
    try:
        # Check if the API key is available
        if not OPENAI_API_KEY:
            logger.error("OpenAI API key is not available.")
            return {"error": "Service unavailable due to configuration issues."}
        
        # Create prompts based on the topic
        if topic == "techniques":
            system_prompt = "You are an expert in farming techniques. Provide detailed, practical information about farming methods, crops, and best practices."
        elif topic == "schemes":
            system_prompt = "You are an expert in government schemes for farmers. Explain schemes clearly, including eligibility criteria and application processes."
        elif topic == "laws":
            system_prompt = "You are an expert in agricultural laws and regulations. Explain farming laws in simple, accessible language, focusing on practical implications."
        else:
            system_prompt = "You are an expert in farming. Provide accurate, practical information about the requested topic."
        
        user_prompt = f"Provide detailed information about: {query}\n\nRespond with a JSON object with the following structure: {{\"title\": \"...\", \"summary\": \"...\", \"details\": \"...\", \"recommendation\": \"...\"}}"
        
        # The newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    except Exception as e:
        logger.error(f"Error getting farming information: {e}")
        return {"error": "Failed to retrieve information. Please try again later."}
