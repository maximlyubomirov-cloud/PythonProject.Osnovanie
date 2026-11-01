# -*- coding: utf-8 -*-
"""
Единое приложение «Практикум Tkinter»
Объединяет задачи из листингов 2.1.2 и СРС 2.2
"""

from tkinter import *
import time
import datetime as dt


# =========================================================
#  ЗАДАЧА 1. БРАУЗЕР (tkinterweb) — фрейм слева направо
# =========================================================
def task_browser():
    try:
        import tkinterweb
    except ImportError:
        _error("Библиотека tkinterweb не установлена.\n"
               "Установите командой:\n"
               "pip install tkinterweb")
        return

    win = Toplevel(root)
    win.title("Задача 1. Просмотр сайта")
    win.geometry("800x600")

    def read():
        frame.load_website(e.get())

    # Верхняя панель: метка + поле + кнопка слева направо
    f = Frame(win)
    f.pack(fill=X)

    Label(f, text="введите адрес сайта:").pack(side=LEFT, padx=5)
    e = Entry(f, width=40, justify='left')
    e.pack(side=LEFT, padx=5)
    Button(f, text="Ввод", command=read).pack(side=LEFT, padx=5)

    # Область браузера
    frame = tkinterweb.HtmlFrame(win)
    frame.pack(fill="both", expand=1)
    frame.load_website("https://www.google.com")


# =========================================================
#  ЗАДАЧА 2. ДАТА И ВРЕМЯ
# =========================================================
def task_datetime():
    win = Toplevel(root)
    win.title("Задача 2. Дата и время")

    text = time.strftime('%d %B %Y, %H:%M:%S')
    Label(win, text=text, font="Verdana 20 bold").pack(padx=30, pady=30)


# =========================================================
#  ЗАДАЧА 3. ДАТА С РУССКИМ МЕСЯЦЕМ (день → месяц → год)
# =========================================================
def task_date_ru():
    win = Toplevel(root)
    win.title("Задача 3. Дата на русском")

    Month = time.strftime('%B')
    Year  = time.strftime('%Y')
    Day   = time.strftime('%d')

    match Month:
        case "January":   Month = "Января"
        case "February":  Month = "Февраля"
        case "March":     Month = "Марта"
        case "April":     Month = "Апреля"
        case "May":       Month = "Мая"
        case "June":      Month = "Июня"
        case "July":      Month = "Июля"
        case "August":    Month = "Августа"
        case "September": Month = "Сентября"
        case "October":   Month = "Октября"
        case "November":  Month = "Ноября"
        case "December":  Month = "Декабря"

    Label(win, text=f"{Day} {Month} {Year}",
          font="Verdana 20 bold").pack(padx=30, pady=30)


# =========================================================
#  ЗАДАЧА 4. ЧАСЫ (обновление каждую секунду)
# =========================================================
def task_clock():
    win = Toplevel(root)
    win.title("Задача 4. Часы")

    m = Label(win, font="Verdana 24 bold")
    m.pack(padx=30, pady=30)

    def tick():
        m.config(text=time.strftime("%H:%M:%S"))
        m.after(1000, tick)

    tick()


# =========================================================
#  ЗАДАЧА 5. ДЕНЬ НЕДЕЛИ ПО-РУССКИ
# =========================================================
def task_weekday():
    win = Toplevel(root)
    win.title("Задача 5. Сегодня ...")

    Day = time.strftime('%A')
    match Day:
        case "Monday":    Day = "понедельник"
        case "Tuesday":   Day = "вторник"
        case "Wednesday": Day = "среда"
        case "Thursday":  Day = "четверг"
        case "Friday":    Day = "пятница"
        case "Saturday":  Day = "суббота"
        case "Sunday":    Day = "воскресенье"

    Label(win, text="Сегодня " + Day,
          font="Verdana 20 bold").pack(padx=30, pady=30)


