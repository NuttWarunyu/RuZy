document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('winProbabilityChart').getContext('2d');
    const winProbabilityChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: window.teams || [], // ทีมที่รับจาก Python
            datasets: [{
                label: 'Win Probability (%)',
                data: window.winProbabilities || [], // ข้อมูลโอกาสชนะ
                backgroundColor: [
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)'
                ],
                borderColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
