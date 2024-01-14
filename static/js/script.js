var selectingCity = 0;
window.onload = function() {
    add_locations()
    renderMap()
showPath(start_loc,end_loc)

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
    var url = `/weather-analysis?weather_condition=${weather}&city=${start_location}&departure_location=${end_location}&start_date=${start_date}&end_date=${end_date}`
    console.log(url)
    location.href = url
}