
(async () => {
  const data = await (await fetch("../output/travel_data_complete.json")).json();
  // 🔽 Références aux conteneurs DOM
  const accommodationsEl = document.getElementById("accommodations");
  const activitiesEl = document.getElementById("activities");
  const foodsEl = document.getElementById("foods");
  const currencyEl = document.getElementById("currency");
  const tipsEl = document.getElementById("tips");
  const citiesEl = document.getElementById("cities");

  // 🔄 Villes
  const allCities = data.macro_planning.ordered_cities.map(c => c.name);
  const citiesWithAccommodations = data.accommodations.map(acc => acc.from_city);
  let currentCity = allCities[0];


  function getDefaultImageFor(type) {
    const defaults = {
      acc: "https://static.wixstatic.com/media/940aa7_b3084a33a847435ab89048d06254b8fd~mv2.jpg/v1/fill/w_736,h_920,al_c,q_85,enc_auto/940aa7_b3084a33a847435ab89048d06254b8fd~mv2.jpg",
      act: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTXus_37nXqC7ibgpYURzvLsFA4HEs_Cy1AMg&s",
      food: "https://cdn.shopify.com/s/files/1/0588/6207/6066/files/street-food-chiang-mai-viandes.1497124.w740_480x480.jpg?v=1685608826",
    };
    return defaults[type] || "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTXus_37nXqC7ibgpYURzvLsFA4HEs_Cy1AMg&s";
  }

  // 📸 Récupère l'image OG de façon asynchrone
  async function fetchOGImage(url) {
    try {
      const res = await fetch(url);
      const html = await res.text();
      const doc = new DOMParser().parseFromString(html, "text/html");
      const meta = doc.querySelector('meta[property="og:image"]');
      return meta?.content || null;
    } catch {
      return null;
    }
  }

  // 🧱 Rendu d'une carte
  function renderCard(item, index, container, type) {
    const cardId = `${type}-${index}`;
    const placeholder = `<div class="image-placeholder h-40 bg-gray-100 rounded mb-2"></div>`;

    const html = `
      <div id="${cardId}" class="bg-white p-4 rounded-xl shadow relative overflow-hidden">
        ${placeholder}
        <h3 class="text-lg font-semibold">${item.name}</h3>
        <p>${item.description}</p>
        <p class="text-sm mt-2">Prix : ${item.euro_currency_price_min || item.euro_currency_price}€${item.euro_currency_price_max ? ` - ${item.euro_currency_price_max}€` : ''}</p>
        <a href="${item.link}" target="_blank" class="text-blue-600 underline">Voir plus</a>
      </div>`;

    container.innerHTML += html;

    // Ajout image async
    if (item.link) {
      fetchOGImage(item.link).then(url => {
        const img = document.createElement("img");
        img.src = url || getDefaultImageFor(type);
        img.alt = item.name;
        img.className = "w-full h-40 object-cover rounded mb-2";
        const placeholderEl = document.getElementById(cardId).querySelector(".image-placeholder");
        if (placeholderEl) placeholderEl.replaceWith(img);
      });
    }
  }

  // 🔄 Affiche les sections filtrées par ville
  function renderSection(container, items, filterFn, type) {
    container.innerHTML = "";
    const filtered = items.filter(filterFn);
    if (filtered.length === 0) {
      container.innerHTML = `<p class='text-gray-500'>Aucun élément trouvé pour cette ville.</p>`;
      return;
    }
    filtered.forEach((item, index) => renderCard(item, index, container, type));
  }

  // 🔁 Mise à jour de la sélection ville
  function updateCitySelectionUI(selectedCity) {
    document.querySelectorAll(".city-card").forEach(card => {
      const isActive = card.dataset.city === selectedCity;
      card.classList.toggle("ring-2", isActive);
      card.classList.toggle("ring-blue-500", isActive);
      card.classList.toggle("bg-blue-50", isActive);
    });
  }

  // 🔄 Rendu principal de la ville sélectionnée
  function renderCityContent(city) {
    currentCity = city;

    // Boutons (anciens city-button si encore utilisés)
    document.querySelectorAll(".city-button").forEach(btn => {
      const isActive = btn.dataset.city === city;
      btn.classList.toggle("bg-blue-600", isActive);
      btn.classList.toggle("text-white", isActive);
      btn.classList.toggle("bg-gray-200", !isActive);
    });

    document.querySelectorAll(".open-map-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const type = btn.dataset.type;
        showCategoryMap(type);
      });
    });

    renderSection(accommodationsEl, data.accommodations, acc => acc.from_city === city, "acc");
    renderSection(activitiesEl, data.activities, act => act.from_city === city, "act");
    renderSection(foodsEl, data.foods, food => food.from_city.includes(city), "food");
    updateMap(currentCity)
  }

  // 🏙️ Affichage interactif des tuiles de ville
  data.macro_planning.ordered_cities.forEach((city, index) => {
    const hasAccommodation = data.accommodations.some(acc => acc.from_city === city.name);
    const card = document.createElement("div");

    card.className = `city-card bg-white p-4 rounded-xl shadow cursor-pointer hover:bg-blue-50 transition ${
      hasAccommodation ? "" : "opacity-50 cursor-not-allowed"
    }`;

    card.dataset.city = city.name;
    card.innerHTML = `
      <h3 class="text-xl font-bold">${city.name}</h3>
      <p>${city.best_transport_to_come}</p>
      <p class="text-sm text-gray-500">Étape ${index + 1} / ${allCities.length}</p>
    `;

    if (hasAccommodation) {
      card.addEventListener("click", () => {
        renderCityContent(city.name);
        updateCitySelectionUI(city.name);
      });
    }

    citiesEl.appendChild(card);
  });

  const transportsEl = document.getElementById("transports");
  transportsEl.innerHTML = data.macro_planning.transports.map(t => `
  <div class="bg-white p-4 rounded shadow mb-2">
    <h4 class="font-semibold">${t.from_city} → ${t.to_city} (${t.type})</h4>
    <p>Prix : ${t.euro_price_min}€ - ${t.euro_price_max}€</p>
    <p>Durée moyenne : ${t.average_duration_in_hours}h</p>
  </div>
`).join("");

  // 📌 Conseils de voyage
  tipsEl.innerHTML = data.macro_planning.travel_considerations.map(tip => `<li>${tip}</li>`).join("");

  // 🔽 Remplissage de l'en-tête
  const headerEl = document.querySelector("header");

  // Extraire les informations depuis les données
  const travelerCount = data.traveler_count;
  const originalCountry = data.original_country;
  const destinationCountry = data.destination_country;
  const year = data.date;
  const localCurrency = data.macro_planning.local_currency;
  const exchangeRate = data.macro_planning.current_exchange_rate;

  // Remplir les éléments du header
  headerEl.innerHTML = `
    <h1 class="text-4xl font-bold mb-2">🌏 Voyage ${originalCountry} → ${destinationCountry} (${year})</h1>
    <p class="text-lg">${travelerCount} voyageurs | Monnaie locale : <span id="currency">${localCurrency}</span></p>
    <p class="text-sm text-gray-500">Taux de change actuel : 1 EUR = ${exchangeRate} ${localCurrency}</p>
  `;

  // 🔽 Fonction pour gérer l'affichage ou la dissimulation de la section "Douane"
  const toggleCustomsButton = document.getElementById("toggleCustoms");
  const customsContent = document.getElementById("customs-content");

  toggleCustomsButton.addEventListener("click", () => {
    const isHidden = customsContent.classList.contains("hidden");

    // Si la section est cachée, on l'affiche, sinon on la cache
    if (isHidden) {
      customsContent.classList.remove("hidden");
      toggleCustomsButton.textContent = "▲"; // Change le symbole pour indiquer que l'on peut replier
    } else {
      customsContent.classList.add("hidden");
      toggleCustomsButton.textContent = "▼"; // Change le symbole pour indiquer que l'on peut déplier
    }
  });

  // 🔽 Affichage de la section Douane avec un layout côte à côte
  const customsEl = document.getElementById("customs-content");

  // Extraire les informations sur les douanes
  const borders = data.borders;

  // Fonction pour afficher les informations sur la douane
  function renderCustomsInfo() {
    customsEl.innerHTML = ""; // On vide le contenu de la section

    borders.forEach(border => {
      customsEl.innerHTML += `
        <div class="bg-white p-4 rounded-xl shadow mb-4">
          <h3 class="text-xl font-semibold">${border.name}</h3>
          <div class="grid grid-cols-2 gap-4 mt-2">
            <p><strong>Passeport valide : </strong>${border.passport_validity ? "Oui" : "Non"}</p>
            <p><strong>Exigences de visa : </strong>${border.visa_requirements ? "Oui" : "Non"}</p>
            <p><strong>Note sur le visa : </strong>${border.visa_note}</p>
            <p><strong>Régulations douanières : </strong>${border.customs_regulations}</p>
            <p><strong>Note supplémentaire : </strong>${border.extra_note}</p>
          </div>
        </div>
      `;
    });
  }

  // Affichage initial des informations de douane
  renderCustomsInfo();




  async function getCoordinates(query) {
    const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query)}&format=json&addressdetails=1&limit=1`;

    try {
      const response = await fetch(url);
      const data = await response.json();
      if (data.length > 0) {
        const lat = parseFloat(data[0].lat);
        const lon = parseFloat(data[0].lon);
        return { lat, lon };
      } else {
        console.error("Coordonnées non trouvées pour :", query);
        return null;
      }
    } catch (error) {
      console.error("Erreur lors de la récupération des coordonnées :", error);
      return null;
    }
  }

  // Initialisation de la carte OpenStreetMap
  const map = L.map("openstreetmap").setView([48.8566, 2.3522], 13); // Coordonnées par défaut : Paris

  // Ajout de la couche OpenStreetMap
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);

  let marker;
  // Fonction pour mettre à jour la carte avec la ville actuelle
  async function updateMap(city) {
    // Récupérer les coordonnées via Nominatim
    const coordinates = await getCoordinates(city);

    if (coordinates) {
      const { lat, lon } = coordinates;

      // Centrer la carte sur la ville
      map.setView([lat, lon], 7);

      // Ajouter ou mettre à jour le marqueur
      if (marker) {
        marker.setLatLng([lat, lon]);
      } else {
        marker = L.marker([lat, lon]).addTo(map);
      }
    }
  }

  // Fonction principale pour initialiser la carte et tracer le trajet
  async function initMap() {
    const cityCoordinates = [];

    // Récupérer les coordonnées pour chaque ville de manière asynchrone
    for (let city of allCities) {
      const coordinates = await getCoordinates(city);
      if (coordinates) {
        cityCoordinates.push({ city, coordinates });
        // Ajouter un marqueur pour chaque ville
        L.marker([coordinates.lat, coordinates.lon]).addTo(map).bindPopup(`Ville: ${city}`);
      }
    }

    // 🚗 Tracer le trajet entre toutes les villes, après avoir récupéré toutes les coordonnées
    let previousCity = null;
    cityCoordinates.forEach(({ coordinates }) => {
      if (previousCity) {
        // Vérification que les coordonnées ne sont pas nulles ou incorrectes
        if (coordinates.lat && coordinates.lon && previousCity.lat && previousCity.lon) {
          // Tracer la courbe entre la ville précédente et la ville actuelle
          L.curve(["M", [previousCity.lat, previousCity.lon], "Q", [(previousCity.lat + coordinates.lat) / (2 + (Math.random() * 0.2 - 0.1)), (previousCity.lon + coordinates.lon) / (2 + (Math.random() * 0.2 - 0.1))], [coordinates.lat, coordinates.lon]],
            {
              color: '#1e90ff',
              weight: 4,
              opacity: 0.9,
              dashArray: '5, 10',
              lineJoin: 'round'
            }
          ).addTo(map);
        }
      }
      previousCity = coordinates; // Mettre à jour la ville précédente avec l'objet de coordonnées
    });

    // 🌍 Ajuster la carte pour qu'elle englobe toutes les villes
    if (cityCoordinates.length > 0) {
      const bounds = cityCoordinates.map(({ coordinates }) => [coordinates.lat, coordinates.lon]);
      map.fitBounds(bounds);  // Ajuste la vue de la carte pour inclure toutes les villes
    }
  }

  // 🚀 Init
  updateCitySelectionUI(currentCity);
  renderCityContent(currentCity);

  // 📍 Appel de la fonction pour initialiser la carte
  initMap();



  // 📍 Fonction d'affichage de la carte modale
  const mapModal = document.getElementById("mapModal");
  const categoryMapEl = document.getElementById("categoryMap");
  let categoryMap = null;
  let categoryLayerGroup = null;

  document.getElementById("closeMapModal").addEventListener("click", () => {
    mapModal.classList.add("hidden");
    if (categoryMap) {
      categoryMap.remove();
      categoryMap = null;
    }
  });

// 📌 Fonction pour ouvrir la carte avec les éléments d'une catégorie
  async function showCategoryMap(type) {
    const items = {
      acc: data.accommodations,
      act: data.activities,
      food: data.foods
    }[type].filter(item => item.from_city === currentCity);

    // Initialise la carte si besoin
    mapModal.classList.remove("hidden");

    // Nettoyer
    categoryMapEl.innerHTML = "";

    categoryMap = L.map("categoryMap").setView([20, 105], 6); // centrage temporaire
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: '&copy; OpenStreetMap contributors',
    }).addTo(categoryMap);

    categoryLayerGroup = L.layerGroup().addTo(categoryMap);

    const bounds = [];

    for (const item of items) {
      const locationQuery = item.address || item.from_city || currentCity;
      const coords = await getCoordinates(locationQuery);

      if (coords) {
        const marker = L.marker([coords.lat, coords.lon]).addTo(categoryLayerGroup)
          .bindPopup(`<strong>${item.name}</strong><br>${item.description || ''}${item.address ? `<br><em>${item.address}</em>` : ""}`);
        bounds.push([coords.lat, coords.lon]);
      }
    }

    if (bounds.length) {
      categoryMap.fitBounds(bounds);
    }
  }

})()