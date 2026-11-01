from tkinter import *
from pathlib import Path

# --- Окно ---
base_dir = Path(__file__).parent
icon_path = base_dir / 'python.ico'

def unbusy(num, row): 3


# --- Функция определения цвета ряда ---
def get_row_color(row_number):
    if 1 <= row_number <= 4:
        return 'red'
    elif 5 <= row_number <= 7:
        return 'blue'
    elif 8 <= row_number <= 10:
        return 'gold'
    else:
        return 'gray'


# --- Функция определения цены ряда ---
def get_row_price(row_number):
    """Возвращает цену билета в зависимости от номера ряда."""
    if 1 <= row_number <= 4:
        return 1500  # VIP-зона
    elif 5 <= row_number <= 7:
        return 1200  # Средняя зона
    elif 8 <= row_number <= 10:
        return 1000  # Эконом-зона
    else:
        return 0


# --- Обновление шкалы прогресса ---
def update_progress():
    canvas.delete("progress")
    if total_seats == 0:
        return

    percent = (booked_count / total_seats) * 100

    if percent < 50:
        color = 'green'
    elif percent < 80:
        color = 'orange'
    else:
        color = 'red'

    fill_width = 500 * (percent / 100)
    end_x = 50 + fill_width

    if percent > 0:
        canvas.create_line(50, 20, end_x, 20, fill=color, width=8,
                           capstyle='round', tags="progress")

    canvas.create_text(300, 40,
                       text=f"Забронировано: {booked_count} из {total_seats} ({percent:.0f}%)  |  "
                            f"Сумма: {total_price} ₽",
                       font=('Arial', 10, 'bold'), tags="progress")


# --- Обработчик клика по кнопке ---
def handler(btn, base_color, price):
    """Переключает состояние места и обновляет итоговую сумму."""
    global booked_count, total_price
    current = btn.cget('bg')

    if current == 'green':
        # Отменяем бронь — возвращаем цвет ряда
        btn.config(bg=base_color)
        booked_count -= 1
        total_price -= price
    else:
        # Бронируем
        btn.config(bg='green')
        booked_count += 1
        total_price += price

    print(f"Кнопка: {btn['text']}, Цена: {price} ₽, "
          f"Всего мест: {booked_count}, Сумма: {total_price} ₽")

    update_progress()


# --- Заголовок «ЭКРАН» ---
frame1 = Frame(root)
frame1.pack(pady=10)

Label(frame1, text='ЭКРАН', font=('Arial', 16, 'bold')).pack()

canvas = Canvas(frame1, width=600, height=55, bg='white', highlightthickness=0)
canvas.pack()
canvas.create_line(50, 20, 550, 20, fill='light blue', width=8, capstyle='round')

# --- Легенда ---
legend_frame = Frame(root)
legend_frame.pack(pady=5)

Label(legend_frame, text='Легенда:', font=('Arial', 10, 'bold')).pack(side=LEFT, padx=5)

# Красный — VIP
Label(legend_frame, text='  ', bg='red').pack(side=LEFT, padx=(10, 2))
Label(legend_frame, text='Ряды 1-4 (1500 ₽)', font=('Arial', 10)).pack(side=LEFT, padx=(0, 15))

# Синий — Стандарт
Label(legend_frame, text='  ', bg='blue').pack(side=LEFT, padx=(10, 2))
Label(legend_frame, text='Ряды 5-7 (1200 ₽)', font=('Arial', 10)).pack(side=LEFT, padx=(0, 15))

# Жёлтый — Эконом
Label(legend_frame, text='  ', bg='gold').pack(side=LEFT, padx=(10, 2))
Label(legend_frame, text='Ряды 8-10 (1000 ₽)', font=('Arial', 10)).pack(side=LEFT, padx=(0, 15))

# Зелёный — Забронировано
Label(legend_frame, text='  ', bg='green').pack(side=LEFT, padx=(10, 2))
Label(legend_frame, text='Забронировано', font=('Arial', 10)).pack(side=LEFT, padx=(0, 5))

# --- Сетка мест ---
frame2 = Frame(root)
frame2.pack(pady=15)

row_count = 10
column_count = 18
total_seats = row_count * column_count

btns = []  # Список кортежей (кнопка, base_color, price)

for i in range(row_count):
    row_number = i + 1
    base_color = get_row_color(row_number)
    price = get_row_price(row_number)

    # Номер ряда слева
    row_label = Label(frame2, text=f'Ряд {row_number}',
                      font=('Arial', 10, 'bold'), fg=base_color)
    row_label.grid(row=i, column=0, padx=(5, 2), pady=2, sticky='e')

    # Цена ряда
    price_label = Label(frame2, text=f'{price} ₽',
                        font=('Arial', 9), fg='gray')
    price_label.grid(row=i, column=1, padx=(2, 8), pady=2, sticky='w')

    for j in range(column_count):
        btn = Button(
            frame2,
            text=f'{j + 1}',
            font=('Arial', 9),
            bg=base_color,
            fg='white',
            width=3,
            relief=RAISED,
            bd=2
        )
        # ✅ Передаём кнопку, цвет и цену
        btn.config(command=lambda b=btn, c=base_color, p=price: handler(b, c, p))
        btn.grid(row=i, column=j + 2, padx=2, pady=2)  # column=j+2, т.к. столбец 0 — ряд, столбец 1 — цена
        btns.append((btn, base_color, price))


# --- Кнопка очистки всех мест ---
def clear_all():
    global booked_count, total_price
    for b, base_color, _ in btns:
        b.config(bg=base_color)
    booked_count = 0
    total_price = 0
    update_progress()


Button(root, text='Очистить всё', bg='#f44336', fg='white',
       font=('Arial', 11, 'bold'), command=clear_all).pack(pady=10)

# --- Информация о ценах внизу ---
info = Label(root,
             text=f'Всего мест: {total_seats}  |  '
                  f'VIP (1-4): 1500 ₽  |  '
                  f'Стандарт (5-7): 1200 ₽  |  '
                  f'Эконом (8-10): 1000 ₽',
             font=('Arial', 9), fg='gray')
info.pack(pady=5)

# Инициализация шкалы
update_progress()

# --- Запуск ---
root.mainloop()