car_info = input("Введите параметры автомобиля: ")
brand,year,mileage,price = car_info.split()
print(f"Марка: {brand}\n"
      f"Год: {year[:-1]}\n"
      f"Пробег: {mileage[:-2]} км\n"
      f"Цена: {price[:-3]} руб")