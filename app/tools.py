# backend/app/tools.py

import os
import requests
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
print("OPENWEATHER_API_KEY loaded:", "✓" if OPENWEATHER_API_KEY else "✗")

@tool
def get_weather(city: str) -> str:
    """
    Get the current weather for a specified city.
    Use this tool when users ask about weather conditions, temperature, or climate in a specific location.
    
    Args:
        city: The name of the city to get weather for (e.g., "Pune", "Mumbai", "New York")
    
    Returns:
        A string describing the current weather conditions including temperature, humidity, and description
    """
    try:
        # Check if API key is configured
        if not OPENWEATHER_API_KEY:
            return "Weather API key not configured. Please set OPENWEATHER_API_KEY in your .env file. You can get a free API key from https://openweathermap.org/"
        
        # OpenWeatherMap API endpoint
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"  # Use Celsius
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract relevant weather information
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]
        
        weather_report = (
            f"Current weather in {city}:\n"
            f"🌡️ Temperature: {temp}°C (feels like {feels_like}°C)\n"
            f"☁️ Conditions: {description.capitalize()}\n"
            f"💧 Humidity: {humidity}%\n"
            f"💨 Wind Speed: {wind_speed} m/s"
        )
        
        return weather_report
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            return "Invalid weather API key. Please check your OPENWEATHER_API_KEY in .env file."
        elif e.response.status_code == 404:
            return f"City '{city}' not found. Please check the spelling and try again."
        else:
            return f"Sorry, I couldn't fetch weather data for {city}. Error: {e.response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Sorry, I couldn't connect to the weather service. Please check your internet connection."
    except KeyError as e:
        return f"Sorry, I received incomplete weather data. Please try again."
    except Exception as e:
        print(f"Unexpected error in get_weather: {str(e)}")
        return f"An unexpected error occurred while fetching weather data."

@tool
def calculate(expression: str) -> str:
    """
    Perform mathematical calculations safely.
    Use this when users ask to calculate, compute, or solve mathematical expressions.
    
    Args:
        expression: A mathematical expression to evaluate (e.g., "2 + 2", "15 * 8", "100 / 5")
    
    Returns:
        The result of the calculation
    """
    try:
        # Only allow safe mathematical operations
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in expression):
            return "Sorry, I can only perform basic arithmetic operations (+, -, *, /)."
        
        # Evaluate the expression
        result = eval(expression)
        return f"The result of {expression} is {result}"
    except ZeroDivisionError:
        return "Cannot divide by zero!"
    except Exception as e:
        print(f"Calculation error: {str(e)}")
        return f"Sorry, I couldn't calculate that expression. Please check the format."

# Test function
if __name__ == "__main__":
    print("\n=== Testing Tools ===")
    print("\n1. Testing calculator:")
    print(calculate.invoke("2 + 2"))
    print(calculate.invoke("15 * 8"))
    
    print("\n2. Testing weather (will fail without API key):")
    print(get_weather.invoke("Pune"))