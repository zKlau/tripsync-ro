var selectingCity = 0;
window.onload = function() {
    add_locations()
    renderMap()
    showPath(start_loc,end_loc)
    $("#start-location").val(end_loc);
    $("#end-location").val(start_loc);

    if (hotels_list != null) {
        hotels_list.forEach(function(hotel) {
            var hotelItem = `
                <div class="hotel-item">
                    <img src="${hotel[2]}" alt="Hotel Photo" width="100" height="100">
                    <div class="description">
                        <h3>${hotel[0]}</h3>
                        <p></p>
                    </div>
                    <div class="price">
                        €${hotel[1]} pe noapte
                    </div>
                </div>
            `;
            $('#hotels').append(hotelItem);
    });
}


    

      flatpickr('#datePicker', {
            mode: 'range',
            inline: true,
            defaultDate: [startDate, endDate],
            onChange: function (selectedDates, dateStr, instance) {
                console.log("Selected dates: " + dateStr);
            },
            disable: [
                function (date) {
                    return date < new Date(startDate);
                },
                function (date) {
                    return date > new Date(endDate);
                }
            ],
        });

}

function formatDate(inputDate) {
    const dateComponents = inputDate.split('/');
    const formattedDate = new Date(`${dateComponents[2]}-${dateComponents[0]}-${dateComponents[1]}`);
    const result = formattedDate.toISOString().split('T')[0];
    return result;
}
function setCity(type) {
    selectingCity = type
}

// cities[0]["coordinates"]
function add_locations() {
    var capitals = [
        "Alba Iulia", "Arad", "Bacau","Buzau", "Baia Mare", "Bistrita", "Botosani",
        "Braila", "Brasov", "Bucharest", "Calarasi", "Cluj-Napoca", "Constanta",
        "Craiova", "Deva", "Drobeta-Turnu Severin", "Focsani", "Galati", "Giurgiu",
        "Hunedoara", "Iasi", "Miercurea Ciuc", "Oradea", "Piatra Neamt", "Pitesti",
        "Ploiesti", "Ramnicu Valcea", "Resita", "Satu Mare", "Sfantu Gheorghe",
        "Sibiu", "Slatina", "Slobozia", "Suceava","Tulcea", "Targoviste", "Targu Jiu",
        "Timisoara", "Tirgu Mures", "Vaslui", "Zalau"
    ]
    for (let i = 0; i < capitals.length; i++) {
        $(".locations").append(`<option value="${capitals[i]}" data-id="${i}">${capitals[i]}</option>`)
    }
}

function send_data() {
    var date = $('#daterange').data('daterangepicker')
    var start_date = date.startDate.format('YYYY-MM-DD')
    var end_date = date.endDate.format('YYYY-MM-DD')
    var start_location = $("#start-location").val().replaceAll(" ","+")
    var end_location = $("#end-location").val().replaceAll(" ","+")
    var weather = $("#weather").val()
    var url = `/weather-analysis?weather_condition=${weather}&city=${end_location}&departure_location=${start_location}&start_date=${start_date}&end_date=${end_date}`
    location.href = url
}