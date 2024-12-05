import os
import requests
from tools.base_tool import Tool

class WeatherTool(Tool):
    def name(self):
        return "Weather Tool"

    def description(self):
        return "Provides weather information for a given location. The payload is just the location. Example: New York"

    def use(self, location:str):        
        api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            response = f"The weather in {location} is currently {description} with a temperature of {temp}°C."
            print(response)
            return response
        else:
            return f"Sorry, I couldn't find weather information for {location}."