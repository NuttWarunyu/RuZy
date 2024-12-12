from data_fetcher import fetch_live_score

class LiveScoreManager:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_live_scores(self, fixtures):
        """
        ดึงข้อมูล Live Score สำหรับการแข่งขันที่กำลังดำเนินอยู่
        """
        live_scores = []
        for fixture in fixtures:
            fixture_id = fixture.get("fixture", {}).get("id")
            if not fixture_id:
                continue

            live_score = fetch_live_score(self.api_key, fixture_id)
            live_scores.append({
                "fixture_id": fixture_id,
                "live_score": live_score,
                "home_team": fixture.get("teams", {}).get("home", {}).get("name", "N/A"),
                "away_team": fixture.get("teams", {}).get("away", {}).get("name", "N/A")
            })
        return live_scores
