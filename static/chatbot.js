// Smart Farming Chatbot - Front-end JavaScript

// DOM elements
let chatContainer;
let chatMessages;
let userInput;
let sendButton;
let weatherWidget;
let helpButton;
let clearButton;

// Chatbot state
let conversationHistory = [];
let isTyping = false;
let weatherData = null;

// Initialize the chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initializeChat();
    fetchWeatherData();
    initializeThemeToggle();
});

/**
 * Initialize the chat interface and event listeners
 */
function initializeChat() {
    // Get DOM elements
    chatContainer = document.getElementById('chat-container');
    chatMessages = document.getElementById('chat-messages');
    userInput = document.getElementById('user-input');
    sendButton = document.getElementById('send-button');
    weatherWidget = document.getElementById('weather-widget');
    helpButton = document.getElementById('help-button');
    clearButton = document.getElementById('clear-button');
    
    // Set up event listeners
    sendButton.addEventListener('click', handleUserInput);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleUserInput();
        }
    });
    
    helpButton.addEventListener('click', showHelpGuide);
    clearButton.addEventListener('click', clearChat);
    
    // Display welcome message
    const welcomeMessage = `
        👨‍🌾 Welcome to the Smart Farming Assistant! 
        
        I'm here to help you with:
        • Farming techniques and crop information
        • Government schemes for farmers
        • Farming laws and regulations
        • Weather-related farming advice
        
        How can I assist you today?
    `;
    
    addBotMessage(welcomeMessage);
}

/**
 * Handle user input submission
 */
function handleUserInput() {
    const message = userInput.value.trim();
    
    if (message === '' || isTyping) {
        return;
    }
    
    // Add user message to chat
    addUserMessage(message);
    
    // Clear input field
    userInput.value = '';
    
    // Process quick commands
    if (processQuickCommands(message)) {
        return;
    }
    
    // Show typing indicator
    showTypingIndicator();
    
    // Send message to backend for processing
    sendMessageToBackend(message);
}

/**
 * Process quick commands like 'weather', 'help', etc.
 * @param {string} message - The user's message
 * @returns {boolean} - True if a command was processed, false otherwise
 */
function processQuickCommands(message) {
    const lowerMessage = message.toLowerCase();
    
    // Process weather command
    if (lowerMessage === 'weather' || lowerMessage.startsWith('weather ')) {
        const location = lowerMessage === 'weather' ? 'Delhi' : lowerMessage.substring(8).trim();
        fetchWeatherData(location);
        addBotMessage(`Fetching weather information for ${location}...`);
        return true;
    }
    
    // Process help command
    if (lowerMessage === 'help' || lowerMessage === '/help') {
        showHelpGuide();
        return true;
    }
    
    // Process clear command
    if (lowerMessage === 'clear' || lowerMessage === '/clear') {
        clearChat();
        return true;
    }
    
    return false;
}

/**
 * Send a message to the backend for processing
 * @param {string} message - The user's message
 */
function sendMessageToBackend(message) {
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Hide typing indicator
        hideTypingIndicator();
        
        // Add bot response to chat
        if (data.response) {
            addBotMessage(data.response);
        } else {
            addBotMessage("I'm sorry, I couldn't process your request. Please try again.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        hideTypingIndicator();
        addBotMessage("I'm having trouble connecting to my knowledge base. Please try again later.");
    });
}

/**
 * Add a user message to the chat
 * @param {string} message - The user's message
 */
function addUserMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.className = 'message user-message';
    messageElement.innerHTML = `<p>${escapeHTML(message)}</p>`;
    
    chatMessages.appendChild(messageElement);
    
    // Save to conversation history
    conversationHistory.push({ role: 'user', content: message });
    
    // Scroll to bottom
    scrollToBottom();
}

/**
 * Add a bot message to the chat
 * @param {string} message - The bot's message
 */
function addBotMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.className = 'message bot-message';
    
    // Process the message for formatting
    const formattedMessage = formatMessage(message);
    
    messageElement.innerHTML = `
        <div class="bot-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            ${formattedMessage}
        </div>
    `;
    
    chatMessages.appendChild(messageElement);
    
    // Save to conversation history
    conversationHistory.push({ role: 'assistant', content: message });
    
    // Scroll to bottom
    scrollToBottom();
}

/**
 * Format the message with Markdown-like syntax
 * @param {string} message - The message to format
 * @returns {string} - The formatted HTML
 */
function formatMessage(message) {
    // Replace URLs with clickable links
    let formatted = message.replace(
        /(https?:\/\/[^\s]+)/g, 
        '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
    );
    
    // Replace bullet points with proper HTML
    formatted = formatted.replace(/^\s*[•*]\s+(.+)$/gm, '<li>$1</li>');
    formatted = formatted.replace(/<li>(.+?)<\/li>(?:\s*<li>)/g, '<li>$1</li><li>');
    
    // Wrap lists in ul tags
    if (formatted.includes('<li>')) {
        const parts = formatted.split(/<li>/);
        let result = parts[0];
        if (parts.length > 1) {
            result += '<ul><li>' + parts.slice(1).join('<li>');
            result = result.replace(/(<\/li>)(?![\s\S]*<li>)/g, '$1</ul>');
        }
        formatted = result;
    }
    
    // Split by newlines and wrap in paragraphs
    formatted = formatted
        .split('\n\n')
        .map(para => para.trim() ? `<p>${para.replace(/\n/g, '<br>')}</p>` : '')
        .join('');
    
    // Bold text between **
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Italic text between *
    formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    return formatted;
}

