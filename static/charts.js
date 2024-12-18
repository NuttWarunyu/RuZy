document.addEventListener("DOMContentLoaded", function () {
    // รับข้อมูลจาก Jinja2 ผ่านการ Render เป็น JSON
    const teamsData = {{ top_form_teams | tojson | safe }};

    // แยกข้อมูลชื่อทีมและโอกาสชนะ
    const teamLabels = teamsData.map(team => team.selected_team);
    const winProbabilities = teamsData.map(team => team.win_probability);

    // สร้างกราฟ Chart.js
    const ctx = document.getElementById('topTeamsChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: teamLabels,
            datasets: [{
                label: 'โอกาสชนะ (%)',
                data: winProbabilities,
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'โอกาสชนะของทีมที่มีผลงานยอดเยี่ยม'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
