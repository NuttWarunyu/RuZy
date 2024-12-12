def fetch_odds_data(matches):
    """
    Fetch odds comparison data from multiple bookmakers.
    """
    odds_data = []
    for match in matches:
        odds_data.append({
            "bookmaker": "Bet365",
            "home_odds": 1.75,
            "away_odds": 2.10,
            "win_probability": "75% vs 25%"
        })
    return odds_data
