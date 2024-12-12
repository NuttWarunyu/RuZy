from flask import Flask, send_file
from data_fetcher import (
    fetch_fixtures,
    fetch_standings,
    fetch_odds,
)
from analyzer import analyze_match_outcomes
from html_generator import generate_html
from datetime import datetime
from tqdm import tqdm
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

API_KEY = "5ac618d291de54592f73b152ddb41315"
PREMIER_LEAGUE_ID = 39
LA_LIGA_ID = 140
SERIE_A_ID = 135
CURRENT_SEASON = 2024

app = Flask(__name__)

def analyze_fixtures(fixtures, standings, league_id, league_name):
    """
    Analyze fixtures and return detailed match analysis, including live status and odds.
    """
    analysis_results = []
    if not fixtures:
        logging.warning(f"No fixtures available for {league_name}.")
        return analysis_results

    fixtures.sort(key=lambda x: x.get("fixture", {}).get("date", ""))
    logging.info(f"Analyzing match outcomes for {league_name}...")

    for match in tqdm(fixtures, desc=f"Analyzing {league_name}"):
        try:
            home_team = match.get("teams", {}).get("home", {}).get("id")
            away_team = match.get("teams", {}).get("away", {}).get("id")
            match_date = match.get("fixture", {}).get("date")
            fixture_id = match.get("fixture", {}).get("id")

            if not (home_team and away_team and match_date and fixture_id):
                logging.warning(f"Invalid match data: {match}")
                continue

            # Fetch odds
            odds = fetch_odds(API_KEY, fixture_id) or {"handicap": "N/A", "odd": "N/A"}

            # Analyze match outcomes
            result = analyze_match_outcomes(
                API_KEY,
                league_id,
                CURRENT_SEASON,
                home_team,
                away_team,
                standings,
                odds=odds,
                league_name=league_name
            )
            result["match_date"] = datetime.strptime(match_date, '%Y-%m-%dT%H:%M:%S%z').astimezone().strftime('%d-%b %H:%M')
            result["home_team"] = match.get("teams", {}).get("home", {}).get("name", "N/A")
            result["away_team"] = match.get("teams", {}).get("away", {}).get("name", "N/A")
            result["handicap"] = odds.get("handicap", "N/A")
            result["odd"] = odds.get("odd", "N/A")
            analysis_results.append(result)

        except Exception as e:
            home_team_name = match.get("teams", {}).get("home", {}).get("name", "Unknown")
            away_team_name = match.get("teams", {}).get("away", {}).get("name", "Unknown")
            logging.error(f"Error analyzing match {home_team_name} vs {away_team_name}: {e}")

    return analysis_results

@app.route("/")
def index():
    """
    Main route to fetch data, analyze fixtures, and return the HTML report.
    """
    try:
        # Premier League
        logging.info("Fetching Premier League fixtures...")
        fixtures_premier_league = fetch_fixtures(API_KEY, PREMIER_LEAGUE_ID, CURRENT_SEASON)
        standings_premier_league = fetch_standings(API_KEY, PREMIER_LEAGUE_ID, CURRENT_SEASON)
        analysis_results_premier_league = analyze_fixtures(fixtures_premier_league, standings_premier_league, PREMIER_LEAGUE_ID, "Premier League")

        # La Liga
        logging.info("Fetching La Liga fixtures...")
        fixtures_la_liga = fetch_fixtures(API_KEY, LA_LIGA_ID, CURRENT_SEASON)
        standings_la_liga = fetch_standings(API_KEY, LA_LIGA_ID, CURRENT_SEASON)
        analysis_results_la_liga = analyze_fixtures(fixtures_la_liga, standings_la_liga, LA_LIGA_ID, "La Liga")

        # Serie A
        logging.info("Fetching Serie A fixtures...")
        fixtures_serie_a = fetch_fixtures(API_KEY, SERIE_A_ID, CURRENT_SEASON)
        standings_serie_a = fetch_standings(API_KEY, SERIE_A_ID, CURRENT_SEASON)
        analysis_results_serie_a = analyze_fixtures(fixtures_serie_a, standings_serie_a, SERIE_A_ID, "Serie A")

        # Generate HTML report
        generate_html(
            results=analysis_results_premier_league,
            la_liga_results=analysis_results_la_liga,
            serie_a_results=analysis_results_serie_a,
            output_file="analysis.html"
        )
        logging.info("Analysis report generated successfully.")
        return send_file("analysis.html")

    except Exception as e:
        logging.error(f"Error during analysis: {e}")
        return f"Error during analysis: {e}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