# =========================================================
#  ЗАДАЧА 6. РАДИОКНОПКИ — НАПИТКИ + МЕТКА ВЫБОРА
# =========================================================
def task_drinks():
    win = Toplevel(root)
    win.title("Задача 6. Любимый напиток")

    kvas, tea, coffee = "Квас", "Чай", "Кофе"
    drink = StringVar(value=coffee)

    Label(win, text="Выбери любимый напиток:",
          font="Verdana 12").pack(pady=5)

    Radiobutton(win, text=kvas,   value=kvas,   variable=drink).pack(anchor=W, padx=20)
    Radiobutton(win, text=tea,    value=tea,    variable=drink).pack(anchor=W, padx=20)
    Radiobutton(win, text=coffee, value=coffee, variable=drink).pack(anchor=W, padx=20)

    # Метка автоматически обновляется через textvariable
    Label(win, textvariable=drink,
          font="Verdana 16 bold", fg="blue").pack(pady=15)


# =========================================================
#  ЗАДАЧА 7. ЧАСЫ С РАДИОКНОПКАМИ + НОЧНАЯ ТЕМА
# =========================================================
def task_clock_radio():
    win = Toplevel(root)
    win.title("Задача 7. Часы с режимами")

    d = dt.datetime.now()
    Date = d.strftime('%d %B %Y')
    Time = d.strftime('%X')

    def show_datetime(): m.config(text=f"{Date} {Time}")
    def show_date():     m.config(text=Date)
    def show_time():     m.config(text=Time)

    def night():
        for w in (m, R1, R2, R3, R4):
            w.config(bg="black", fg="white")

    var = IntVar(value=0)

    R1 = Radiobutton(win, text="Дата и время", command=show_datetime,
                     variable=var, value=0)
    R2 = Radiobutton(win, text="Дата",         command=show_date,
                     variable=var, value=1)
    R3 = Radiobutton(win, text="Время",        command=show_time,
                     variable=var, value=2)
    R4 = Radiobutton(win, text="Ночная тема",  command=night,
                     variable=var, value=3)

    for r in (R1, R2, R3, R4):
        r.pack(side=LEFT, padx=5)

    m = Label(win, font="Verdana 20 bold", text=f"{Date} {Time}")
    m.pack(side=LEFT, padx=15)


# =========================================================
#  ЗАДАЧА 8. ЧАСЫ С ФЛАЖКАМИ (фон, текст, шрифт, высота)
# =========================================================
def task_clock_checks():
    win = Toplevel(root)
    win.title("Задача 8. Часы с флажками")

    def tick():
        m.config(text=time.strftime("%H:%M:%S"))
        m.after(1000, tick)

    def bg_color(): m['bg']     = v1.get()
    def fg_color(): m['fg']     = v2.get()
    def font():     m['font']   = v3.get()
    def size():     m['height'] = v4.get()

    m = Label(win, font='Verdana 16', bg='lightblue', fg='black')
    m.pack(padx=20, pady=10)

    v1 = StringVar(value='lightblue')
    Checkbutton(win, text='Цвет фона', variable=v1,
                onvalue='salmon', offvalue='lightblue',
                command=bg_color).pack(anchor=W, padx=20)

    v2 = StringVar(value='black')
    Checkbutton(win, text='Цвет текста', variable=v2,
                onvalue='white', offvalue='black',
                command=fg_color).pack(anchor=W, padx=20)

    v3 = StringVar(value='Verdana 16')
    Checkbutton(win, text='Шрифт', variable=v3,
                onvalue='Courier 16 bold', offvalue='Verdana 16',
                command=font).pack(anchor=W, padx=20)

    v4 = IntVar(value=1)
    Checkbutton(win, text='Переключатель высоты (1 ↔ 3)', variable=v4,
                onvalue=3, offvalue=1,
                command=size).pack(anchor=W, padx=20)

    tick()


