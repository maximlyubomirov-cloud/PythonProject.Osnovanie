# -*- coding: utf-8 -*-
"""
Единое приложение «Практикум Tkinter»
Листинги 2.1.2 + 2.1.3 + СРС 2.2
"""

from tkinter import *
from tkinter import messagebox as mb
from tkinter import filedialog as fd
import time
import datetime as dt
import random


# =========================================================
#  2.1.2  ЗАДАЧА 1. БРАУЗЕР (tkinterweb)
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
    win.title("2.1.2-1. Просмотр сайта")
    win.geometry("800x600")

    def read():
        frame.load_website(e.get())

    f = Frame(win); f.pack(fill=X)
    Label(f, text="введите адрес сайта:").pack(side=LEFT, padx=5)
    e = Entry(f, width=40, justify='left'); e.pack(side=LEFT, padx=5)
    Button(f, text="Ввод", command=read).pack(side=LEFT, padx=5)

    frame = tkinterweb.HtmlFrame(win)
    frame.pack(fill="both", expand=1)
    frame.load_website("https://www.google.com")


# =========================================================
#  2.1.2  ЗАДАЧА 2. ДАТА И ВРЕМЯ
# =========================================================
def task_datetime():
    win = Toplevel(root)
    win.title("2.1.2-2. Дата и время")
    Label(win, text=time.strftime('%d %B %Y, %H:%M:%S'),
          font="Verdana 20 bold").pack(padx=30, pady=30)


# =========================================================
#  2.1.2  ЗАДАЧА 3. ДАТА С РУССКИМ МЕСЯЦЕМ
# =========================================================
def task_date_ru():
    win = Toplevel(root)
    win.title("2.1.2-3. Дата на русском")

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
#  2.1.2  ЗАДАЧА 4. ЧАСЫ
# =========================================================
def task_clock():
    win = Toplevel(root)
    win.title("2.1.2-4. Часы")

    m = Label(win, font="Verdana 24 bold"); m.pack(padx=30, pady=30)

    def tick():
        m.config(text=time.strftime("%H:%M:%S"))
        m.after(1000, tick)

    tick()


# =========================================================
#  2.1.2  ЗАДАЧА 5. ДЕНЬ НЕДЕЛИ
# =========================================================
def task_weekday():
    win = Toplevel(root)
    win.title("2.1.2-5. Сегодня ...")

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
#  2.1.2  ЗАДАЧА 6. НАПИТКИ
# =========================================================
def task_drinks():
    win = Toplevel(root)
    win.title("2.1.2-6. Любимый напиток")

    kvas, tea, coffee = "Квас", "Чай", "Кофе"
    drink = StringVar(value=coffee)

    Label(win, text="Выбери любимый напиток:",
          font="Verdana 12").pack(pady=5)

    Radiobutton(win, text=kvas,   value=kvas,   variable=drink).pack(anchor=W, padx=20)
    Radiobutton(win, text=tea,    value=tea,    variable=drink).pack(anchor=W, padx=20)
    Radiobutton(win, text=coffee, value=coffee, variable=drink).pack(anchor=W, padx=20)

    Label(win, textvariable=drink,
          font="Verdana 16 bold", fg="blue").pack(pady=15)


# =========================================================
#  2.1.2  ЗАДАЧА 7. ЧАСЫ С РАДИОКНОПКАМИ + НОЧНАЯ ТЕМА
# =========================================================
def task_clock_radio():
    win = Toplevel(root)
    win.title("2.1.2-7. Часы с режимами")

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
    R1 = Radiobutton(win, text="Дата и время", command=show_datetime, variable=var, value=0)
    R2 = Radiobutton(win, text="Дата",         command=show_date,     variable=var, value=1)
    R3 = Radiobutton(win, text="Время",        command=show_time,     variable=var, value=2)
    R4 = Radiobutton(win, text="Ночная тема",  command=night,         variable=var, value=3)

    for r in (R1, R2, R3, R4):
        r.pack(side=LEFT, padx=5)

    m = Label(win, font="Verdana 20 bold", text=f"{Date} {Time}")
    m.pack(side=LEFT, padx=15)


