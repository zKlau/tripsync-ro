import json
import random
from datetime import datetime, timedelta

def generate_data():
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_generated = [start_date + timedelta(days=x) for x in range((end_date-start_date).days + 1)]

    capitals = [
        "Alba Iulia", "Arad", "Bacau", "Baia Mare", "Bistrita", "Botosani",
        "Braila", "Brasov", "Bucharest", "Calarasi", "Cluj-Napoca", "Constanta",
        "Craiova", "Deva", "Drobeta-Turnu Severin", "Focsani", "Galati", "Giurgiu",
        "Hunedoara", "Iasi", "Miercurea Ciuc", "Oradea", "Piatra Neamt", "Pitesti",
        "Ploiesti", "Ramnicu Valcea", "Resita", "Satu Mare", "Sfantu Gheorghe",
        "Sibiu", "Slatina", "Slobozia", "Suceava", "Targoviste", "Targu Jiu",
        "Targu Mures", "Timisoara", "Tirgu Mures", "Vaslui", "Zalau"
    ]

    # Probabilitatea ca un tip de vreme sa apara ( totalul == 100 )
    probabilities = {
        "Clear": 30,
        "Partly Cloudy": 30,
        "Cloudy": 30,
        "Light Rain": 5,
        "Snow": 5
    }

    data = {}
    for capital in capitals:
        
        data[capital] = [
            {
                "date": date.strftime("%Y-%m-%d"),
                "temperature": (temperature := random.randint(-5, 10)),
                "weather_condition": (
                    "Snow" if temperature <= 0 and random.randint(0,100) < probabilities['Snow'] else
                    random.choices(
                    [condition for condition in probabilities.keys() if condition != "Snow"],
                    weights=[probabilities[condition] for condition in probabilities.keys() if condition != "Snow"]
                )[0]
                )
            }
            for date in date_generated
            
        ]
    print([condition for condition in probabilities.keys() if condition != "Snow"])
    print([probabilities[condition] for condition in probabilities.keys() if condition != "Snow"])
    return data

weather_data = generate_data()

with open("./weather_data.json", "w") as json_file:
    json.dump(weather_data, json_file, indent=2)

