from jinja2 import Template

def generate_html(results, la_liga_results, serie_a_results, live_matches=None, output_file="analysis.html"):
    """
    Generate an HTML report for match analysis, using external static files (CSS and JS).
    """
    live_matches = live_matches or []

    # คำนวณข้อมูลสำหรับกราฟ
    match_labels = [f"{match.get('home_team', 'N/A')} vs {match.get('away_team', 'N/A')}" for match in results[:5]]
    home_win_probabilities = [float(match.get("home_win_probability", 0)) for match in results[:5]]
    away_win_probabilities = [float(match.get("away_win_probability", 0)) for match in results[:5]]

    # คำนวณ Top Pick
    try:
        all_matches = results + la_liga_results + serie_a_results
        top_team_data = max(
            all_matches,
            key=lambda x: max(
                float(x.get('home_win_probability', 0)),
                float(x.get('away_win_probability', 0))
            )
        )
        top_team = {
            "team_name": top_team_data.get("home_team") if float(top_team_data.get("home_win_probability", 0)) > float(top_team_data.get("away_win_probability", 0)) else top_team_data.get("away_team"),
            "league": top_team_data.get("league", "Unknown League"),
            "probability": f"{max(float(top_team_data.get('home_win_probability', 0)), float(top_team_data.get('away_win_probability', 0))):.2f}%",
            "odds": top_team_data.get("handicap", "N/A"),
            "handicap_analysis": top_team_data.get("handicap_analysis", "N/A"),
            "reason": top_team_data.get("reason", "N/A"),
            "last_5": top_team_data.get("last_5", "N/A"),
            "goals_scored": top_team_data.get("goals_scored", "N/A"),
            "goals_conceded": top_team_data.get("goals_conceded", "N/A"),
            "standing": top_team_data.get("standing", "N/A")
        }
    except Exception as e:
        print(f"Error selecting top pick: {e}")
        top_team = {}

    # Template HTML
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Match Analysis</title>
        <link rel="stylesheet" href="static/style.css">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <h1>ฤาษี.Ai</h1>

        <!-- Top Pick -->
        {% if top_team.team_name %}
        <section class="top-picks">
            <h2>โอกาสผ่านราคาสูงสุด</h2>
            <div class="card">
                <h3>{{ top_team.team_name }}</h3>
                <p><strong>League:</strong> {{ top_team.league }}</p>
                <p><strong>Win Probability:</strong> {{ top_team.probability }}</p>
                <p><strong>Odds Handicap:</strong> {{ top_team.odds }}</p>
            </div>
        </section>
        {% endif %}

        <!-- Win Probability Chart -->
        <section>
            <h2>โอกาสชนะ</h2>
            <canvas id="winProbabilityChart" width="400" height="200"></canvas>
        </section>

        <!-- All Matches -->
        {% for league_name, matches in [("Premier League", results), ("La Liga", la_liga_results), ("Serie A", serie_a_results)] %}
        <section>
            <h2>{{ league_name }}</h2>
            <table>
                <thead>
                    <tr>
                        <th>Match Date</th>
                        <th>Home Team</th>
                        <th>Away Team</th>
                        <th>Win Probability</th>
                        <th>Odds Handicap</th>
                        <th>Handicap Analysis</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for match in matches %}
                    <tr>
                        <td>{{ match.get('match_date', 'N/A') }}</td>
                        <td>{{ match.get('home_team', 'N/A') }}</td>
                        <td>{{ match.get('away_team', 'N/A') }}</td>
                        <td>{{ match.get('win_probability', 'N/A') }}</td>
                        <td>{{ match.get('handicap', 'N/A') }}</td>
                        <td>{{ match.get('handicap_analysis', 'N/A') }}</td>
                        <td class="live-status">{% if match.get('live_status', '') == 'Live' %}Live{% else %}Upcoming{% endif %}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </section>
        {% endfor %}

        <script>
            window.teams = {{ match_labels | tojson }};
            window.homeWinProbabilities = {{ home_win_probabilities | tojson }};
            window.awayWinProbabilities = {{ away_win_probabilities | tojson }};
        </script>
        <script src="static/charts.js"></script>
    </body>
    </html>
    """

    # Render HTML
    try:
        template = Template(template)
        html_content = template.render(
            live_matches=live_matches,
            results=results,
            la_liga_results=la_liga_results,
            serie_a_results=serie_a_results,
            match_labels=match_labels,
            home_win_probabilities=home_win_probabilities,
            away_win_probabilities=away_win_probabilities,
            top_team=top_team
        )
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(html_content)
        print(f"HTML file generated with static files: {output_file}")
    except Exception as e:
        print(f"Error generating HTML with static files: {e}")
