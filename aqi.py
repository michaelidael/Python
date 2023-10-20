import main_functions
import requests
import folium

"""Task 6"""
def get_api_key(filename):
    my_api = main_functions.read_from_file(filename)
    api_key = my_api["aqi_api_key"]
    return api_key

my_aqi_api_key = get_api_key("api_key.json")
print(my_aqi_api_key)

"""Task #7"""
def get_aqi_data(api_key):
     url = "http://api.airvisual.com/v2/nearest_city?key="
     url_aqi = url + api_key
     response = requests.get(url_aqi).json()
     main_functions.save_to_file(response, "aqi.json")
     aqi = main_functions.read_from_file("aqi.json")
get_aqi_data(my_aqi_api_key)


"""Task 8"""
def generate_map(data_filename,zoom_start):
    aqi_data = main_functions.read_from_file(data_filename)
    lat = aqi_data["data"]["location"]["coordinates"][1]
    long = aqi_data["data"]["location"]["coordinates"][0]
    m = folium.Map(location=[lat, long], zoom_start=zoom_start)
    folium.Marker(
        location=[lat, long],
        popup='AQI Station',
        icon=folium.Icon()
    ).add_to(m)
    m.save("map.html")

"""Task 9"""
import math
def display_aqi_info(data_filename):
    aqi_data = main_functions.read_from_file(data_filename)
    tempC = aqi_data["data"]["current"]["weather"]["tp"]
    tempF = math.trunc(tempC * 9 / 5 + 32)
    humid = aqi_data["data"]["current"]["weather"]["hu"]
    aqius = aqi_data["data"]["current"]["pollution"]["aqius"]

    print("The temperature is", tempC,"°C or",tempF,"°F, the humidity is",humid,"%, ")
    if (aqius >= 0) and (aqius <= 50):
        print("and the index shows that the air quality is good")
    elif (aqius >= 51) and (aqius <= 149):
        print("and the index shows that the air quality is moderate")
    elif (aqius >= 101) and (aqius <= 150):
        print("and the index shows that the air quality is unhealthy for sensitive groups")
    elif (aqius >= 151) and (aqius <= 200):
        print("and the index shows that the air quality is unhealthy ")
    elif (aqius >= 201) and (aqius <= 300):
        print("and the index shows that the air quality is very unhealthy ")
    else:
        print("unknown")

display_aqi_info("aqi.json")