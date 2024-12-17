# data_processor.py
from utils import process_handicap_performance

def process_handicap_teams(results, match_histories):
    """
    ประมวลผลทีมที่ผ่านราคาต่อรองจาก match_histories
    """
    top_handicap_teams = []
    for match, history in zip(results, match_histories):
        selected_team = match.get("home_team", "N/A")  # ตัวอย่างการเลือกทีม
        success_count = history["handicap_performance"].count("green")
        
        top_handicap_teams.append({
            "selected_team": selected_team,
            "league": match.get("league", "ไม่พบข้อมูล"),
            "handicap_success_count": success_count,
            "handicap_performance": history["handicap_performance"],
        })
    return top_handicap_teams