# =========================================================
#  ЗАДАЧА 9. РИСОВАНИЕ ФИГУР (СРС 2.2)
# =========================================================
def task_draw():
    win = Toplevel(root)
    win.title("Задача 9. Рисование фигур")

    canvas = Canvas(win, width=300, height=200, bg="salmon")
    canvas.pack(pady=10)

    def draw_circle():
        canvas.create_oval(50, 30, 150, 130,
                           fill=fill_entry.get(),
                           outline=outline_entry.get(), width=2)

    def draw_square():
        canvas.create_rectangle(50, 30, 150, 130,
                                fill=fill_entry.get(),
                                outline=outline_entry.get(), width=2)

    def draw_triangle():
        points = [100, 20, 40, 140, 160, 140]
        canvas.create_polygon(points,
                              fill=fill_entry.get(),
                              outline=outline_entry.get(), width=2)

    def clear_canvas():
        canvas.delete("all")

    def change_background():
        try:
            canvas.config(bg=bg_entry.get())
        except TclError:
            _error("Некорректный цвет: " + bg_entry.get())

    Button(win, text="Окружность",  width=22, command=draw_circle).pack(pady=2)
    Button(win, text="Треугольник", width=22, command=draw_triangle).pack(pady=2)
    Button(win, text="Квадрат",     width=22, command=draw_square).pack(pady=2)
    Button(win, text="Очистить",    width=22, command=clear_canvas).pack(pady=2)

    Label(win, text="Цвет заливки:").pack()
    fill_entry = Entry(win); fill_entry.insert(0, "lightblue"); fill_entry.pack()

    Label(win, text="Цвет обводки:").pack()
    outline_entry = Entry(win); outline_entry.insert(0, "blue"); outline_entry.pack()

    Label(win, text="Цвет фона:").pack()
    bg_entry = Entry(win); bg_entry.insert(0, "white"); bg_entry.pack()

    Button(win, text="Изменить цвет фона", width=22,
           command=change_background).pack(pady=5)


# =========================================================
#  ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ДЛЯ СООБЩЕНИЙ ОБ ОШИБКАХ
# =========================================================
def _error(message):
    from tkinter import messagebox
    messagebox.showerror("Ошибка", message)


# =========================================================
#  ГЛАВНОЕ ОКНО С МЕНЮ
# =========================================================
root = Tk()
root.title("Практикум Tkinter — 2.1.2 + 2.2")
root.geometry("420x260")
root.configure(bg="#f0f0f0")

Label(root, text="Практикум Tkinter",
      font="Verdana 18 bold", bg="#f0f0f0").pack(pady=15)
Label(root, text="Выберите задачу в меню сверху ↑",
      font="Verdana 11", bg="#f0f0f0").pack()

# ---------- Строка меню ----------
menubar = Menu(root)

# Меню «Веб»
m_web = Menu(menubar, tearoff=0)
m_web.add_command(label="1. Просмотр сайта (tkinterweb)", command=task_browser)
menubar.add_cascade(label="Веб", menu=m_web)

# Меню «Дата и время»
m_date = Menu(menubar, tearoff=0)
m_date.add_command(label="2. Дата и время",           command=task_datetime)
m_date.add_command(label="3. Дата с рус. месяцем",    command=task_date_ru)
m_date.add_command(label="4. Часы",                   command=task_clock)
m_date.add_command(label="5. День недели по-русски",  command=task_weekday)
menubar.add_cascade(label="Дата и время", menu=m_date)

# Меню «Виджеты»
m_widgets = Menu(menubar, tearoff=0)
m_widgets.add_command(label="6. Радиокнопки — напитки",   command=task_drinks)
m_widgets.add_command(label="7. Часы с радиокнопками",    command=task_clock_radio)
m_widgets.add_command(label="8. Часы с флажками",         command=task_clock_checks)
menubar.add_cascade(label="Виджеты", menu=m_widgets)

# Меню «Графика»
m_graphics = Menu(menubar, tearoff=0)
m_graphics.add_command(label="9. Рисование фигур (СРС 2.2)", command=task_draw)
menubar.add_cascade(label="Графика", menu=m_graphics)

# Меню «Файл»
m_file = Menu(menubar, tearoff=0)
m_file.add_command(label="Выход", command=root.quit)
menubar.add_cascade(label="Файл", menu=m_file)

root.config(menu=menubar)

# ---------- Запуск ----------
root.mainloop()