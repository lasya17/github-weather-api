import os
import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()

GITHUB_API_URL = "https://api.github.com/users/{username}"
OPENWEATHER_GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"
OPENWEATHER_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


@app.get("/get_github_user")
def get_github_user(username: str):
    url = GITHUB_API_URL.format(username=username)
    resp = requests.get(url, timeout=10)

    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail="GitHub user not found")
    if resp.status_code == 403:
        raise HTTPException(status_code=403, detail="GitHub API rate limit exceeded")
    if resp.status_code != 200:
        raise HTTPException(status_code=500, detail="GitHub API error")

    data = resp.json()
    return {
        "login": data.get("login"),
        "name": data.get("name"),
        "public_repos": data.get("public_repos"),
        "followers": data.get("followers"),
        "following": data.get("following"),
    }


@app.get("/get_weather/{city}")
def get_weather(city: str):
    if not OPENWEATHER_API_KEY:
        raise HTTPException(status_code=500, detail="OpenWeather API key not set")

    # Step 1: get coordinates
    geo_params = {"q": city, "appid": OPENWEATHER_API_KEY}
    geo_resp = requests.get(OPENWEATHER_GEO_URL, params=geo_params, timeout=10)
    if geo_resp.status_code != 200:
        raise HTTPException(status_code=500, detail="OpenWeather geo API error")

    geo_data = geo_resp.json()
    if not geo_data:
        raise HTTPException(status_code=404, detail="City not found")

    lat, lon = geo_data[0]["lat"], geo_data[0]["lon"]

    # Step 2: get weather
    weather_params = {"lat": lat, "lon": lon, "appid": OPENWEATHER_API_KEY, "units": "metric"}
    weather_resp = requests.get(OPENWEATHER_WEATHER_URL, params=weather_params, timeout=10)
    if weather_resp.status_code != 200:
        raise HTTPException(status_code=500, detail="OpenWeather weather API error")

    weather_data = weather_resp.json()

    return {
        "city": city,
        "temperature": weather_data["main"]["temp"],
        "weather": weather_data["weather"][0]["description"],
    }
