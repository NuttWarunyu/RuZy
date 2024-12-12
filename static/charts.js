document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('winProbabilityChart').getContext('2d');
    const winProbabilityChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: window.teams || [], // ชื่อคู่แข่งในรูปแบบ "Home vs Away"
            datasets: [
                {
                    label: 'Home Win Probability (%)',
                    data: window.homeWinProbabilities || [], // โอกาสชนะของทีมเหย้า
                    backgroundColor: 'rgba(75, 192, 192, 0.7)', // สีแท่งของทีมเหย้า
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Away Win Probability (%)',
                    data: window.awayWinProbabilities || [], // โอกาสชนะของทีมเยือน
                    backgroundColor: 'rgba(255, 99, 132, 0.7)', // สีแท่งของทีมเยือน
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        font: {
                            size: 14
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'โอกาสชนะของทีมเหย้าและทีมเยือน (%)', // ชื่อกราฟ
                    font: {
                        size: 16
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        font: {
                            size: 12
                        }
                    }
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function (value) {
                            return value + '%'; // เพิ่ม % ในแกน Y
                        }
                    }
                }
            }
        }
    });
});
