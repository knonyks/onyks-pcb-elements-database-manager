console.log("sort.js ZAŁADOWANY!");

function filterByCategory(category) {
    let rows = document.querySelectorAll(".custom-table-row");

    rows.forEach(row => {
        let cat = row.children[1].innerText.trim();
        if (category === "all" || cat === category) {
            row.style.display = ""; // pokazujemy
        } else {
            row.style.display = "none"; // ukrywamy
        }
    });
}

document.getElementById('menuToggle').addEventListener('click', function() {
    document.getElementById('navLinks').classList.toggle('show');
});