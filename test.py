import json
from datetime import datetime, timedelta

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
    print(consecutive_days)
    #if int(consecutive_days[0][1].split("-")[2])+2 == int(consecutive_days[1][0].split("-")[2]):
    #    return [consecutive_days[0][0],consecutive_days[1][0]]
    #else:
    longest_streak = max(consecutive_days, key=len, default=[])
    return longest_streak

def main():
    # Read JSON data from file
    with open("database/weather_data.json", "r") as file:
        weather_data = json.load(file)

    # Specify city, weather_condition, and period
    city_to_check = "Alba Iulia"
    weather_condition_to_find = "Clear"
    start_date = "2024-01-08"
    end_date = "2024-01-06"

    # Find consecutive days with the specified weather condition in the given period
    result = find_consecutive_days_in_period(weather_data, city_to_check, weather_condition_to_find, start_date, end_date)

    # Print the result
    if result:
        print(f"The most consecutive days with {weather_condition_to_find} in {city_to_check} from {start_date} to {end_date}:")
        print(result)
    else:
        print(f"No consecutive days found with {weather_condition_to_find} in {city_to_check} during the specified period.")

if __name__ == "__main__":
    main()
