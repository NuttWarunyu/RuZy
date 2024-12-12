from jinja2 import Template

def generate_html(results, la_liga_results, serie_a_results, live_matches=None, output_file="analysis.html"):
    """
    Generate an HTML report for match analysis, including live matches, top pick, and all league results.
    """
    live_matches = live_matches or []

    # Template HTML
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Match Analysis</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .card { 
                background: #fff; 
                border-radius: 8px; 
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
                padding: 20px; 
                max-width: 400px; 
                margin: 20px auto; 
                text-align: center; 
            }
            .card h1 { font-size: 24px; margin: 0; }
            .card .subtitle { color: gray; margin: 10px 0; }
            .highlight { color: green; font-weight: bold; }
            .odds { color: red; font-weight: bold; font-size: 18px; }
            table { width: 100%; border-collapse: collapse; margin: 20px 0; }
            th, td { padding: 10px; text-align: center; border: 1px solid #ddd; }
            th { background-color: #f4f4f4; }
            tr:nth-child(even) { background-color: #f9f9f9; }
            .live-status { color: red; font-weight: bold; font-size: 14px; }
        </style>
    </head>
    <body>
        {% if live_matches %}
        <h2>Live Matches</h2>
        <table>
            <thead>
                <tr>
                    <th>Match Time</th>
                    <th>Home Team</th>
                    <th>Away Team</th>
                    <th>Live Score</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {% for match in live_matches %}
                <tr>
                    <td>{{ match.get('match_time', 'N/A') }}</td>
                    <td>{{ match.get('home_team', 'N/A') }}</td>
                    <td>{{ match.get('away_team', 'N/A') }}</td>
                    <td>{{ match.get('live_score', 'N/A') }}</td>
                    <td class="live-status">{{ match.get('status', 'N/A') }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% endif %}

        {% if top_team.team_name %}
        <h1>Top Pick: {{ top_team.team_name }}</h1>
        <div class="card">
            <h1>{{ top_team.team_name }}</h1>
            <p class="subtitle">League: {{ top_team.league }}</p>
            <p class="odds">Odds Handicap: {{ top_team.odds }}</p>
            <p><span class="highlight">Win Probability:</span> {{ top_team.probability }}</p>
            <p><strong>Reason:</strong> {{ top_team.reason }}</p>
            <hr>
            <p><strong>Handicap Analysis:</strong> {{ top_team.handicap_analysis }}</p>
            <p><strong>Last 5 Matches:</strong> {{ top_team.last_5 }}</p>
            <p><strong>Goals Scored:</strong> {{ top_team.goals_scored }}</p>
            <p><strong>Goals Conceded:</strong> {{ top_team.goals_conceded }}</p>
            <p><strong>Current Standing:</strong> {{ top_team.standing }}</p>
        </div>
        {% else %}
        <h1>No Top Pick Available</h1>
        {% endif %}

        {% for league_name, matches in [("Premier League", results), ("La Liga", la_liga_results), ("Serie A", serie_a_results)] %}
        <h2>All Matches - {{ league_name }}</h2>
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
        {% endfor %}
    </body>
    </html>
    """

    # Select the top pick based on the highest win probability
    try:
        all_matches = results + la_liga_results + serie_a_results
        top_team_data = max(
            all_matches,
            key=lambda x: max(
                float(x.get('home_win_probability', 0)),
                float(x.get('away_win_probability', 0))
            )
        )
    except Exception:
        top_team_data = {}

    # เลือก Top Pick จากข้อมูลทั้งหมด
    try:
        all_matches = results + la_liga_results + serie_a_results
        top_team_data = max(
            all_matches,
            key=lambda x: max(
                float(x.get('home_win_probability', 0) or 0),
                float(x.get('away_win_probability', 0) or 0)
            )
        )
    except Exception as e:
        print(f"Error selecting top pick: {e}")
        top_team_data = {}

    # Extract details for the top team
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

    # Render and write to HTML file
    try:
        template = Template(template)
        html_content = template.render(
            top_team=top_team,
            live_matches=live_matches,
            results=results,
            la_liga_results=la_liga_results,
            serie_a_results=serie_a_results
        )
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(html_content)
        print(f"HTML file generated: {output_file}")
    except Exception as e:
        print(f"Error generating HTML: {e}")
