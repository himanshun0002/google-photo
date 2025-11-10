from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('location.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT,
                    state TEXT,
                    country TEXT,
                    latitude REAL,
                    longitude REAL,
                    timestamp TEXT
                )''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/save_location', methods=['POST'])
def save_location():
    data = request.get_json()
    city = data.get('city')
    state = data.get('state')
    country = data.get('country')
    lat = data.get('latitude')
    lon = data.get('longitude')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect('location.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (city, state, country, latitude, longitude, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
              (city, state, country, lat, lon, timestamp))
    conn.commit()
    conn.close()

    return jsonify({"message": "Location saved successfully!"})

@app.route('/show_users')
def show_users():
    conn = sqlite3.connect('location.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return jsonify(data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
