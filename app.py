from flask import Flask, render_template
from fetch_data import fetch_fixtures
from config import LEAGUE_IDS, CURRENT_SEASON

app = Flask(__name__)

@app.route("/")
def index():
    league_data = {}
    for league_name, league_id in LEAGUE_IDS.items():
        fixtures = fetch_fixtures(league_id, CURRENT_SEASON)
        league_data[league_name] = fixtures

    return render_template("index.html", league_data=league_data)

if __name__ == "__main__":
    app.run(debug=True)
