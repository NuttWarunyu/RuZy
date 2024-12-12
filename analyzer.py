import requests
from data_fetcher import fetch_team_statistics, fetch_head_to_head

def analyze_match_outcomes(api_key, league_id, season, home_team_id, away_team_id, standings, odds=None, league_name="Unknown League"):
    """
    Analyze match outcomes based on team statistics, head-to-head results, standings, and odds.
    """
    try:
        # Fetch team statistics
        home_stats = fetch_team_statistics(api_key, league_id, season, home_team_id) or {}
        away_stats = fetch_team_statistics(api_key, league_id, season, away_team_id) or {}
        head_to_head = fetch_head_to_head(api_key, home_team_id, away_team_id) or []

        # Extract standings ranks
        home_rank = next((int(team.get("rank", 999)) for team in standings if team.get("team", {}).get("id") == home_team_id), 999)
        away_rank = next((int(team.get("rank", 999)) for team in standings if team.get("team", {}).get("id") == away_team_id), 999)

        # Extract team forms
        home_form = home_stats.get("form", "") or ""
        away_form = away_stats.get("form", "") or ""

        # Analyze head-to-head results
        home_wins_h2h = len([
            match for match in head_to_head
            if match.get("teams", {}).get("home", {}).get("id") == home_team_id and
            (match.get("goals", {}).get("home") or 0) > (match.get("goals", {}).get("away") or 0)
        ])
        away_wins_h2h = len([
            match for match in head_to_head
            if match.get("teams", {}).get("away", {}).get("id") == away_team_id and
            (match.get("goals", {}).get("away") or 0) > (match.get("goals", {}).get("home") or 0)
        ])
        draws_h2h = len([
            match for match in head_to_head
            if (match.get("goals", {}).get("home") or 0) == (match.get("goals", {}).get("away") or 0)
        ])

        # Calculate win probabilities
        home_win_probability = (
            home_form.count("W") / len(home_form) * 100 if home_form and len(home_form) > 0 else 0
        )
        away_win_probability = (
            away_form.count("W") / len(away_form) * 100 if away_form and len(away_form) > 0 else 0
        )

        # Normalize probabilities
        total_probability = home_win_probability + away_win_probability
        if total_probability > 0:
            home_win_probability = home_win_probability / total_probability * 100
            away_win_probability = away_win_probability / total_probability * 100
        else:
            home_win_probability = 0
            away_win_probability = 0


        # Generate analysis
        analysis = {
            "league": league_name or "Unknown League",
            "home_team": home_stats.get("team_name", "Unknown"),
            "away_team": away_stats.get("team_name", "Unknown"),
            "home_form": home_stats.get("form", "N/A"),
            "away_form": away_stats.get("form", "N/A"),
            "home_win_probability": round(home_win_probability, 2) if home_win_probability else "N/A",
            "away_win_probability": round(away_win_probability, 2) if away_win_probability else "N/A",
            "win_probability": f"Home: {round(home_win_probability, 2)}% / Away: {round(away_win_probability, 2)}%"
                if home_win_probability and away_win_probability else "N/A",
            "handicap_analysis": analyze_handicap_outcome(
              home_win_probability,
                away_win_probability,
                odds.get("handicap", None) if odds else None,
                odds.get("odd", None) if odds else None,
            ).get("recommendation", "N/A") if odds else "N/A",
            "reason": generate_analysis_reason(
                home_win_probability,
                away_win_probability,
                home_rank,
                away_rank,
                home_stats.get("form", "N/A"),
                away_stats.get("form", "N/A")
            ),
            "current_standing": f"Home Rank: {home_rank}, Away Rank: {away_rank}" if home_rank and away_rank else "N/A",
            "last_5_matches": {
                "home": home_stats.get("last_5_matches", "N/A"),
                "away": away_stats.get("last_5_matches", "N/A")
            },
            "goals_scored": {
                "home": home_stats.get("goals_scored", "N/A"),
                "away": away_stats.get("goals_scored", "N/A")
            },
            "goals_conceded": {
                "home": home_stats.get("goals_conceded", "N/A"),
                "away": away_stats.get("goals_conceded", "N/A")
            }
        }

        return analysis  # Return the complete analysis

    except Exception as e:
        print(f"Error in analyze_match_outcomes: {e}")
        return {}



def analyze_handicap_outcome(home_probability, away_probability, handicap, odds):
    """
    Analyze the handicap and recommend which side to bet on based on probabilities and odds.
    """
    try:
        # ตรวจสอบว่ามีค่า handicap และ odds หรือไม่
        if not handicap or odds is None:
            return {
                "handicap": handicap or "N/A",
                "odds": odds or "N/A",
                "recommendation": "Insufficient data for analysis"
            }
        
        # Parse handicap value
        handicap_value = float(handicap.split()[1]) if handicap and handicap.split() else 0
        implied_probability = 100 / float(odds) if odds else 0

        # Determine which team has a higher chance of covering the handicap
        if handicap_value < 0:  # Handicap favors the home team
            if home_probability - abs(handicap_value * 10) > away_probability:
                recommendation = "Bet on Home"
            else:
                recommendation = "Avoid betting on Home"
        else:  # Handicap favors the away team
            if away_probability - handicap_value * 10 > home_probability:
                recommendation = "Bet on Away"
            else:
                recommendation = "Avoid betting on Away"

        return {
            "handicap": handicap,
            "odds": odds,
            "implied_probability": round(implied_probability, 2),
            "recommendation": recommendation
        }
    except Exception as e:
        print(f"Error analyzing handicap outcome: {e}")
        return {
            "handicap": handicap,
            "odds": odds,
            "recommendation": "Analysis failed"
        }

def generate_analysis_reason(home_prob, away_prob, home_rank, away_rank, home_form, away_form):
    """
    Generate a textual reason for the match analysis.
    """
    reason = []
    if home_prob > away_prob:
        reason.append(f"The home team is favored with a {home_prob:.2f}% win probability.")
    else:
        reason.append(f"The away team is favored with a {away_prob:.2f}% win probability.")

    if isinstance(home_rank, int) and isinstance(away_rank, int):
        if home_rank < away_rank:
            reason.append(f"The home team is ranked higher ({home_rank}) compared to the away team ({away_rank}).")
        else:
            reason.append(f"The away team is ranked higher ({away_rank}) compared to the home team ({home_rank}).")

    if home_form:
        reason.append(f"The home team's recent form is {home_form}.")
    if away_form:
        reason.append(f"The away team's recent form is {away_form}.")

    return " ".join(reason)
