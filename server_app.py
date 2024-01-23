from flask import Flask, request, json, render_template
from datetime import datetime
import hotels as hotels_data
app = Flask(__name__)

with open('database/weather_data.json') as f:
    weather_data = json.load(f)


def find_preferred_weather_period(city, duration, desired_condition):
    city_weather = weather_data.get(city, [])
    best_period = None
    max_days_with_desired_condition = 0
    best_avg_temp = 0

    for i in range(len(city_weather) - duration + 1):
        period = city_weather[i:i + duration]
        days_with_desired_condition = sum(1 for day in period if day['weather_condition'] == desired_condition)
        avg_temp = sum(day['temperature'] for day in period) / duration

        if days_with_desired_condition > max_days_with_desired_condition or (
                days_with_desired_condition == max_days_with_desired_condition and avg_temp > best_avg_temp):
            max_days_with_desired_condition = days_with_desired_condition
            best_period = (period[0]['date'], period[-1]['date'])
            best_avg_temp = avg_temp

    if best_period:
        return {
            'start_date': best_period[0],
            'end_date': best_period[1],
            'average_temperature': round(best_avg_temp, 1),
            'desired_condition': desired_condition
        }
        return render_template('home.html', data=data)
    else:
        return "Nu s-a găsit o perioadă alternativă cu condiția meteorologică dorită."


def analyze_weather(city, start_date, end_date, desired_condition):
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

        # Verifică dacă condiția predominantă nu este cea dorită și caută o perioadă alternativă
        if most_common_condition == desired_condition:
            alternative_period = find_preferred_weather_period(city, duration, desired_condition)
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


@app.route('/')
def home():
    return render_template('/tripsync-ro-website/index.html')


@app.route('/weather-analysis')
def get_weather_analysis():
    city = request.args.get('city')  # Locația pentru care se calculează datele
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    departure_location = request.args.get('departure_location')  # Locația de plecare
    weather_condition = request.args.get('weather_condition')
    print(city,start_date,end_date,departure_location,weather_condition)
    if not city or not start_date or not end_date or not departure_location or not weather_condition:
        return render_template('/tripsync-ro-website/index.html')
        #return ("Te rog să specifici orașul, perioada (start_date, end_date), locația de plecare și condiția ""meteorologică dorită.")
    weather_info = analyze_weather(city, start_date, end_date, weather_condition)

    if weather_info:
        weather_info['departure_location'] = departure_location # Adaugă locația de plecare la răspuns
        weather_info['destination_city'] = city # Adaugă orașul destinație la răspuns
        print(weather_info['destination_city'])
        if "alternative_period" in weather_info:
            alt_period=weather_info["alternative_period"]
            start_date=weather_info['alternative_period']['start_date']
            end_date=weather_info['alternative_period']['end_date']
            hotels = hotels_data.get_data(city)
        else:
            alt_period = None
            start_date = None
            end_date = None
            hotels = None        
        #,hotels=hotels.get_data(city)
        return render_template('/tripsync-ro-website/date.html',hotels=hotels,alternative_period=alt_period,departure_location=weather_info['departure_location'], destination_city=weather_info['destination_city'],start_date=start_date,end_date=end_date)
    else:
        return "Nu s-au găsit date pentru perioada sau condiția meteorologică specificată."


if __name__ == '__main__':
    app.run(debug=True)
