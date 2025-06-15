import os
from langsmith import traceable
import requests
import time
from dotenv import load_dotenv
load_dotenv()

# Example 1: Trace a simple data processing function
@traceable
def process_data(data: list) -> list:
    """Process a list of numbers (doubles each value)"""
    processed = [x * 2 for x in data]
    time.sleep(0.5)  # Simulate processing time
    return processed

# Example 2: Trace an external API call
@traceable
def fetch_weather(city: str) -> dict:
    """Fetch weather data from a public API"""
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=your_api_key")
    response.raise_for_status()
    return response.json()

# Example 3: Trace a function with error handling 
@traceable
def risky_operation(value: int) -> str:
    """Simulate a function that might fail"""
    if value < 0:
        raise ValueError("Negative values are not allowed")
    return f"Success: {value}"

if __name__ == "__main__":
    # Trace a data processing pipeline
    try:
        raw_data = [1, 2, 3, 4]
        processed = process_data(raw_data)
        print(f"Processed data: {processed}")
        
        weather = fetch_weather("Monaco")
        print(f"Weather in Monaco: {weather['weather'][0]['description']}")
        
        result = risky_operation(10)
        print(result)
        
        # This would create an error trace
        risky_operation(-5)
        
    except Exception as e:
        print(f"Caught error: {str(e)}")
