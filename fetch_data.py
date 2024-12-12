import requests
from datetime import datetime, timedelta, timezone
from config import API_KEY

def fetch_fixtures(league_id, season, days_ahead=7):
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {"x-apisports-key": API_KEY}
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    end_date = (datetime.now(timezone.utc) + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
    params = {"league": league_id, "season": season, "from": today, "to": end_date}

    response = requests.get(url, headers=headers, params=params)
    return response.json().get("response", [])