# =========================================================
#  2.1.2  ЗАДАЧА 8. ЧАСЫ С ФЛАЖКАМИ
# =========================================================
def task_clock_checks():
    win = Toplevel(root)
    win.title("2.1.2-8. Часы с флажками")

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
#  СРС 2.2  ЗАДАЧА 9. РИСОВАНИЕ ФИГУР
# =========================================================
def task_draw():
    win = Toplevel(root)
    win.title("СРС 2.2. Рисование фигур")

    canvas = Canvas(win, width=300, height=200, bg="salmon")
    canvas.pack(pady=10)

    def draw_circle():
        canvas.create_oval(50, 30, 150, 130,
                           fill=fill_entry.get(), outline=outline_entry.get(), width=2)
    def draw_square():
        canvas.create_rectangle(50, 30, 150, 130,
                                fill=fill_entry.get(), outline=outline_entry.get(), width=2)
    def draw_triangle():
        canvas.create_polygon([100, 20, 40, 140, 160, 140],
                              fill=fill_entry.get(), outline=outline_entry.get(), width=2)
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
#  2.1.3  ЗАДАЧА 10. ОКНА MESSAGEBOX (askyesno и др.)
# =========================================================
def task_messagebox():
    win = Toplevel(root)
    win.title("2.1.3-10. Окна Messagebox")

    def check_yesno():
        if mb.askyesno(title="Вопрос", message="Перенести данные?"):
            s = e.get()
            e.delete(0, END)
            m['text'] = s

    def check_okcancel():
        if mb.askokcancel(title="Вопрос", message="Перенести данные?"):
            s = e.get()
            e.delete(0, END)
            m['text'] = s

    def check_retrycancel():
        if mb.askretrycancel(title="Вопрос", message="Перенести данные?"):
            s = e.get()
            e.delete(0, END)
            m['text'] = s

    e = Entry(win); e.pack(pady=5)

    Button(win, text="askyesno",       command=check_yesno).pack(fill=X, padx=20)
    Button(win, text="askokcancel",    command=check_okcancel).pack(fill=X, padx=20)
    Button(win, text="askretrycancel", command=check_retrycancel).pack(fill=X, padx=20)

    m = Label(win, height=3); m.pack(fill=X, padx=20)


# =========================================================
#  2.1.3  ЗАДАЧА 11. ИГРА «УГАДАЙ ЧИСЛО»
# =========================================================
def task_guess():
    win = Toplevel(root)
    win.title('2.1.3-11. Игра "Угадай число"')

    def check():
        s = e.get()
        if not s.isdigit():
            mb.showerror("Ошибка", "Введите число")
            return

        rnd = random.randint(1, 2)
        if int(s) == rnd:
            mb.showinfo(title="Результат", message="Угадал!")
        else:
            mb.showinfo(title="Результат", message=f"Неудача :(\nБыло загадано: {rnd}")

        if mb.askretrycancel(title="Вопрос", message="Загадать еще одно число?"):
            e.delete(0, END)
        else:
            win.destroy()

    Label(win, height=3,
          text="Введи число, которое я загадал, и нажми на кнопку").pack()
    e = Entry(win); e.pack()
    Button(win, text="Передать", command=check).pack()


