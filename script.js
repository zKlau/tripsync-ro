window.onload = function() {
    add_locations()
}

function add_locations() {
    var capitals = [
        "Alba Iulia", "Arad", "Bacau", "Baia Mare", "Bistrita", "Botosani",
        "Braila", "Brasov", "Bucharest", "Calarasi", "Cluj-Napoca", "Constanta",
        "Craiova", "Deva", "Drobeta-Turnu Severin", "Focsani", "Galati", "Giurgiu",
        "Hunedoara", "Iasi", "Miercurea Ciuc", "Oradea", "Piatra Neamt", "Pitesti",
        "Ploiesti", "Ramnicu Valcea", "Resita", "Satu Mare", "Sfantu Gheorghe",
        "Sibiu", "Slatina", "Slobozia", "Suceava", "Targoviste", "Targu Jiu",
        "Targu Mures", "Timisoara", "Tirgu Mures", "Vaslui", "Zalau"
    ]
    for (let i = 0; i < capitals.length; i++) {
        $("#locations").append(`<option value="${capitals[i]}">${capitals[i]}</option>`)
    }
}

function send_data() {
    var start_date = $("#start-date").val()
    var end_date = $("#end-date").val()
    var location = $("#locations").val()
    var weather = $("#weather").val()
    var url = `/weather=${weather}&location=${location}&start-date=${start_date}&end-date=${end_date}`
    console.log(url)
}