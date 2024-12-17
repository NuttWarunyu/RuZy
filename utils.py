# utils.py
def check_handicap_success(score_home, score_away, handicap):
    """
    Check if the team passed the handicap.
    """
    try:
        handicap = float(handicap)
        goal_diff = score_home - score_away

        if handicap < 0:  # ทีมเจ้าบ้านต่อ
            return "green" if goal_diff > abs(handicap) else "red"
        elif handicap > 0:  # ทีมเยือนต่อ
            return "green" if goal_diff < -abs(handicap) else "red"
        else:  # Handicap เสมอ
            return "green" if goal_diff == 0 else "red"
    except Exception as e:
        print(f"Error checking handicap: {e}")
        return "red"


def process_handicap_performance(match_history):
    """
    Process the last 5 matches to determine handicap performance.
    """
    performance = []
    try:
        for match in match_history:
            score_home = match.get('home_score')
            score_away = match.get('away_score')
            handicap = match.get('handicap')

            result = check_handicap_success(score_home, score_away, handicap)
            performance.append(result)

        success_count = performance.count("green")
        return performance, success_count
    except Exception as e:
        print(f"Error processing handicap performance: {e}")
        return [], 0
