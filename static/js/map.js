var map
var control
var cities
var distance
var time
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
       attribution: '© TripSync RO',
       minZoom: 6
   }).addTo(map);

   cities = [
    { name: "Alba Iulia", coordinates: [46.0775, 23.5804] },
    { name: "Arad", coordinates: [46.1866, 21.3126] },
    { name: "Bacau", coordinates: [46.5713, 26.9252] },
    { name: "Buzau", coordinates:  [45.1500, 26.8333]},
    { name: "Baia Mare", coordinates: [47.6531, 23.5795] },
    { name: "Bistrita", coordinates: [47.1357, 24.4997] },
    { name: "Botosani", coordinates: [47.7485, 26.6625] },
    { name: "Braila", coordinates: [45.2691, 27.9577] },
    { name: "Brasov", coordinates: [45.6579, 25.6012] },
    { name: "Bucharest", coordinates: [44.4268, 26.1025] },
    { name: "Calarasi", coordinates: [44.2027, 27.3255] },
    { name: "Cluj-Napoca", coordinates: [46.7712, 23.6236] },
    { name: "Constanta", coordinates: [44.1765, 28.6348] },
    { name: "Craiova", coordinates: [44.3302, 23.7949] },
    { name: "Deva", coordinates: [45.8671, 22.9047] },
    { name: "Drobeta-Turnu Severin", coordinates: [44.6316, 22.6562] },
    { name: "Focsani", coordinates: [45.6960, 27.1829] },
    { name: "Galati", coordinates: [45.4257, 28.0319] },
    { name: "Giurgiu", coordinates: [43.9036, 25.9699] },
    { name: "Hunedoara", coordinates: [45.7517, 22.8907] },
    { name: "Iasi", coordinates: [47.1585, 27.6014] },
    { name: "Miercurea Ciuc", coordinates: [46.3609, 25.8014] },
    { name: "Oradea", coordinates: [47.0465, 21.9189] },
    { name: "Piatra Neamt", coordinates: [46.9226, 26.3705] },
    { name: "Pitesti", coordinates: [44.8565, 24.8690] },
    { name: "Ploiesti", coordinates: [44.9462, 26.0368] },
    { name: "Ramnicu Valcea", coordinates: [45.0997, 24.3693] },
    { name: "Resita", coordinates: [45.2976, 21.8861] },
    { name: "Satu Mare", coordinates: [47.7938, 22.8859] },
    { name: "Sfantu Gheorghe", coordinates: [45.8664, 25.7939] },
    { name: "Sibiu", coordinates: [45.7983, 24.1256] },
    { name: "Slatina", coordinates: [44.4298, 24.3650] },
    { name: "Slobozia", coordinates: [44.5633, 27.3664] },
    { name: "Suceava", coordinates: [47.6376, 26.2597] },
    { name: "Targoviste", coordinates: [44.9385, 25.4598] },
    { name: "Targu Jiu", coordinates: [45.0428, 23.2745] },
    { name: "Timisoara", coordinates: [45.7489, 21.2087] },
    { name: "Tirgu Mures", coordinates: [46.5407, 24.5560] },
    { name: "Vaslui", coordinates: [46.6333, 27.7333] },
    { name: "Zalau", coordinates: [47.1797, 23.0554] },
    { name: "Tulcea", coordinates: [45.1760, 28.8044] }
   ];

   cities.forEach(function (city) {
    var marker = L.marker(city.coordinates, { icon: createCustomMarker(city.name) }).addTo(map);
    
    marker.bindPopup("<b>" + city.name + "</b>").on('click', function () {
        var index = cities.findIndex(function(cty) {
            return cty.name === city.name;
        });
        if(selectingCity == 0) {
            $("#start-location").val(city.name)
        } else {
            $("#end-location").val(city.name)
        }
        //alert("You clicked on " + city.name + " " + index + " " + selectingCity);
        // You can customize the interaction here, for example, open a modal or show additional information.
    });
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
    control.on('routesfound', function (event) {
        var route = event.routes[0];
        distance = route.summary.totalDistance / 1000; // Convert meters to kilometers
        time = route.summary.totalTime / 3600; // Convert seconds to hours

        $("#time").text("Timp pe drum : " + time.toFixed(2) + " ore")
        $("#distance").text("Distanta parcursa : " + distance.toFixed(2) + " km")
        //alert("Distance: " + distance.toFixed(2) + " km\nTime: " + time.toFixed(2) + " hours");
    });
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
        L.latLng(cities.filter(e => e.name == start)[0].coordinates),
        L.latLng(cities.filter(e => e.name == finish)[0].coordinates)
    ]);
    console.log(cities.filter(e => e.name == start)[0].coordinates[0])
    control.route();
}