  // =============================
  // Filtr kategorii
  // =============================
  window.filterByCategory = (category) => {
    const rows = document.querySelectorAll(".table tbody tr");
    rows.forEach((row) => {
      const cell = row.children[1]; // kolumna „Kategoria”
      const cat = cell ? cell.textContent : "";
      row.style.display = (category === "all" || cat === category) ? "" : "none";
    });
  };

  // =============================
  // Wyszukiwarka
  // =============================
  function filterTable() {
    const input = document.querySelector(".search-input");
    if (!input) return;
    const filter = input.value.toLowerCase();

    const rows = document.querySelectorAll(".table tbody tr");
    rows.forEach((row) => {
      const text = row.innerText.toLowerCase();
      row.style.display = text.includes(filter) ? "" : "none";
    });
  }

  const searchInput = document.querySelector(".search-input");
  if (searchInput) {
    searchInput.addEventListener("keyup", (e) => {
      if (e.key === "Enter") filterTable();
    });
  }

  // =============================
  // Tooltipy dla opisów
  // =============================
  document.querySelectorAll('.description-tooltip img').forEach((icon) => {
    const tooltip = document.createElement('span');
    tooltip.className = 'tooltip-text';
    tooltip.textContent = icon.parentElement.dataset.fullDescription || '';
    tooltip.style.position = 'fixed';
    tooltip.style.display = 'none';
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

  // =============================
  // Sprawdzanie przepełnienia opisów
  // =============================
  function checkDescriptions() {
    document.querySelectorAll('.description').forEach((description) => {
      const tooltipWrap = description.parentElement.querySelector('.description-tooltip');
      if (!tooltipWrap) return;
      tooltipWrap.style.display =
        description.scrollWidth > description.clientWidth ? 'flex' : 'none';
    });
  }

  checkDescriptions();
  window.addEventListener('resize', checkDescriptions);