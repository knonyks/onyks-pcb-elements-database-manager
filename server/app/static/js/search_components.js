// // =============================
// // Filtr kategorii
// // =============================
// window.filterByCategory = (category) => {
//   const rows = document.querySelectorAll(".table tbody tr");
//   rows.forEach((row) => {
//     const cell = row.children[1]; // kolumna „Kategoria”
//     const cat = cell ? cell.textContent : "";
//     row.style.display = (category === "all" || cat === category) ? "" : "none";
//   });
// };

// // =============================
// // Wyszukiwarka
// // =============================
// function filterTable() {
//   const input = document.querySelector(".search-input");
//   if (!input) return;
//   const filter = input.value.toLowerCase();

//   const rows = document.querySelectorAll(".table tbody tr");
//   rows.forEach((row) => {
//     const text = row.innerText.toLowerCase();
//     row.style.display = text.includes(filter) ? "" : "none";
//   });
// }

// const searchInput = document.querySelector(".search-input");
// if (searchInput) {
//   searchInput.addEventListener("keyup", (e) => {
//     if (e.key === "Enter") filterTable();
//   });
// }

// // =============================
// // Tooltipy dla opisów
// // =============================
// document.querySelectorAll('.description-tooltip img').forEach((icon) => {
//   const tooltip = document.createElement('span');
//   tooltip.className = 'tooltip-text';
//   tooltip.textContent = icon.parentElement.dataset.fullDescription || '';
//   tooltip.style.position = 'fixed';
//   tooltip.style.display = 'none';
//   document.body.appendChild(tooltip);

//   icon.addEventListener('mouseenter', () => {
//     const rect = icon.getBoundingClientRect();
//     tooltip.style.left = rect.right + 5 + 'px';
//     tooltip.style.top = rect.top + 'px';
//     tooltip.style.display = 'block';
//   });
//   icon.addEventListener('mouseleave', () => {
//     tooltip.style.display = 'none';
//   });
// });

// // =============================
// // Sprawdzanie przepełnienia opisów
// // =============================
// function checkDescriptions() {
//   document.querySelectorAll('.description').forEach((description) => {
//     const tooltipWrap = description.parentElement.querySelector('.description-tooltip');
//     if (!tooltipWrap) return;
//     tooltipWrap.style.display =
//       description.scrollWidth > description.clientWidth ? 'flex' : 'none';
//   });
// }

// checkDescriptions();
// window.addEventListener('resize', checkDescriptions);
function generateRandomEntry() {
  function randomString(length) {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let str = '';
    for (let i = 0; i < length; i++) {
      str += chars[Math.floor(Math.random() * chars.length)];
    }
    return str;
  }

  function randomLength(min = 5, max = 15) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
      const r = (Math.random() * 16) | 0;
      const v = c === 'x' ? r : (r & 0x3) | 0x8;
      return v.toString(16);
    });
  }

  function randomFrom(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }

  // realistic-ish sample pools
  const categories = ['Resistor', 'Capacitor', 'IC', 'Connector', 'Diode', 'Transistor', 'Sensor', 'Inductor'];
  const values = ['10k', '1k', '100nF', '10uF', 'SOT-23', '0603', '5V', '3.3V'];
  const availabilityStates = ['In stock', 'Out of stock', 'Preorder', 'Limited'];

  const uuid = uuidv4();
  const partName = randomString(randomLength(5, 14));
  const manufacturer = randomString(randomLength(5, 14));
  const manufacturerPartName = randomString(randomLength(4, 16));
  const category = randomFrom(categories);
  const datasheet = `https://example.com/datasheets/${uuid}.pdf`;
  const descriptionFull = randomString(randomLength(20, 120));
  // shorten visible description a bit
  const descriptionShort = descriptionFull.length > 60 ? descriptionFull.slice(0, 57) + '...' : descriptionFull;
  const value = randomFrom(values);
  const availability = randomFrom(availabilityStates);
  const libraryRef = randomString(randomLength(6, 18));
  const libraryPath = `/libs/${randomString(randomLength(4, 12))}/${randomString(randomLength(4, 12))}`;
  const footprintRef1 = randomString(randomLength(4, 12));
  const footprintPath1 = `/footprints/${randomString(randomLength(4, 12))}`;
  const footprintRef2 = randomString(randomLength(4, 12));
  const footprintPath2 = `/footprints/${randomString(randomLength(4, 12))}`;
  const footprintRef3 = randomString(randomLength(4, 12));
  const footprintPath3 = `/footprints/${randomString(randomLength(4, 12))}`;
  const createdAt = new Date(Date.now() - Math.floor(Math.random() * 31536000000)).toISOString(); // within last year

  const html = `
    <div class="data-table-row">
      <div class="data-table-checkbox-cell"><input type="checkbox"></div>
      <div>${uuid}</div>
      <div>${partName}</div>
      <div>${manufacturer}</div>
      <div>${manufacturerPartName}</div>
      <div>${category}</div>
      <div><a href="${datasheet}" target="_blank" rel="noopener">datasheet</a></div>
      <div class="description" title="${descriptionFull}">${descriptionShort}</div>
      <div>${value}</div>
      <div>${availability}</div>
      <div>${libraryRef}</div>
      <div>${libraryPath}</div>
      <div>${footprintRef1}</div>
      <div>${footprintPath1}</div>
      <div>${footprintRef2}</div>
      <div>${footprintPath2}</div>
      <div>${footprintRef3}</div>
      <div>${footprintPath3}</div>
      <div>${createdAt}</div>
    </div>
    `;
  return html;
}

let elements_table = new Data_Table("#elements-table");
elements_table.init();

for (let i = 0; i < 50; i++) {
  const newEntryHTML = generateRandomEntry();
  elements_table.ui.querySelector('.data-table-content').insertAdjacentHTML('beforeend', newEntryHTML);
}