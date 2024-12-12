import requests
from datetime import datetime, timedelta, timezone

# Create a global session with connection pooling
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
session.mount("https://", adapter)
session.mount("http://", adapter)

def fetch_fixtures(api_key, league_id, season, days_ahead=14):
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {"x-apisports-key": api_key}
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    end_date = (datetime.now(timezone.utc) + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
    params = {"league": league_id, "season": season, "from": today, "to": end_date}

    print(f"Requesting fixtures for league {league_id} from {today} to {end_date}")

    try:
        response = session.get(url, headers=headers, params=params, timeout=(5, 10))
        response.raise_for_status()
        fixtures = response.json().get("response", [])

        if not fixtures:
            print(f"No fixtures found for league {league_id} in the next {days_ahead} days.")
            return []

        # Group fixtures by date
        fixtures_by_date = {}
        for match in fixtures:
            match_date = match.get("fixture", {}).get("date", "").split("T")[0]
            if match_date:
                fixtures_by_date.setdefault(match_date, []).append(match)

        if not fixtures_by_date:
            print("No fixtures available in the response.")
            return []

        # Find the closest date with fixtures
        closest_date = min(fixtures_by_date.keys(), key=lambda d: datetime.strptime(d, '%Y-%m-%d'))
        print(f"Closest match date: {closest_date} with {len(fixtures_by_date[closest_date])} matches.")
        return fixtures_by_date[closest_date]  # Return fixtures for the closest date
    except requests.exceptions.RequestException as e:
        print(f"Error fetching fixtures: {e}")
    return []

def fetch_standings(api_key, league_id, season):
    url = "https://v3.football.api-sports.io/standings"
    headers = {"x-apisports-key": api_key}
    params = {"league": league_id, "season": season}

    try:
        response = session.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json().get("response", [])
        if data and "league" in data[0] and "standings" in data[0]["league"]:
            return data[0]["league"]["standings"][0]  # Return team standings
    except requests.exceptions.RequestException as e:
        print(f"Error fetching standings: {e}")
    return []

def fetch_team_statistics(api_key, league_id, season, team_id):
    url = "https://v3.football.api-sports.io/teams/statistics"
    headers = {"x-apisports-key": api_key}
    params = {"league": league_id, "season": season, "team": team_id}

    try:
        response = session.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json().get("response", {})
        
        team_name = data.get("team", {}).get("name", "Unknown")
        form = data.get("form", "Unknown")
        return {"team_name": team_name, "form": form}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching team statistics for team {team_id}: {e}")
    return {"team_name": "Unknown", "form": "Unknown"}

def fetch_injuries(api_key, team_id):
    url = "https://v3.football.api-sports.io/injuries"
    headers = {"x-apisports-key": api_key}
    params = {"team": team_id}

    try:
        response = session.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get("response", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching injuries for team {team_id}: {e}")
    return []

def fetch_live_score(api_key, fixture_id):
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {"x-apisports-key": api_key}
    params = {"id": fixture_id}

    try:
        response = session.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json().get("response", [])
        if data:
            match = data[0]
            status = match.get("fixture", {}).get("status", {}).get("short", "Unknown")
            home_team = match.get("teams", {}).get("home", {}).get("name", "Unknown")
            away_team = match.get("teams", {}).get("away", {}).get("name", "Unknown")
            home_score = match.get("goals", {}).get("home", 0)
            away_score = match.get("goals", {}).get("away", 0)

            if status in ["LIVE", "1H", "HT", "2H", "ET", "P", "PEN"]:
                return f"Live: {home_team} {home_score}-{away_score} {away_team}"
            elif status == "FT":
                return f"Full-Time: {home_team} {home_score}-{away_score} {away_team}"
            elif status == "NS":
                return "Match has not started yet."
    except requests.exceptions.RequestException as e:
        print(f"Error fetching live score for fixture {fixture_id}: {e}")
    return "No live data available."

def fetch_head_to_head(api_key, home_team_id, away_team_id):
    url = "https://v3.football.api-sports.io/fixtures/headtohead"
    headers = {"x-apisports-key": api_key}
    params = {"h2h": f"{home_team_id}-{away_team_id}"}

    try:
        response = session.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get("response", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching head-to-head data: {e}")
    return []

def fetch_odds(api_key, fixture_id):
    url = "https://v3.football.api-sports.io/odds"
    headers = {"x-apisports-key": api_key}
    params = {"fixture": fixture_id}

    try:
        response = session.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json().get("response", [])
        if data:
            bookmakers = data[0].get("bookmakers", [])
            if bookmakers:
                bets = bookmakers[0].get("bets", [])
                for bet in bets:
                    if bet["name"] == "Asian Handicap":
                        odds_values = bet.get("values", [])
                        if odds_values:
                            odds = odds_values[0]
                            return {"handicap": odds.get("value", "N/A"), "odd": odds.get("odd", "N/A")}
    except Exception as e:
        print(f"Error fetching odds for fixture {fixture_id}: {e}")
    return {"handicap": "N/A", "odd": "N/A"}
