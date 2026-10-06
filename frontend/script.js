(() => {
  // Mobile nav toggle
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      const isOpen = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(isOpen));
      toggle.setAttribute('aria-label', isOpen ? 'Close navigation' : 'Open navigation');
    });
  }

  // Interactive Plant Search (Section 20)
  const searchInput = document.querySelector('#catalogSearchInput');
  const clearBtn = document.querySelector('#searchClearBtn');
  const statusBar = document.querySelector('#searchStatusBar');
  const resultsGrid = document.querySelector('#searchResultsGrid');

  if (searchInput && resultsGrid) {
    const API_BASE = typeof window.getAyurScanApiBase === 'function'
      ? window.getAyurScanApiBase()
      : '';

    let debounceTimer = null;

    // Load initial featured plants
    loadFeaturedPlants();

    async function loadFeaturedPlants() {
      try {
        const res = await fetch(`${API_BASE}/api/plants?limit=6`);
        if (!res.ok) throw new Error("Could not load featured plants");
        const plants = await res.json();
        renderPlantCards(plants);
        if (statusBar) statusBar.textContent = `Showing ${plants.length} featured plants from catalog`;
      } catch (e) {
        if (statusBar) statusBar.textContent = "Connect backend to explore the live catalog.";
      }
    }

    searchInput.addEventListener('input', () => {
      const query = searchInput.value.trim();

      if (clearBtn) clearBtn.hidden = !query;

      clearTimeout(debounceTimer);
      if (!query) {
        loadFeaturedPlants();
        return;
      }

      if (statusBar) statusBar.textContent = `Searching for '${query}'...`;

      debounceTimer = setTimeout(async () => {
        try {
          const res = await fetch(`${API_BASE}/api/search?q=${encodeURIComponent(query)}`);
          if (!res.ok) throw new Error("Search request failed");
          const data = await res.json();
          renderPlantCards(data.results);
          if (statusBar) {
            statusBar.textContent = data.count > 0
              ? `Found ${data.count} matching ${data.count === 1 ? 'plant' : 'plants'} for '${query}'`
              : `No plants found matching '${query}'. Try another search.`;
          }
        } catch (err) {
          if (statusBar) statusBar.textContent = `Search error: ${err.message}`;
        }
      }, 250);
    });

    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        searchInput.value = '';
        clearBtn.hidden = true;
        searchInput.focus();
        loadFeaturedPlants();
      });
    }

    function renderPlantCards(plants) {
      resultsGrid.innerHTML = '';
      if (!plants || plants.length === 0) {
        resultsGrid.innerHTML = `
          <div style="grid-column: 1 / -1; padding: 24px; background: #e9ecdf; text-align: center; color: #5a6458; font-size: 13px;">
            No botanical entries found. Try searching by common name (e.g. Tulsi, Ginger, Mint) or Sanskrit name (e.g. Haridra, Nimba).
          </div>
        `;
        return;
      }

      plants.forEach(plant => {
        const card = document.createElement('a');
        card.className = 'search-result-card';
        card.href = `result.html?name=${encodeURIComponent(plant.scientific_name)}`;

        const sanskritBadge = plant.ayurvedic_name
          ? `<span class="search-ayur-badge">${escapeHtml(plant.ayurvedic_name)}</span>`
          : '';

        card.innerHTML = `
          <div>
            <div class="search-card-top">
              <div>
                <h3>${escapeHtml(plant.common_name)}</h3>
                <p class="latin">${escapeHtml(plant.scientific_name)}</p>
              </div>
              ${sanskritBadge}
            </div>
            <p class="search-card-desc">${escapeHtml(plant.description || 'Traditional Ayurvedic botanical entry.')}</p>
          </div>
          <span class="search-card-arrow">View details ↗</span>
        `;
        resultsGrid.appendChild(card);
      });
    }

    function escapeHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }
  }
})();
