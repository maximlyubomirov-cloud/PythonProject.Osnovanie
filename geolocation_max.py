from opencage.geocoder import OpenCageGeocode
import pprint
from tkinter import messagebox, Tk


def get_coordinates(city, key):
    geocoder = OpenCageGeocode(key)
    query = city
    results = geocoder.geocode(query)
    #pp = pprint.PrettyPrinter(indent=4)
    # pp.print(results)
    if results:
        lat
        return results[0]['geometry']['lat'], results[0]['geometry']['lng']
    else:
        return 'Город не найден'







key = '96112fb6d80d4059ae9dabea94898600'
#city = 'Ялта'
#coordinates = get_coordinates(city, key)
#print(coordinates)
root = Tk()
root.title('Поиск координат города')
root.geometry('400x200')
entry
