from flask import Flask, request, json, render_template
from datetime import datetime
import hotels as hotels_data
from flask import jsonify
import json
from datetime import datetime, timedelta
app = Flask(__name__)

with open('database/weather_data.json') as f:
    weather_data = json.load(f)

def find_consecutive_days_in_period(data, city, weather_condition, start_date, end_date):
    if city not in data:
        return []

    start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
    current_datetime = start_datetime

    consecutive_days = []
    current_consecutive_days = []

    while current_datetime <= end_datetime:
        current_date_str = current_datetime.strftime("%Y-%m-%d")

        # Check if the current date is in the data for the city
        if any(entry["date"] == current_date_str for entry in data[city]):
            # Get the weather condition for the current date
            current_weather_condition = next(entry["weather_condition"] for entry in data[city] if entry["date"] == current_date_str)

            # Check if the weather condition matches the desired condition
            if current_weather_condition == weather_condition:
                current_consecutive_days.append(current_date_str)
            else:
                # If there was a streak, save it
                if current_consecutive_days:
                    consecutive_days.append(current_consecutive_days)
                current_consecutive_days = []

        current_datetime += timedelta(days=1)

    # Check again at the end in case the last days are consecutive
    if current_consecutive_days:
        consecutive_days.append(current_consecutive_days)

    # Find the longest consecutive streak
    print(consecutive_days, city, weather_condition, start_date, end_date)
    #if int(consecutive_days[0][1].split("-")[2])+2 == int(consecutive_days[1][0].split("-")[2]):
    #    return [consecutive_days[0][0],consecutive_days[1][0]]
    #else:
    longest_streak = max(consecutive_days, key=len, default=[])
    return longest_streak

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
    #weather_info = analyze_weather(city, start_date, end_date, weather_condition)
    #hotels = hotels_data.get_data(city)
    hotels = None
    date_vreme = find_consecutive_days_in_period(weather_data,city,weather_condition,start_date,end_date)

    if len(date_vreme) > 1:
        return render_template('/tripsync-ro-website/date.html',hotels=hotels,departure_location=departure_location, destination_city=city,start_date=date_vreme[0],end_date=date_vreme[len(date_vreme)-1])
    elif len(date_vreme) == 1:
        return render_template('/tripsync-ro-website/date.html',hotels=hotels,departure_location=departure_location, destination_city=city,start_date=date_vreme[0],end_date=date_vreme[0])
    else:
        return render_template('/tripsync-ro-website/date.html',hotels=hotels,departure_location=departure_location, destination_city=city,start_date=date_vreme,end_date=date_vreme)
    '''
    if weather_info:
        weather_info['departure_location'] = departure_location # Adaugă locația de plecare la răspuns
        weather_info['destination_city'] = city # Adaugă orașul destinație la răspuns
        print(weather_info['destination_city'])
        if "alternative_period" in weather_info:
            alt_period=weather_info["alternative_period"]
            start_date=weather_info['alternative_period']['start_date']
            end_date=weather_info['alternative_period']['end_date']
            #hotels = None
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
'''

if __name__ == '__main__':
    app.run(debug=True)
