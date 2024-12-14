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

def calculate_value_bet(matches):
    """
    Calculate Value Bet for each match and return matches with positive value bets.
    """
    print("Matches Received:")
    print(matches)
    value_bets = []
    for match in matches:
        # Get probabilities and odds
        home_probability = float(match.get('home_win_probability', 0)) / 100
        away_probability = float(match.get('away_win_probability', 0)) / 100
        home_odds = float(match.get('home_odds', 0))
        away_odds = float(match.get('away_odds', 0))

        # Calculate Value Bet
        home_value = (home_probability * home_odds) - 1
        away_value = (away_probability * away_odds) - 1

        # Check for Value Bet
        if home_value > 0:
            value_bets.append({
                "team": match.get('home_team', 'N/A'),
                "value": home_value,
                "odds": home_odds,
                "reason": "ทีมเหย้ามีโอกาสชนะสูงและอัตราต่อรองคุ้มค่า"
            })
        if away_value > 0:
            value_bets.append({
                "team": match.get('away_team', 'N/A'),
                "value": away_value,
                "odds": away_odds,
                "reason": "ทีมเยือนมีโอกาสชนะสูงและอัตราต่อรองคุ้มค่า"
            })

    # Sort Value Bets by value descending
    print("Value Bets Calculated:")
    print(value_bets)
    return sorted(value_bets, key=lambda x: x['value'], reverse=True)
    

    # Template HTML
    template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Match Analysis</title>
    <link rel="stylesheet" href="static/styles.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        /* Additional Styling */
        .header {
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
        }
        nav {
            background-color: #333;
            color: white;
            display: flex;
            justify-content: center;
            padding: 10px 0;
            gap: 15px;
        }
        nav a {
            color: white;
            text-decoration: none;
            font-weight: bold;
        }
        nav a:hover {
            text-decoration: underline;
        }
        .section-title {
            color: #007bff;
            text-align: center;
            margin-top: 30px;
        }
        .top-picks {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        .top-picks .card {
            text-align: center;
        }
    </style>
</head>
<body>
    <header class="header">ทีเด็ดฟุตบอล.Ai - การวิเคราะห์การแข่งขันฟุตบอล</header>

    <!-- Navigation Bar -->
    <nav>
        <a href="#top-picks">Top Picks</a>
        <a href="#win-probability">Win Probability</a>
        <a href="#all-matches">All Matches</a>
    </nav>

    <!-- Top Pick Section -->
    {% if top_team.team_name %}
    <section id="top-picks" class="top-picks">
    <h2 class="section-title">โอกาสผ่านราคาสูงสุด</h2>
    <div style="display: flex; justify-content: center; margin-top: 20px;">
        <div class="card card-rank-1">
            <h3>{{ top_team.team_name }}</h3>
            <p><strong>League:</strong> {{ top_team.league }}</p>
            <p><strong>Win Probability:</strong> {{ top_team.probability }}</p>
            <p><strong>Odds Handicap:</strong> {{ top_team.odds }}</p>
            <p><strong>Analysis:</strong> <span style="color: red;">{{ top_team.handicap_analysis }}</span></p>
            <p><strong>Goals Scored:</strong> {{ top_team.goals_scored }}</p>
            <p><strong>Standing:</strong> {{ top_team.standing }}</p>
            <button style="background-color: #007bff; color: white; padding: 10px 15px; border-radius: 5px; border: none; cursor: pointer; margin-top: 10px;">ดูวิเคราะห์เพิ่มเติม</button>
        </div>
    </div>
</section>
    {% endif %}

    <!-- Win Probability Chart -->
    <section id="win-probability">
        <h2 class="section-title">โอกาสชนะ</h2>
        <div style="max-width: 800px; margin: auto;">
            <canvas id="winProbabilityChart" width="400" height="200"></canvas>
        </div>
    </section>

    <!-- Value Bet Section -->
    <section id="value-bets" style="padding: 20px; text-align: center;">
        <h2 class="section-title">ทีมที่น่าเดิมพัน (Value Bet)</h2>
        <div class="value-bet-list">
        {% for bet in value_bets %}
            <div class="card" style="background: #f8f9fa; padding: 15px; margin: 10px auto; max-width: 400px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-radius: 8px;">
                <h3>ทีม: {{ bet.team }}</h3>
                <p><strong>Value:</strong> {{ bet.value | round(2) }}</p>
                <p><strong>Odds:</strong> {{ bet.odds }}</p>
                <p><strong>เหตุผล:</strong> {{ bet.reason }}</p>
            </div>
            {% else %}
            <p>ไม่มีทีมที่มี Value Bet ในขณะนี้</p>
            {% endfor %}
        </div>
    </section>

    <!-- All Matches Section -->
    {% for league_name, matches in [("Premier League", results), ("La Liga", la_liga_results), ("Serie A", serie_a_results)] %}
    <section id="all-matches">
        <h2 class="section-title">{{ league_name }}</h2>
        <table>
            <thead>
                <tr>
                    <th>Match Date</th>
                    <th>Home Team</th>
                    <th>Away Team</th>
                    <th>Win Probability</th>
                    <th>Odds Handicap</th>
                    <th>Handicap Analysis</th>
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
                    <td><span style="color: red;">{{ match.get('handicap_analysis', 'N/A') }}</span></td>
                </tr>
                {% endfor %}
                <tr>
                    <td colspan="6" style="text-align: center; padding: 15px;">
                        <button style="background-color: #007bff; color: white; padding: 10px 15px; border-radius: 5px; border: none; cursor: pointer;">ดูวิเคราะห์เพิ่มเติม</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </section>
    {% endfor %}

    <script>
        window.matchLabels = {{ match_labels | tojson }};
        window.homeWinProbabilities = {{ home_win_probabilities | tojson }};
        window.awayWinProbabilities = {{ away_win_probabilities | tojson }};

        // Enhanced Chart Configuration
        const ctx = document.getElementById('winProbabilityChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: window.matchLabels,
                datasets: [
                    {
                        label: 'Home Win Probability (%)',
                        data: window.homeWinProbabilities,
                        backgroundColor: 'rgba(75, 192, 192, 0.7)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Away Win Probability (%)',
                        data: window.awayWinProbabilities,
                        backgroundColor: 'rgba(255, 99, 132, 0.7)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'top' },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.dataset.label}: ${context.raw}%`;
                            }
                        }
                    },
                    title: {
                        display: true,
                        text: 'โอกาสชนะ (%)'
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Matches'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Win Probability (%)'
                        }
                    }
                }
            }
        });
    </script>
    <script src="static/charts.js"></script>
    <footer style="background-color: #333; color: white; text-align: center; padding: 10px 0; margin-top: 20px;">
        © 2024 ทีเด็ดฟุตบอล.Ai | วิเคราะห์การแข่งขันฟุตบอลอย่างมืออาชีพ
    </footer>
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
            top_team=top_team,
            value_bets=value_bets  # ส่ง Value Bet ไปยัง Template
        )
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(html_content)
        print(f"HTML file generated with static files: {output_file}")
    except Exception as e:
        print(f"Error generating HTML with static files: {e}")