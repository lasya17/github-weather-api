# GitHub User & City Weather API 🌦️

Two simple FastAPI endpoints:
1. `/get_github_user?username=<username>` → GitHub user profile
2. `/get_weather/<city>` → current weather for a city (via OpenWeather)

## 🚀 Setup
```bash
git clone https://github.com/<your-username>/github-weather-api.git
cd github-weather-api
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## 🔑 Add your OpenWeather API Key
```bash
export OPENWEATHER_API_KEY="your_api_key"
```

## ▶️ Run the server
```bash
uvicorn app:app --reload --port 3400
```

## 📌 Example Requests
- `GET http://localhost:3400/get_github_user?username=octocat`
- `GET http://localhost:3400/get_weather/London`

## 🛡 Error Handling
- 404: User or city not found
- 403: GitHub API rate limit exceeded
- 500: API errors
