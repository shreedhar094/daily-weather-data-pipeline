
import requests
import sqlite3
import logging
import time
import os

# Configure logging
logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# WeatherAPI function with retry mechanism
def get_weather_data(city):
    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        raise ValueError("WeatherAPI key not found")

    url = "https://api.weatherapi.com/v1/current.json"

    params = {
        "key": api_key,
        "q": city
    }

    for attempt in range(3):
        try:
            response = requests.get(
                url,
                params=params,
                timeout=15
            )

            response.raise_for_status()
            data = response.json()

            current = data["current"]

            weather = {
                "time": current["last_updated"],
                "temperature_2m": float(current["temp_c"]),
                "relative_humidity_2m": float(current["humidity"]),
                "apparent_temperature": float(current["feelslike_c"]),
                "wind_speed_10m": float(current["wind_kph"])
            }

            logging.info(
                "WeatherAPI successfully fetched data for %s", city
            )

            return weather

        except requests.RequestException as error:
            if attempt == 2:
                logging.error(
                    "WeatherAPI failed for %s after 3 attempts: %s",
                    city, type(error).__name__
                )
                raise RuntimeError(
                    "WeatherAPI request failed after 3 attempts"
                ) from None

            print("API request failed. Retrying...")
            logging.warning(
                "API request failed for %s. Attempt %s of 3",
                city, attempt + 1
            )

            time.sleep(5)


# Connect to database
conn = sqlite3.connect("weather.db")
cursor = conn.cursor()

try:

    # Create weather table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        time TEXT,
        temperature REAL,
        humidity REAL,
        feels_like REAL,
        wind_speed REAL
    )
    """)

    # Prevent duplicate weather records
    cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS
    idx_weather_city_time
    ON weather(city, time)
    """)

    logging.info("Weather pipeline started")

    # Cities to collect weather data
    cities = [
        "Bengaluru",
        "Mumbai",
        "Delhi"
    ]

    successful_cities = 0
    failed_cities = 0

    # Fetch weather data
    for city in cities:

        try:

            weather = get_weather_data(city)

            # Insert data into database
            cursor.execute("""
            INSERT OR IGNORE INTO weather
            (city, time, temperature, humidity, feels_like, wind_speed)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                city,
                weather["time"],
                weather["temperature_2m"],
                weather["relative_humidity_2m"],
                weather["apparent_temperature"],
                weather["wind_speed_10m"]
            ))

            if cursor.rowcount > 0:
                print(city, "data inserted successfully")
                logging.info("%s data inserted successfully", city)

            else:
                print(city, "duplicate record skipped")
                logging.info("%s duplicate record skipped", city)

            successful_cities += 1

        except (
            requests.RequestException,
            RuntimeError,
            ValueError,
            KeyError,
            sqlite3.Error
        ):

            failed_cities += 1

            print(city, "failed to process")

            logging.exception(
                "Failed to process weather data for %s", city
            )

    # Save changes
    try:

        conn.commit()

        print("\nWeather pipeline completed!")
        print("Successfully processed cities:", successful_cities)
        print("Failed cities:", failed_cities)

        logging.info(
            "Pipeline completed. Successful: %s, Failed: %s",
            successful_cities,
            failed_cities
        )

        if failed_cities == 0:
            print("All cities processed successfully.")

        elif successful_cities == 0:
            print("No cities were processed successfully.")

        else:
            print("Pipeline completed with some failures.")

    except sqlite3.Error:

        conn.rollback()

        print("Database commit failed")

        logging.exception("Database commit failed")

    logging.info("Weather pipeline finished")

except sqlite3.Error:

    logging.exception("Database operation failed")

    print("Database operation failed")

finally:

    # Close database connection
    conn.close()

    logging.info("Database connection closed")
