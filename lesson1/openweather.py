import os

import requests
from dotenv import load_dotenv


def get_weather(city_name):
    path = os.path.join(os.getcwd(), '.env')
    load_dotenv(path)

    key = "OPENWEATHER_API_KEY"
    api_key = os.getenv(key, None)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}\
    &appid={api_key}"
    response = requests.get(url)
    response.json()
    return response


city = input("Enter city name: ")

response_weather = get_weather(city)
weather_dict = response_weather.json()

if weather_dict['cod'] == "404":
    print(weather_dict['message'])
else:
    # weather_dict = json.loads(response_weather.text)
    print(weather_dict["weather"][0]["main"])
    temp = round(float(weather_dict["main"]["temp"]) - 273, 1)
    print(f"Temperature: {temp}° С")
