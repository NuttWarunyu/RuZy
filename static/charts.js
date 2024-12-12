document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('winProbabilityChart').getContext('2d');
    const winProbabilityChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: window.matchLabels || [],
            datasets: [
                {
                    label: 'Home Win Probability (%)',
                    data: window.homeWinProbabilities || [],
                    backgroundColor: 'rgba(75, 192, 192, 0.7)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Away Win Probability (%)',
                    data: window.awayWinProbabilities || [],
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
                title: { display: true, text: 'โอกาสชนะ (%)' }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
});
