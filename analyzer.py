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

        # Handicap performance simulation (random for now)
        handicap_performance = ["Pass", "Pass", "Fail", "Pass", "Fail"]
        loss_performance = ["Fail", "Fail", "Pass", "Fail", "Pass"]

        # Generate analysis
        analysis = {
            "league": league_name or "Unknown League",
            "home_team": home_stats.get("team_name", "Unknown"),
            "away_team": away_stats.get("team_name", "Unknown"),
            "home_form": home_stats.get("form", "N/A"),
            "away_form": away_stats.get("form", "N/A"),
            "home_win_probability": round(home_win_probability, 2),
            "away_win_probability": round(away_win_probability, 2),
            "win_probability": f"Home: {round(home_win_probability, 2)}% / Away: {round(away_win_probability, 2)}%",
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
                home_form,
                away_form
            ),
            "current_standing": f"Home Rank: {home_rank}, Away Rank: {away_rank}",
            "handicap_performance": [
                "green" if result == "Pass" else "red" for result in handicap_performance
            ],
            "loss_performance": [
                "red" if result == "Fail" else "green" for result in loss_performance
            ]
        }

        return analysis

    except Exception as e:
        print(f"Error in analyze_match_outcomes: {e}")
        return {}


def calculate_top_form_teams(analysis_results, top_n=3):
    """
    Calculate top-performing teams based on win probabilities.
    """
    try:
        sorted_teams = sorted(
            analysis_results,
            key=lambda x: float(x.get("home_win_probability", 0)) + float(x.get("away_win_probability", 0)),
            reverse=True
        )
        return sorted_teams[:top_n]
    except Exception as e:
        print(f"Error calculating top form teams: {e}")
        return []


def calculate_top_handicap_teams(analysis_results, top_n=5):
    """
    Calculate the best handicap-performing teams.
    """
    try:
        for team in analysis_results:
            team["handicap_success_count"] = team.get("handicap_performance", []).count("green")

        sorted_teams = sorted(
            analysis_results,
            key=lambda x: x.get("handicap_success_count", 0),
            reverse=True
        )
        return sorted_teams[:top_n]
    except Exception as e:
        print(f"Error calculating top handicap teams: {e}")
        return []


def calculate_losing_teams(analysis_results, top_n=5):
    """
    Calculate teams with the worst betting performance.
    """
    try:
        for team in analysis_results:
            team["loss_count"] = team.get("loss_performance", []).count("red")

        sorted_teams = sorted(
            analysis_results,
            key=lambda x: x.get("loss_count", 0),
            reverse=True
        )
        return sorted_teams[:top_n]
    except Exception as e:
        print(f"Error calculating losing teams: {e}")
        return []


def generate_betting_recommendations(analysis_results):
    """
    Generate betting recommendations based on analyzed match results.
    """
    recommendations = []
    for result in analysis_results:
        try:
            home_team = result.get("home_team", "N/A")
            away_team = result.get("away_team", "N/A")
            home_prob = float(result.get("home_win_probability", 0))
            away_prob = float(result.get("away_win_probability", 0))
            handicap_analysis = result.get("handicap_analysis", "N/A")

            if home_prob > 60:
                recommendations.append({
                    "team": home_team,
                    "type": "Home Win",
                    "reason": f"{home_team} has a high win probability of {home_prob:.2f}%."
                })
            if away_prob > 60:
                recommendations.append({
                    "team": away_team,
                    "type": "Away Win",
                    "reason": f"{away_team} has a high win probability of {away_prob:.2f}%."
                })
            if "Bet on Home" in handicap_analysis:
                recommendations.append({
                    "team": home_team,
                    "type": "Handicap Bet",
                    "reason": "Handicap analysis favors the home team."
                })
            if "Bet on Away" in handicap_analysis:
                recommendations.append({
                    "team": away_team,
                    "type": "Handicap Bet",
                    "reason": "Handicap analysis favors the away team."
                })
        except Exception as e:
            print(f"Error generating recommendation for match {home_team} vs {away_team}: {e}")
    return recommendations


def analyze_handicap_outcome(home_probability, away_probability, handicap, odds):
    """
    Analyze the handicap and recommend which side to bet on.
    """
    try:
        if not handicap or odds is None:
            return {
                "handicap": handicap or "N/A",
                "odds": odds or "N/A",
                "recommendation": "Insufficient data for analysis"
            }
        handicap_value = float(handicap.split()[1]) if handicap.split() else 0

        if handicap_value < 0:
            recommendation = "Bet on Home" if home_probability > away_probability else "Avoid betting on Home"
        else:
            recommendation = "Bet on Away" if away_probability > home_probability else "Avoid betting on Away"

        return {
            "handicap": handicap,
            "odds": odds,
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

    if home_rank < away_rank:
        reason.append(f"The home team is ranked higher ({home_rank}) compared to the away team ({away_rank}).")
    else:
        reason.append(f"The away team is ranked higher ({away_rank}) compared to the home team ({home_rank}).")

    if home_form:
        reason.append(f"The home team's recent form is {home_form}.")
    if away_form:
        reason.append(f"The away team's recent form is {away_form}.")

    return " ".join(reason)
