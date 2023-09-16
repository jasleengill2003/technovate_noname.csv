import requests
from datetime import datetime

def geocode(api_key, location_name):
    BASE_URL = "https://graphhopper.com/api/1/geocode"
    params = {
        'q': location_name,
        'key': api_key,
        'limit': 1
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    lat = data['hits'][0]['point']['lat']
    lon = data['hits'][0]['point']['lng']

    return lat, lon

def get_route_info(api_key, start_lat_lon, end_lat_lon):
    BASE_URL = "https://graphhopper.com/api/1/route"
    params = {
        'point': [f"{start_lat_lon[0]},{start_lat_lon[1]}", f"{end_lat_lon[0]},{end_lat_lon[1]}"],
        'vehicle': 'car',
        'locale': 'en',
        'key': api_key
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    distance = data['paths'][0]['distance'] / 1000  # Convert to km
    time = data['paths'][0]['time'] / 60000  # Convert to minutes

    return distance, time

def calculate_fare(time, distance, mode_of_transport, base_prices, is_peak_hours):
    # Fare rates per minute for different modes of transport
    fare_rates_per_minute = {
        'auto': 0.5,
        'cab': 0.6,
        'taxi': 0.7
    }

    # Per kilometer prices for different modes of transport during peak and non-peak hours
    per_km_prices = {
        'auto': {'non_peak': 14, 'peak': 16},
        'cab': {'non_peak': 18, 'peak': 20},
        'taxi': {'non_peak': 16, 'peak': 18}
    }

    if mode_of_transport in fare_rates_per_minute:
        rate_per_minute = fare_rates_per_minute[mode_of_transport]

        # Select the per kilometer price based on peak hours
        if is_peak_hours:
            rate_per_km = per_km_prices[mode_of_transport]['peak']
        else:
            rate_per_km = per_km_prices[mode_of_transport]['non_peak']

        fare = (time * rate_per_minute) + (distance * rate_per_km)

        # Ensure fare is above the base price
        if fare < base_prices[mode_of_transport]:
            fare = base_prices[mode_of_transport]

        return fare
    else:
        return None

if __name__ == "__main__":
    API_KEY = 'apikey'  # Replace with your GraphHopper API key
    start_name = input("Enter the starting place name: ")
    end_name = input("Enter the destination place name: ")

    start_lat_lon = geocode(API_KEY, start_name)
    end_lat_lon = geocode(API_KEY, end_name)

    distance, base_time = get_route_info(API_KEY, start_lat_lon, end_lat_lon)

    print(f"The distance from {start_name} to {end_name} is approximately {distance:.2f} km.")

    # Determine the current time and day
    current_time = datetime.now().time()
    current_day = datetime.now().strftime("%A")

    # Define peak hours
    peak_hours_start = datetime.strptime("09:00:00", "%H:%M:%S").time()
    peak_hours_end = datetime.strptime("11:00:00", "%H:%M:%S").time()

    evening_peak_start = datetime.strptime("18:00:00", "%H:%M:%S").time()
    evening_peak_end = datetime.strptime("21:00:00", "%H:%M:%S").time()

    # Check if it's Sunday (no peak hours)
    if current_day == "Sunday":
        time_multiplier = 2.5  # Non-peak hours on Sunday
        peak_hours_text = "No"
    else:
        # Check if it's peak hours
        if (current_time >= peak_hours_start and current_time <= peak_hours_end) or (current_time >= evening_peak_start and current_time <= evening_peak_end):
            time_multiplier = 3.5  # Peak hours, multiply by 3.5
            peak_hours_text = "Yes"
        else:
            time_multiplier = 2.5  # Non-peak hours, multiply by 2.5
            peak_hours_text = "No"

    adjusted_time = base_time * time_multiplier

    print(f"Is it peak hours? {peak_hours_text}")
    print(f"Travel time will take roughly {adjusted_time:.2f} minutes.")

    # Ask for the mode of transport and base prices
    mode_of_transport = input("Enter the mode of transport (auto/cab/taxi): ").lower()

    # Define base prices for each mode of transport
    base_prices = {
        'auto': 23,
        'cab': 30,
        'taxi': 40
    }

    fare = calculate_fare(adjusted_time, distance, mode_of_transport, base_prices, peak_hours_text == "Yes")

    if fare is not None:
        print(f"The estimated fare for a {mode_of_transport} journey is approximately {fare:.2f} INR.")
    else:
        print("Invalid mode of transport.")
