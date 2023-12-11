from flask import Flask, request, json
from datetime import datetime

# Inițializarea aplicației Flask
app = Flask(__name__)

# Deschiderea și citirea fișierului JSON
with open('database/weather_data.json') as f:
    weather_data = json.load(f)


# Funcția pentru găsirea unei perioade însorite
def find_sunny_period(city, original_start, duration):
    city_weather = weather_data.get(city, [])
    best_period = None
    max_sunny_days = 0
    best_avg_temp = 0
    best_common_condition = ""

    for i in range(len(city_weather) - duration + 1):
        period = city_weather[i:i + duration]
        sunny_days = sum(1 for day in period if day['weather_condition'] == 'Clear')
        avg_temp = sum(day['temperature'] for day in period) / duration
        common_condition = max(set(day['weather_condition'] for day in period),
                               key=lambda cond: sum(day['weather_condition'] == cond for day in period))

        if sunny_days > max_sunny_days or (sunny_days == max_sunny_days and avg_temp > best_avg_temp):
            max_sunny_days = sunny_days
            best_period = (period[0]['date'], period[-1]['date'])
            best_avg_temp = avg_temp
            best_common_condition = common_condition

    if best_period and best_period[0] != original_start.strftime("%Y-%m-%d"):
        return {
            'start_date': best_period[0],
            'end_date': best_period[1],
            'average_temperature': round(best_avg_temp, 1),
            'most_common_condition': best_common_condition
        }
    else:
        return "Nu s-a găsit o perioadă alternativă mai însorită."


# Funcția de analiză a vremii
def analyze_weather(city, start_date, end_date):
    city_weather = weather_data.get(city, [])
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    duration = (end_date - start_date).days + 1

    total_temp = 0
    weather_conditions = {}
    count = 0

    for day in city_weather:
        day_date = datetime.strptime(day['date'], "%Y-%m-%d")
        if start_date <= day_date <= end_date:
            total_temp += day['temperature']
            weather_conditions[day['weather_condition']] = weather_conditions.get(day['weather_condition'], 0) + 1
            count += 1

    if count > 0:
        average_temp = round(total_temp / count, 1)
        most_common_condition = max(weather_conditions, key=weather_conditions.get)

        # Verifică dacă condiția predominantă nu este însorită și caută o perioadă alternativă
        if most_common_condition != "Clear":
            alternative_period = find_sunny_period(city, start_date, duration)
            return {
                'average_temperature': average_temp,
                'most_common_condition': most_common_condition,
                'alternative_period': alternative_period
            }
        else:
            return {
                'average_temperature': average_temp,
                'most_common_condition': most_common_condition
            }
    else:
        return None


# Rutele Flask
@app.route('/')
def home():
    return 'Bine ai venit la TripSyncRO!'


@app.route('/weather-analysis')
def get_weather_analysis():
    city = request.args.get('city')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not city or not start_date or not end_date:
        return "Te rog să specifici orașul și perioada (start_date, end_date)."

    weather_info = analyze_weather(city, start_date, end_date)
    if weather_info:
        return json.dumps(weather_info)
    else:
        return "Nu s-au găsit date pentru perioada specificată."


# Punctul de start pentru aplicație
if __name__ == '__main__':
    app.run(debug=True)
