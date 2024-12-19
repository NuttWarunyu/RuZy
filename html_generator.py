from jinja2 import Template
import os

def combine_league_results(results, la_liga_results, serie_a_results):
    """
    Combine results from multiple leagues into a single list.
    """
    combined_results = results + la_liga_results + serie_a_results
    print("Combined League Results:")
    for res in combined_results:
        print(res)
    return combined_results

import random

def generate_random_performance():
    """
    Generate a random performance history with 'green' and 'red' values.
    """
    return [random.choice(["green", "red"]) for _ in range(5)]

def process_handicap_teams(results):
    """
    Process and select teams based on handicap analysis.
    """
    top_handicap_teams = []
    for match in results:
        try:
            home_team = match.get("home_team", "ไม่พบข้อมูล")
            away_team = match.get("away_team", "ไม่พบข้อมูล")
            analysis = match.get("handicap_analysis", "")

            # สุ่มประวัติราคาต่อรอง
            handicap_performance = generate_random_performance()
            success_count = handicap_performance.count("green")

            # เลือกทีมตามคำแนะนำ
            if "Bet on Home" in analysis:
                selected_team = home_team
            elif "Bet on Away" in analysis:
                selected_team = away_team
            else:
                selected_team = home_team  # fallback ถ้าไม่มีคำแนะนำ

            # เพิ่มข้อมูลทีมที่ผ่านราคาต่อรอง
            top_handicap_teams.append({
                "selected_team": selected_team,
                "league": match.get("league", "ไม่พบข้อมูล"),
                "handicap_success_count": success_count,
                "handicap_performance": handicap_performance,
            })
        except Exception as e:
            print(f"Error processing match data: {e}")
            continue

    return top_handicap_teams





def process_top_form_teams(top_form_teams):
    """
    Select the best performing team based on win probabilities.
    """
    for team in top_form_teams:
        try:
            home_team = team.get("home_team", "ไม่พบข้อมูล")
            away_team = team.get("away_team", "ไม่พบข้อมูล")
            home_win = float(team.get("home_win_probability", 0))
            away_win = float(team.get("away_win_probability", 0))

            # ตัดสินใจเลือกทีมที่มีโอกาสชนะมากกว่า
            if home_win > away_win:
                team["selected_team"] = home_team
            else:
                team["selected_team"] = away_team
        except Exception as e:
            print(f"Error processing top form teams: {e}")
            team["selected_team"] = "ไม่พบข้อมูล"

    return top_form_teams

def generate_html(results, la_liga_results, serie_a_results, betting_recommendations=None,
                  live_matches=None, top_form_teams=None, top_handicap_teams=None, losing_teams=None,prediction_history=None,
                  output_file="analysis.html"):
    # Debug Fixtures
    print("Premier League Fixtures:", results)
    print("La Liga Fixtures:", la_liga_results)
    print("Serie A Fixtures:", serie_a_results)

    # รวมผลลัพธ์จากทุกลีก
    combined_results = combine_league_results(results, la_liga_results, serie_a_results)

    # Process top form teams
    if top_form_teams:
        top_form_teams = process_top_form_teams(top_form_teams)

    # Process top handicap teams
    if top_handicap_teams:
        top_handicap_teams = process_handicap_teams(combined_results)

    # คำนวณ Top Pick
    try:
        top_team_data = max(
            combined_results,
            key=lambda x: max(
                float(x.get('home_win_probability', 0)),
                float(x.get('away_win_probability', 0))
            )
        )
        top_team = {
            "team_name": top_team_data.get("home_team")
            if float(top_team_data.get("home_win_probability", 0))
            > float(top_team_data.get("away_win_probability", 0))
            else top_team_data.get("away_team"),
            "league": top_team_data.get("league", "ไม่พบข้อมูล"),
            "probability": f"{max(float(top_team_data.get('home_win_probability', 0)), float(top_team_data.get('away_win_probability', 0))):.2f}%",
            "odds": top_team_data.get("handicap", "N/A"),
            "reason": top_team_data.get("reason", "N/A"),
        }
    except Exception as e:
        print(f"Error selecting top pick: {e}")
        top_team = {}

    # Load the HTML template
    try:
        TEMPLATE_PATH = os.path.join("templates", "template.html")
        if not os.path.exists(TEMPLATE_PATH):
            raise FileNotFoundError(f"Template file not found at path: {TEMPLATE_PATH}")

        with open(TEMPLATE_PATH, "r", encoding="utf-8") as template_file:
            template = Template(template_file.read())

        # Render HTML with context
        html_content = template.render(
            fixtures_premier_league=results,
            fixtures_la_liga=la_liga_results,
            fixtures_serie_a=serie_a_results,
            top_team=top_team,
            top_form_teams=top_form_teams,
            top_handicap_teams=top_handicap_teams,
            prediction_history=prediction_history 
        )

        # Write the output to a file
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as output:
            output.write(html_content)
        print(f"HTML file generated successfully: {output_file}")

    except Exception as e:
        print(f"Error generating HTML: {e}")