/**
 * Show the typing indicator
 */
function showTypingIndicator() {
    isTyping = true;
    
    const typingElement = document.createElement('div');
    typingElement.className = 'message bot-message typing-indicator';
    typingElement.id = 'typing-indicator';
    
    typingElement.innerHTML = `
        <div class="bot-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="typing-animation">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;
    
    chatMessages.appendChild(typingElement);
    
    // Scroll to bottom
    scrollToBottom();
}

/**
 * Hide the typing indicator
 */
function hideTypingIndicator() {
    isTyping = false;
    
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

/**
 * Scroll to the bottom of the chat
 */
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Fetch weather data from the backend
 * @param {string} location - The location to get weather for (default: Delhi)
 */
function fetchWeatherData(location = 'Delhi') {
    fetch(`/api/weather?location=${encodeURIComponent(location)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Weather data not available');
            }
            return response.json();
        })
        .then(data => {
            weatherData = data;
            updateWeatherWidget();
        })
        .catch(error => {
            console.error('Error fetching weather:', error);
            weatherWidget.innerHTML = `
                <div class="weather-error">
                    <p>Weather data unavailable</p>
                    <p>Please try again later</p>
                </div>
            `;
        });
}

/**
 * Update the weather widget with current data
 */
function updateWeatherWidget() {
    if (!weatherData) {
        return;
    }
    
    const current = weatherData.current;
    
    // Create weather widget HTML
    weatherWidget.innerHTML = `
        <div class="weather-header">
            <h3>Weather: ${weatherData.location}</h3>
        </div>
        <div class="weather-current">
            <div class="weather-icon">
                ${current.icon ? `<img src="${current.icon}" alt="Weather Icon">` : '<i class="fas fa-cloud"></i>'}
            </div>
            <div class="weather-details">
                <p class="temp">${typeof current.temperature === 'number' ? `${current.temperature.toFixed(1)}°C` : 'N/A'}</p>
                <p>${current.description || 'Weather data unavailable'}</p>
            </div>
        </div>
        <div class="weather-info">
            <p><i class="fas fa-tint"></i> Humidity: ${typeof current.humidity === 'number' ? `${current.humidity}%` : 'N/A'}</p>
            <p><i class="fas fa-wind"></i> Wind: ${typeof current.wind_speed === 'number' ? `${current.wind_speed} m/s` : 'N/A'}</p>
        </div>
        <div class="weather-farming-tips">
            <h4>Farming Tips:</h4>
            <ul>
                ${weatherData.farming_recommendations ? 
                    weatherData.farming_recommendations.slice(0, 2).map(tip => `<li>${tip}</li>`).join('') : 
                    '<li>No recommendations available</li>'}
            </ul>
            <button id="weather-more-tips" class="small-button">More Tips</button>
        </div>
    `;
    
    // Add event listener for the "More Tips" button
    document.getElementById('weather-more-tips').addEventListener('click', () => {
        if (weatherData && weatherData.farming_recommendations) {
            const tipsMessage = `
                **Weather-Based Farming Recommendations:**
                
                ${weatherData.farming_recommendations.map(tip => `• ${tip}`).join('\n\n')}
            `;
            addBotMessage(tipsMessage);
        }
    });
}

/**
 * Show the help guide
 */
function showHelpGuide() {
    const helpMessage = `
        **Smart Farming Assistant - Help Guide**
        
        **General Commands:**
        • **help** or **/help** - Display this help guide
        • **clear** or **/clear** - Clear the chat history
        • **weather [location]** - Get weather for a location (default: Delhi)
        
        **Topics You Can Ask About:**
        • **Farming Techniques** - Information about various farming methods, crop cultivation, etc.
        • **Government Schemes** - Details about government programs and subsidies for farmers
        • **Farming Laws** - Information about agricultural laws and regulations
        • **Weather Advice** - Get farming recommendations based on weather conditions
        
        **Example Questions:**
        • "How do I grow rice?"
        • "Tell me about organic farming techniques"
        • "What government schemes are available for small farmers?"
        • "What are the best practices for soil management?"
        • "Explain water conservation techniques for farming"
        • "What are the regulations regarding pesticide use?"
    `;
    
    addBotMessage(helpMessage);
}

/**
 * Clear the chat history
 */
function clearChat() {
    // Clear the UI
    chatMessages.innerHTML = '';
    
    // Reset conversation history
    conversationHistory = [];
    
    // Show welcome message again
    const welcomeMessage = `
        👨‍🌾 Welcome to the Smart Farming Assistant! 
        
        I'm here to help you with:
        • Farming techniques and crop information
        • Government schemes for farmers
        • Farming laws and regulations
        • Weather-related farming advice
        
        How can I assist you today?
    `;
    
    addBotMessage(welcomeMessage);
}

/**
 * Escape HTML to prevent XSS
 * @param {string} unsafe - The unsafe string
 * @returns {string} - The escaped string
 */
function escapeHTML(unsafe) {
    return unsafe
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

/**
 * Initialize theme toggle functionality
 */
function initializeThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    
    // Check for saved theme preference or use preferred-color-scheme
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.setAttribute('data-theme', 'dark');
        themeToggle.checked = true;
    } else if (savedTheme === 'light') {
        document.body.setAttribute('data-theme', 'light');
        themeToggle.checked = false;
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.body.setAttribute('data-theme', 'dark');
        themeToggle.checked = true;
    }
    
    // Add event listener for theme switch
    themeToggle.addEventListener('change', function() {
        if (this.checked) {
            document.body.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.body.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
        }
    });
}
