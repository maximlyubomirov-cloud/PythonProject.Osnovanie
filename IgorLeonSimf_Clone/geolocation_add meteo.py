import requests
from opencage.geocoder import OpenCageGeocode
from tkinter import *
from translate import Translator

# Translation setup
translator = Translator(from_lang='en', to_lang='ru')


# --- GEOLOCATION ---
def get_coordinates(city, key):
    try:
        geocoder = OpenCageGeocode(key)
        results = geocoder.geocode(city)

        if results:
            # Get raw numbers for the weather API
            lat = round(results[0]['geometry']['lat'], 2)
            lng = round(results[0]['geometry']['lng'], 2)

            country_en = results[0]['components'].get('country', 'Unknown')
            region_en = results[0]['components'].get('state', '')

            # Translate safely
            try:
                country = translator.translate(country_en)
                region = translator.translate(region_en) if region_en else "Не указан"
            except Exception:
                country = country_en
                region = region_en

            # Return a dictionary so we can use the data for both text and weather
            return {
                'lat': lat,
                'lng': lng,
                'text': f'Широта: {lat}, Долгота: {lng}\nСтрана: {country}\nРегион: {region}'
            }
        else:
            return None
    except Exception as err:
        return None


# --- WEATHER ---
def get_weather(lat, lon):
    try:
        url = (f'https://api.open-meteo.com/v1/forecast'
               f'?latitude={lat}&longitude={lon}'
               f'&current_weather=true')

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        weather_data = response.json()
        return weather_data.get('current_weather', {})
    except Exception as err:
        return f'Ошибка при получении погоды: {err}'


# --- GUI FUNCTIONS ---
def show_coordinates(event=None):
    city = entry.get().strip()
    if not city:
        return

    global current_lat, current_lng  # Save coordinates globally for the weather button

    result = get_coordinates(city, key)

    if result:
        label['text'] = result['text']
        current_lat = result['lat']
        current_lng = result['lng']
    else:
        label['text'] = 'Город не найден'


def show_weather():
    if 'current_lat' not in globals():
        label['text'] = 'Сначала найдите город!'
        return

    weather_info = get_weather(current_lat, current_lng)

    if isinstance(weather_info, str):
        label['text'] = weather_info
        return

    temp = weather_info.get('temperature', 'Н/Д')
    wind = weather_info.get('windspeed', 'Н/Д')

    # Append weather to the current text
    current_text = label['text'].split('\n\n')[0]
    label['text'] = f"{current_text}\n\nТемпература: {temp}°C\nВетер: {wind} км/ч"


# --- GUI SETUP ---
key = '96112fb6d80d4059ae9dabea94898600'

root = Tk()
root.title('Поиск координат города')
root.geometry('400x300')

entry = Entry(root)
entry.pack(pady=(10, 0))
entry.bind('<Return>', show_coordinates)

btn_search = Button(root, text="Найти город", command=show_coordinates)
btn_search.pack(pady=5)

btn_weather = Button(root, text="Показать погоду", command=show_weather)
btn_weather.pack(pady=5)

label = Label(text='Введите город', justify=LEFT)
label.pack(pady=10)

# THIS MUST BE AT THE VERY BOTTOM, OUTSIDE ALL FUNCTIONS
root.mainloop()