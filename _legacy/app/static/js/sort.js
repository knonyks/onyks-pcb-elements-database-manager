/* ============================================= */

/* Obsługa przycisków KATEGORI */

/* ============================================= */

function filterByCategory(category) {
    let rows = document.querySelectorAll(".table-row");

    rows.forEach(row => {
        let cat = row.children[1].innerText; //Kategoria jest w drugiej kolumnie dlatego children[1]
        if (category === "all" || cat === category) { // Jeśli kategoria jest "all" lub pasuje do kategorii w wierszu
            row.style.display = "";
        } else {
            row.style.display = "none"; 
        }
    });
}

/* ============================================= */

/* Obsługa przycisku MENU */

/* ============================================= */

document.getElementById('menuToggle').addEventListener('click', function() {
    document.getElementById('navLinks').classList.toggle('show');
});

/* ============================================= */

/* Obsługa przycisku DESCRIPTION */

/* ============================================= */

document.querySelectorAll('.description-tooltip img').forEach(icon => {
    const tooltip = document.createElement('span');
    tooltip.className = 'tooltip-text';
    tooltip.textContent = icon.parentElement.dataset.fullDescription;
    document.body.appendChild(tooltip);

    icon.addEventListener('mouseenter', () => {
        const rect = icon.getBoundingClientRect();
        tooltip.style.left = rect.right + 5 + 'px';
        tooltip.style.top = rect.top + 'px';
        tooltip.style.display = 'block';
    });
    icon.addEventListener('mouseleave', () => {
        tooltip.style.display = 'none';
    });
});

/* ============================================= */

/* Obsługa przepełnienia DESCRIPTION */

/* ============================================= */

function checkDescriptions() {
    document.querySelectorAll('.description').forEach(description => {
        const tooltip = description.parentElement.querySelector('.description-tooltip');
        if (description.scrollWidth > description.offsetWidth) {
            tooltip.style.display = 'flex';
        } else {
            tooltip.style.display = 'none';
        }
    });
}

// uruchom na starcie
window.addEventListener('load', checkDescriptions);

// uruchamiaj przy zmianie rozmiaru okna
window.addEventListener('resize', checkDescriptions);