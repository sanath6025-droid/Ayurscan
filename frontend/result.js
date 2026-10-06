(() => {
  const params = new URLSearchParams(window.location.search);
  const identifiedParam = params.get('identified');
  const plantNameParam = params.get('name');

  const identifiedView = document.querySelector('#identifiedView');
  const notIdentifiedView = document.querySelector('#notIdentifiedView');
  const scanPhoto = document.querySelector('#scanPhoto');

  const summaryTitleText = document.querySelector('#summaryTitleText');
  const summarySubtitleText = document.querySelector('#summarySubtitleText');
  const chipIdentifiedCount = document.querySelector('#chipIdentifiedCount');
  const chipUnclearCount = document.querySelector('#chipUnclearCount');

  const identifiedPlantsList = document.querySelector('#identifiedPlantsList');
  const unclearPlantsContainer = document.querySelector('#unclearPlantsContainer');

  // Modal elements
  const modalOverlay = document.querySelector('#plantModalOverlay');
  const modalCloseBtn = document.querySelector('#modalCloseBtn');
  const modalCloseBtnBottom = document.querySelector('#modalCloseBtnBottom');
  const modalPlantFamily = document.querySelector('#modalPlantFamily');
  const modalPlantTitle = document.querySelector('#modalPlantTitle');
  const modalPlantLatin = document.querySelector('#modalPlantLatin');
  const modalPlantDesc = document.querySelector('#modalPlantDesc');
  const modalPlantUses = document.querySelector('#modalPlantUses');
  const modalPlantParts = document.querySelector('#modalPlantParts');
  const modalPlantPrecautions = document.querySelector('#modalPlantPrecautions');
  const modalPlantWarnings = document.querySelector('#modalPlantWarnings');
  const modalPlantImg = document.querySelector('#modalPlantImg');
  const modalMediaWrap = document.querySelector('#modalMediaWrap');
  const modalVideoLink = document.querySelector('#modalVideoLink');

  // Load preview photo
  try {
    const savedPhoto = sessionStorage.getItem('ayurscanScanImage');
    if (savedPhoto && scanPhoto) {
      scanPhoto.src = savedPhoto;
      scanPhoto.hidden = false;
    }
  } catch (_) {}

  // Check URL override for "not identified" testing
  if (identifiedParam === '0') {
    showNotIdentifiedView("Visual evidence was insufficient or no plants were detected.");
    return;
  }

  // Check if plant name was passed directly via URL query (e.g. from Search or Field Notes)
  if (plantNameParam) {
    loadSinglePlantByScientificName(plantNameParam);
    return;
  }

  // Load Scan Results from sessionStorage
  let scanResults = null;
  try {
    const rawResults = sessionStorage.getItem('ayurscanScanResults');
    if (rawResults) {
      scanResults = JSON.parse(rawResults);
    }
  } catch (e) {
    console.warn("Could not read scan results from sessionStorage:", e);
  }

  if (scanResults && scanResults.plants && scanResults.plants.length > 0) {
    renderScanResults(scanResults);
  } else {
    // Default fallback demo if opened without a scan
    renderDefaultDemo();
  }

  function renderScanResults(data) {
    const identifiedList = data.plants.filter(p => p.status === 'identified');
    const unclearList = data.plants.filter(p => p.status === 'unclear');

    const idCount = identifiedList.length;
    const unCount = unclearList.length;

    if (idCount === 0 && unCount > 0) {
      showNotIdentifiedView(
        unclearList[0].reason || "All detected plants were unclear or obscured. Please capture a clearer photo."
      );
      return;
    }

    if (idCount === 0 && unCount === 0) {
      showNotIdentifiedView("No plants could be recognized in this photo.");
      return;
    }

    // Update Summary Banner (Section 7, 18)
    if (idCount === 1 && unCount === 0) {
      summaryTitleText.textContent = "We identified 1 plant successfully.";
      summarySubtitleText.textContent = "Review traditional Ayurvedic properties and botanical field notes below.";
    } else if (idCount > 1 && unCount === 0) {
      summaryTitleText.textContent = `We identified ${idCount} plants successfully.`;
      summarySubtitleText.textContent = "All distinguishable plants have been identified and matched with the Ayurvedic catalog.";
    } else if (idCount > 0 && unCount > 0) {
      summaryTitleText.textContent = `We identified ${idCount} ${idCount === 1 ? 'plant' : 'plants'} successfully.`;
      summarySubtitleText.textContent = `${unCount} additional ${unCount === 1 ? 'plant' : 'plants'} could not be identified clearly.`;
    }

    chipIdentifiedCount.textContent = `${idCount} IDENTIFIED`;
    if (unCount > 0) {
      chipUnclearCount.textContent = `${unCount} UNCLEAR`;
      chipUnclearCount.hidden = false;
    } else {
      chipUnclearCount.hidden = true;
    }

    // Render Identified Cards
    identifiedPlantsList.innerHTML = '';
    identifiedList.forEach((plant, idx) => {
      const card = createIdentifiedPlantCard(plant, idx + 1, idCount);
      identifiedPlantsList.appendChild(card);
    });

    // Render Unclear Cards (Section 18)
    if (unCount > 0) {
      unclearPlantsContainer.hidden = false;
      unclearPlantsContainer.innerHTML = `
        <div style="margin-bottom: 12px; margin-top: 24px;">
          <p class="eyebrow" style="color: var(--coral);">ADDITIONAL DETECTIONS</p>
          <h2 style="font: 500 22px var(--serif); margin: 4px 0 0;">Plants Needing a Closer Look</h2>
        </div>
      `;
      unclearList.forEach((unclearPlant) => {
        const card = createUnclearPlantCard(unclearPlant);
        unclearPlantsContainer.appendChild(card);
      });
    } else {
      unclearPlantsContainer.hidden = true;
    }

    identifiedView.hidden = false;
    notIdentifiedView.hidden = true;
  }

  function createIdentifiedPlantCard(plant, index, total) {
    const card = document.createElement('article');
    card.className = 'plant-card-item';

    const ayur = plant.ayurvedic_info || {};
    const common = plant.common_name || 'Ayurvedic Plant';
    const scientific = plant.scientific_name || '';
    const ayurName = ayur.ayurvedic_name ? `(${ayur.ayurvedic_name})` : '';
    const confidencePct = Math.round((plant.confidence || 0) * 100);

    const usesList = (ayur.traditional_uses && ayur.traditional_uses.length > 0)
      ? ayur.traditional_uses
      : (ayur.ayurvedic_uses || []);

    const usesHtml = usesList.slice(0, 3).map(u => `<li>${escapeHtml(u)}</li>`).join('') ||
      '<li>Traditionally revered for seasonal balance and well-being.</li>';

    const partsChips = (ayur.plant_parts_used || ['Leaves', 'Whole aerial parts'])
      .map(p => `<span class="part-chip">${escapeHtml(p)}</span>`).join('');

    const precautionText = (ayur.precautions && ayur.precautions.length > 0)
      ? ayur.precautions[0]
      : 'Plant identification from a photo is never enough to confirm safety. Consult an expert before internal use.';

    const locationBadge = plant.approximate_location
      ? `<span class="badge-location">📍 ${escapeHtml(plant.approximate_location)}</span>`
      : '';

    const familyText = ayur.family ? `· ${escapeHtml(ayur.family)}` : '';

    card.innerHTML = `
      <div class="plant-card-header">
        <div class="plant-title-group">
          <p class="eyebrow" style="color: var(--green); font-size: 9px; margin-bottom: 2px;">
            PLANT NOTE ${String(index).padStart(2, '0')} / ${String(total).padStart(2, '0')}
          </p>
          <h3>${escapeHtml(common)} <em>${escapeHtml(ayurName)}</em></h3>
          <p class="plant-scientific-name">${escapeHtml(scientific)} ${familyText}</p>
        </div>
        <div class="plant-card-badges">
          <span class="badge-confidence">${confidencePct}% CONFIDENCE</span>
          ${ayur.ayurvedic_name ? `<span class="badge-ayurvedic-name">${escapeHtml(ayur.ayurvedic_name)}</span>` : ''}
          ${locationBadge}
        </div>
      </div>

      <div class="plant-card-body">
        <div>
          <h4 class="section-subtitle">TRADITIONAL BOTANICAL OVERVIEW</h4>
          <p class="plant-desc-text">${escapeHtml(ayur.description || 'Traditional Ayurvedic plant respected in herbal heritage.')}</p>

          <h4 class="section-subtitle">NOTED TRADITIONAL USES</h4>
          <ul class="plant-uses-list">
            ${usesHtml}
          </ul>
        </div>

        <div>
          <h4 class="section-subtitle">PARTS TRADITIONALLY USED</h4>
          <div class="parts-used-chips">
            ${partsChips}
          </div>

          <div class="plant-precaution-box">
            <h4>TAKE CARE · PRECAUTIONS</h4>
            <p>${escapeHtml(precautionText)}</p>
          </div>
        </div>
      </div>

      <div class="plant-card-footer">
        <button class="button button-dark open-monograph-btn" type="button">
          View complete monograph <span aria-hidden="true">↗</span>
        </button>
        ${ayur.video_url ? `
          <a class="text-link" href="${escapeHtml(ayur.video_url)}" target="_blank" rel="noopener noreferrer">
            Watch educational guide <span aria-hidden="true">↗</span>
          </a>
        ` : ''}
      </div>
    `;

    // Hook up modal trigger
    const openBtn = card.querySelector('.open-monograph-btn');
    if (openBtn) {
      openBtn.addEventListener('click', () => openPlantModal(plant));
    }

    return card;
  }

  function createUnclearPlantCard(unclearPlant) {
    const card = document.createElement('article');
    card.className = 'unclear-warning-card';

    const confidencePct = Math.round((unclearPlant.confidence || 0) * 100);
    const reasonText = unclearPlant.reason ||
      "Plant is partially hidden, blurry, or lacking visible distinguishing characteristics.";
    const locationText = unclearPlant.approximate_location
      ? `Location in image: ${escapeHtml(unclearPlant.approximate_location)} · `
      : '';

    card.innerHTML = `
      <div class="unclear-card-top">
        <div class="unclear-header">
          <span class="unclear-icon" aria-hidden="true">⚠️</span>
          <h3>Plant Not Identified Clearly</h3>
        </div>
        <span class="unclear-confidence-tag">${confidencePct}% (below 70% threshold)</span>
      </div>
      <p class="unclear-message">This plant is not clearly visible.</p>
      <p class="unclear-advice">Please upload a clearer image or capture this plant separately in bright daylight.</p>
      <div class="unclear-reason-note">
        <strong>Vision Diagnostic:</strong> ${locationText}${escapeHtml(reasonText)}
      </div>
    `;

    return card;
  }

  function showNotIdentifiedView(customReason) {
    identifiedView.hidden = true;
    notIdentifiedView.hidden = false;
    const copy = document.querySelector('#notIdentifiedCopy');
    if (copy && customReason) {
      copy.textContent = customReason;
    }
  }

  // Open Full Monograph Modal
  function openPlantModal(plant) {
    const ayur = plant.ayurvedic_info || {};
    const common = plant.common_name || plant.scientific_name || 'Ayurvedic Plant';
    const scientific = plant.scientific_name || '';
    const sanskrit = ayur.ayurvedic_name ? ` · Sanskrit: ${ayur.ayurvedic_name}` : '';

    modalPlantFamily.textContent = ayur.family ? `${ayur.family.toUpperCase()} FAMILY · BOTANICAL MONOGRAPH` : 'BOTANICAL MONOGRAPH';
    modalPlantTitle.textContent = common;
    modalPlantLatin.textContent = `${scientific}${sanskrit}`;
    modalPlantDesc.textContent = ayur.description || 'Traditional Ayurvedic plant records.';

    // Populate Uses
    modalPlantUses.innerHTML = '';
    const allUses = [
      ...(ayur.traditional_uses || []),
      ...(ayur.ayurvedic_uses || [])
    ];
    if (allUses.length > 0) {
      allUses.forEach(u => {
        const li = document.createElement('li');
        li.textContent = u;
        modalPlantUses.appendChild(li);
      });
    } else {
      modalPlantUses.innerHTML = '<li>Historical Ayurvedic references document general vitality and balance.</li>';
    }

    // Populate Parts
    modalPlantParts.innerHTML = '';
    (ayur.plant_parts_used || ['Whole aerial parts']).forEach(p => {
      const span = document.createElement('span');
      span.className = 'part-chip';
      span.textContent = p;
      modalPlantParts.appendChild(span);
    });

    // Populate Precautions
    modalPlantPrecautions.innerHTML = '';
    (ayur.precautions || ['Consult a physician before medicinal use.']).forEach(p => {
      const li = document.createElement('li');
      li.textContent = p;
      modalPlantPrecautions.appendChild(li);
    });

    // Populate Warnings
    modalPlantWarnings.innerHTML = '';
    (ayur.warnings || ['Not a substitute for certified medical care.']).forEach(w => {
      const li = document.createElement('li');
      li.textContent = w;
      modalPlantWarnings.appendChild(li);
    });

    // Image
    if (ayur.image_url) {
      modalPlantImg.src = ayur.image_url;
      modalMediaWrap.hidden = false;
    } else {
      modalMediaWrap.hidden = true;
    }

    // Video
    const videoUrl = ayur.video_url || `https://www.youtube.com/results?search_query=${encodeURIComponent(scientific || common)}+plant`;
    modalVideoLink.href = videoUrl;

    // Show modal
    modalOverlay.classList.add('is-open');
    modalOverlay.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closePlantModal() {
    modalOverlay.classList.remove('is-open');
    modalOverlay.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  if (modalCloseBtn) modalCloseBtn.addEventListener('click', closePlantModal);
  if (modalCloseBtnBottom) modalCloseBtnBottom.addEventListener('click', closePlantModal);
  if (modalOverlay) {
    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) closePlantModal();
    });
  }
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modalOverlay.classList.contains('is-open')) {
      closePlantModal();
    }
  });

  // Fetch single plant directly from backend (for query links)
  async function loadSinglePlantByScientificName(scientificName) {
    try {
      const API_BASE = typeof window.getAyurScanApiBase === 'function'
        ? window.getAyurScanApiBase()
        : '';
      const res = await fetch(`${API_BASE}/api/plants/${encodeURIComponent(scientificName)}`);
      if (!res.ok) throw new Error("Plant not found");
      const record = await res.json();

      const mockDetection = {
        common_name: record.common_name,
        scientific_name: record.scientific_name,
        confidence: 0.96,
        status: "identified",
        approximate_location: "Catalog Entry",
        ayurvedic_info: record
      };

      renderScanResults({
        total_detected: 1,
        identified_count: 1,
        unclear_count: 0,
        plants: [mockDetection]
      });
    } catch (e) {
      showNotIdentifiedView(`Botanical record for '${scientificName}' could not be loaded.`);
    }
  }

  // Default demo when opened without prior scan
  function renderDefaultDemo() {
    renderScanResults({
      total_detected: 2,
      identified_count: 1,
      unclear_count: 1,
      plants: [
        {
          common_name: "Tulsi (Holy Basil)",
          scientific_name: "Ocimum tenuiflorum",
          confidence: 0.94,
          status: "identified",
          approximate_location: "Foreground center",
          ayurvedic_info: {
            ayurvedic_name: "Tulasi",
            family: "Lamiaceae",
            description: "An aromatic perennial shrub revered in traditional Indian medicine and household gardens. Noted for its distinct spicy-clove scent and purplish flowers.",
            traditional_uses: [
              "Brewed as herbal tea or tisane for everyday refreshment",
              "Kept in courtyards for natural air purification and cultural significance",
              "Fresh leaves crushed in poultices for minor external soothing"
            ],
            ayurvedic_uses: [
              "Traditionally used to balance Kapha and Vata doshas",
              "Considered an adaptogen (Rasayana) to support daily vitality and mental clarity"
            ],
            plant_parts_used: ["Leaves", "Seeds", "Whole aerial parts"],
            precautions: [
              "May possess mild blood-thinning properties; use moderation prior to surgery",
              "Consult a clinician during pregnancy or while breastfeeding"
            ],
            warnings: [
              "Do not consume concentrated essential oils undiluted",
              "Not an alternative to medical attention for acute respiratory distress"
            ],
            image_url: "https://images.unsplash.com/photo-1618164436241-4473940d1f5c?auto=format&fit=crop&w=800&q=80",
            video_url: "https://www.youtube.com/results?search_query=holy+basil+tulsi+ayurvedic+plant"
          }
        },
        {
          common_name: null,
          scientific_name: null,
          confidence: 0.35,
          status: "unclear",
          approximate_location: "Background right",
          reason: "Plant is partially hidden, out of focus, and lacking visible floral structures."
        }
      ]
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
})();
