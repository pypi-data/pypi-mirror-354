## server.py

from mcp.server.fastmcp import FastMCP
import requests
from bs4 import BeautifulSoup

mcp = FastMCP("WebExtractor")

@mcp.tool()
def extract_content(url: str) -> str:
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')            
        # Get text
        text = soup.get_text()        
        return text
        
    except Exception as e:
        return f"Error: {str(e)}"
    
@mcp.tool()
def fetch_weather(city: str) -> str:
    try:
        import os
        # Fetch the OpenWeatherMap API key from environment variables
        YOUR_API_KEY = os.getenv("OPENWEATHER_API_KEY")
        if not YOUR_API_KEY:
            # If the environment variable is not set, use a default API key
            # Note: Replace with your own OpenWeatherMap API key for production use
            YOUR_API_KEY= "c32bf88be3be047e2ef8b674c89b0957" #Replace with existing OpenWeatherMap API key

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={YOUR_API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code != 200:
            return f"Error: Unable to fetch weather data for {city}. Status code: {response.status_code}"
        text = response.json()
        if 'main' in text:
            temp = text['main']['temp']
            description = text['weather'][0]['description']
            text = f"The current temperature in {city} is {temp}°C with {description}."
        else:
            text = "Weather data not available for the specified city."
        return text
        
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()