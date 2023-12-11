var map
var control
var cities
function renderMap() {
  map = L.map('map').setView([45.9432, 24.9668], 6); // Coordonatele din centru + zoom level

  var bounds = L.latLngBounds(
      L.latLng(42.0, 19.0), // Sud vest Romania
      L.latLng(49.5, 30.0)  // Nord est Romania
  );
   map.setMaxBounds(bounds);
   map.on('drag', function () {
       map.panInsideBounds(bounds, { animate: false });
   });

   L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
       attribution: '© TripSync RO'
   }).addTo(map);

   cities = [
       { name: "Alba Iulia", coordinates: [46.0711, 23.5806] },
       { name: "Arad", coordinates: [46.1833, 21.3167] },
       { name: "Bacau", coordinates: [46.5712, 26.9159] },
       { name: "Baia Mare", coordinates: [47.6531, 23.5795] },
       { name: "Bistrita", coordinates: [47.1299, 24.4989] },
       { name: "Botosani", coordinates: [47.7469, 26.6605] },
       { name: "Braila", coordinates: [45.2690, 27.9574] },
       { name: "Brasov", coordinates: [45.6579, 25.6012] },
       { name: "Bucharest", coordinates: [44.4268, 26.1025] },
       { name: "Calarasi", coordinates: [44.2067, 27.3259] },
       { name: "Cluj-Napoca", coordinates: [46.7712, 23.6236] },
       { name: "Constanta", coordinates: [44.1765, 28.6348] },
       { name: "Craiova", coordinates: [44.3302, 23.7949] },
       { name: "Deva", coordinates: [45.8791, 22.9018] },
       { name: "Drobeta-Turnu Severin", coordinates: [44.6262, 22.6570] },
       { name: "Focsani", coordinates: [45.6968, 27.1827] },
       { name: "Galati", coordinates: [45.4257, 28.0319] },
       { name: "Giurgiu", coordinates: [43.9037, 25.9699] },
       { name: "Hunedoara", coordinates: [45.7544, 22.9045] },
       { name: "Iasi", coordinates: [47.1585, 27.6014] },
       { name: "Miercurea Ciuc", coordinates: [46.3600, 25.8026] },
       { name: "Oradea", coordinates: [47.0458, 21.9183] },
       { name: "Piatra Neamt", coordinates: [46.9275, 26.3705] },
       { name: "Pitesti", coordinates: [44.8606, 24.8675] },
       { name: "Ploiesti", coordinates: [44.9469, 26.0364] },
       { name: "Ramnicu Valcea", coordinates: [45.0985, 24.3693] },
       { name: "Resita", coordinates: [45.2989, 21.8869] },
       { name: "Satu Mare", coordinates: [47.7917, 22.8858] },
       { name: "Sfantu Gheorghe", coordinates: [45.8644, 25.7839] },
       { name: "Sibiu", coordinates: [45.7975, 24.1515] },
       { name: "Slatina", coordinates: [44.4304, 24.3568] },
       { name: "Slobozia", coordinates: [44.5667, 27.3667] },
       { name: "Suceava", coordinates: [47.6344, 26.2576] },
       { name: "Targoviste", coordinates: [44.9386, 25.4598] },
       { name: "Targu Jiu", coordinates: [45.0455, 23.2742] },
       { name: "Targu Mures", coordinates: [46.5424, 24.5624] },
       { name: "Timisoara", coordinates: [45.9432, 21.2367] },
       { name: "Vaslui", coordinates: [46.6398, 27.7295] },
       { name: "Zalau", coordinates: [47.1758, 23.0551] }
   ];

   cities.forEach(function (city) {
    var marker = L.marker(city.coordinates, { icon: createCustomMarker(city.name) }).addTo(map);
    marker.bindPopup(city.name);
    });

    function createCustomMarker(cityName) {
        var customMarker = L.divIcon({
            className: 'custom-marker',
            html: cityName
        });
        return customMarker;
    }

    control = L.Routing.control({
        routeWhileDragging: true,
        show: false 
    }).addTo(map);

    var toggleButton = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom');
        toggleButton.innerHTML = '<button id="toggle-instructions" onclick="toggleInstructions()">Hide</button>';
        document.getElementById('map').appendChild(toggleButton);

    window.addEventListener('resize', function () {
        map.invalidateSize();
    });
}

function toggleInstructions() {
    var instructionsContainer = document.querySelector('.leaflet-routing-container .leaflet-routing-alt');
    instructionsContainer.style.display = (instructionsContainer.style.display === 'none' || instructionsContainer.style.display === '') ? 'block' : 'none';
}

function showPath(start,finish) {
    
    control.setWaypoints([
        L.latLng(start),
        L.latLng(finish)
    ]);

    control.route();
}