# =========================================================
#  2.1.3  ЗАДАЧА 12. КАЛЬКУЛЯТОР СУММЫ ТРЁХ ЧИСЕЛ
# =========================================================
def task_calc3():
    win = Toplevel(root)
    win.title("2.1.3-12. Калькулятор")

    def summ():
        values = []
        for i, entry in enumerate((e1, e2, e3), start=1):
            s = entry.get()
            if not s.lstrip('-').isdigit():
                mb.showerror("Ошибка",
                             f"В поле {i} должно быть введено число")
                return
            values.append(int(s))

        s1, s2, s3 = (str(v) for v in values)
        total = sum(values)
        m1['text'] = f"{s1} + {s2} + {s3} = {total}"

        if mb.askretrycancel(title="Вопрос",
                             message="Сложить еще три числа?"):
            for entry in (e1, e2, e3):
                entry.delete(0, END)
            m1['text'] = ""
        else:
            win.destroy()

    Label(win, height=3,
          text="Введите три числа и нажмите кнопку").pack()
    e1 = Entry(win); e1.pack()
    e2 = Entry(win); e2.pack()
    e3 = Entry(win); e3.pack()
    Button(win, text="Сложить три числа", command=summ).pack(pady=5)
    m1 = Label(win, height=3); m1.pack()


# =========================================================
#  2.1.3  ЗАДАЧА 13. ГЛАВНОЕ ОКНО (геометрия + центр)
# =========================================================
def task_main_window():
    win = Toplevel(root)
    win.title("2.1.3-13. Окно в центре экрана")

    w = win.winfo_screenwidth()
    h = win.winfo_screenheight()

    w2 = w // 2 - 200
    h2 = h // 2 - 150

    win.geometry(f"400x300+{w2}+{h2}")

    Label(win, text=f"Экран: {w} x {h}\n"
                    f"Окно: 400x300+{w2}+{h2}",
          font="Verdana 14").pack(expand=True)


# =========================================================
#  2.1.3  ЗАДАЧА 14. БЛОКНОТ (открыть / сохранить)
# =========================================================
def task_notepad():
    win = Toplevel(root)
    win.title("2.1.3-14. Блокнот")

    def delete():
        text.delete(1.0, END)

    def open_file():
        try:
            file = fd.askopenfilename()
            if file:
                with open(file, 'r', encoding='utf-8') as f:
                    s = f.read()
                text.delete(1.0, END)
                text.insert(1.0, s)
        except FileNotFoundError:
            mb.showerror("Ошибка", "Файл не найден")
        except Exception as e:
            mb.showerror("Ошибка", f"Произошла ошибка: {e}")

    def save():
        try:
            file = fd.asksaveasfilename(
                filetypes=(("TXT files", "*.txt"),
                           ("HTML files", "*.html;*.htm"),
                           ("All files", "*.*")))
            if file:
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(text.get(1.0, END))
        except FileNotFoundError:
            mb.showerror("Ошибка", "Не удалось сохранить файл")
        except Exception as e:
            mb.showerror("Ошибка", f"Произошла ошибка: {e}")

    def close_app():
        win.destroy()

    # --- Меню ---
    mainmenu = Menu(win)
    win.config(menu=mainmenu)

    filemenu = Menu(mainmenu, tearoff=0)
    filemenu.add_command(label="Открыть",  command=open_file)
    filemenu.add_command(label="Новый",    command=delete)
    filemenu.add_command(label="Сохранить", command=save)
    filemenu.add_separator()
    filemenu.add_command(label="Выход",    command=close_app)
    mainmenu.add_cascade(label="Файл", menu=filemenu)

    # --- Текст + скролл ---
    text = Text(win, width=40, height=12, bg="lightgray", wrap=WORD)
    text.pack(side=LEFT, fill=BOTH, expand=1)

    scroll = Scrollbar(win, command=text.yview)
    scroll.pack(side=LEFT, fill=Y)
    text.config(yscrollcommand=scroll.set)


