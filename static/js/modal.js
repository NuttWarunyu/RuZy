// Script to handle table row clicks and show modal
document.addEventListener("DOMContentLoaded", function () {
    const rows = document.querySelectorAll(".clickable-row");
    const modal = document.getElementById("teamModal");
    const closeModal = document.querySelector(".close");
    
    const modalTeamName = document.getElementById("modal-team-name");
    const modalWinProbability = document.getElementById("modal-win-probability");
    const modalCurrentStanding = document.getElementById("modal-current-standing");

    // Handle row click
    rows.forEach(row => {
        row.addEventListener("click", function () {
            const team = row.dataset.team;
            const win = row.dataset.win;
            const standing = row.dataset.standing;

            // Populate modal with data
            modalTeamName.textContent = team;
            modalWinProbability.textContent = win;
            modalCurrentStanding.textContent = standing;

            // Show modal
            modal.style.display = "block";
        });
    });

    // Close modal
    closeModal.addEventListener("click", function () {
        modal.style.display = "none";
    });

    // Close modal on outside click
    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});
