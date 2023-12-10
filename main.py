from flask import Flask, jsonify
import json

app = Flask(__name__)

# Încărcarea datelor din fișierul JSON
with open('weather_data.json', 'r') as file:
    weather_data = json.load(file)

# Definirea unei rute pentru a accesa datele
@app.route('/weather', methods=['GET'])
def get_weather_data():
    return jsonify(weather_data)

# Rularea aplicației
if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=8080)