# =========================================================
#  2.1.3  ЗАДАЧА 15. ПРОСМОТР ИЗОБРАЖЕНИЙ (PIL)
# =========================================================
def task_photo():
    try:
        from PIL import Image, ImageTk
    except ImportError:
        _error("Библиотека Pillow не установлена.\n"
               "Установите командой:\n"
               "pip install Pillow")
        return

    win = Toplevel(root)
    win.title("2.1.3-15. Просмотр изображений")
    win.geometry("500x500")

    def open_image():
        try:
            file = fd.askopenfilename()
            if file:
                img = Image.open(file)
                img.thumbnail((500, 500))
                img_tk = ImageTk.PhotoImage(img)

                if hasattr(win, 'photo_label'):
                    win.photo_label.configure(image=img_tk)
                    win.photo_label.image = img_tk
                else:
                    win.photo_label = Label(win, image=img_tk)
                    win.photo_label.image = img_tk
                    win.photo_label.pack()
        except FileNotFoundError:
            mb.showerror("Ошибка", "Файл не найден")
        except OSError:
            mb.showerror("Ошибка", "Не удалось открыть файл,\nвозможно это не изображение")
        except Exception as e:
            mb.showerror("Ошибка", f"Произошла ошибка: {e}")

    mainmenu = Menu(win)
    win.config(menu=mainmenu)

    filemenu = Menu(mainmenu, tearoff=0)
    filemenu.add_command(label="Открыть...", command=open_image)
    filemenu.add_separator()
    filemenu.add_command(label="Выход", command=win.destroy)
    mainmenu.add_cascade(label="Файл", menu=filemenu)


# =========================================================
#  ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ
# =========================================================
def _error(message):
    mb.showerror("Ошибка", message)


# =========================================================
#  ГЛАВНОЕ ОКНО С МЕНЮ
# =========================================================
root = Tk()
root.title("Практикум Tkinter — 2.1.2 + 2.1.3 + 2.2")
root.geometry("440x280")
root.configure(bg="#f0f0f0")

Label(root, text="Практикум Tkinter",
      font="Verdana 18 bold", bg="#f0f0f0").pack(pady=15)
Label(root, text="Выберите задачу в меню сверху ↑",
      font="Verdana 11", bg="#f0f0f0").pack()

# ---------- Строка меню ----------
menubar = Menu(root)

# --- 2.1.2 ---
m_212 = Menu(menubar, tearoff=0)
m_212.add_command(label="1. Просмотр сайта (tkinterweb)", command=task_browser)
m_212.add_separator()
m_212.add_command(label="2. Дата и время",           command=task_datetime)
m_212.add_command(label="3. Дата с рус. месяцем",    command=task_date_ru)
m_212.add_command(label="4. Часы",                   command=task_clock)
m_212.add_command(label="5. День недели по-русски",  command=task_weekday)
m_212.add_separator()
m_212.add_command(label="6. Радиокнопки — напитки",  command=task_drinks)
m_212.add_command(label="7. Часы с радиокнопками",   command=task_clock_radio)
m_212.add_command(label="8. Часы с флажками",        command=task_clock_checks)
menubar.add_cascade(label="2.1.2", menu=m_212)

# --- 2.1.3 ---
m_213 = Menu(menubar, tearoff=0)
m_213.add_command(label="10. Окна Messagebox",       command=task_messagebox)
m_213.add_command(label="11. Игра «Угадай число»",   command=task_guess)
m_213.add_command(label="12. Калькулятор (3 числа)", command=task_calc3)
m_213.add_separator()
m_213.add_command(label="13. Окно в центре экрана",  command=task_main_window)
m_213.add_separator()
m_213.add_command(label="14. Блокнот",               command=task_notepad)
m_213.add_command(label="15. Просмотр изображений",  command=task_photo)
menubar.add_cascade(label="2.1.3", menu=m_213)

# --- СРС 2.2 ---
m_22 = Menu(menubar, tearoff=0)
m_22.add_command(label="9. Рисование фигур", command=task_draw)
menubar.add_cascade(label="СРС 2.2", menu=m_22)

# --- Файл ---
m_file = Menu(menubar, tearoff=0)
m_file.add_command(label="Выход", command=root.quit)
menubar.add_cascade(label="Файл", menu=m_file)

root.config(menu=menubar)

# ---------- Запуск ----------
root.mainloop()