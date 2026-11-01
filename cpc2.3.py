# -*- coding: utf-8 -*-
"""
Практикум Tkinter — интерфейс в стиле Windows 11
Листинги 2.1.2 + 2.1.3 + СРС 2.2

Запуск:  python cpc2.3.py
Опциональные зависимости:
    pip install tkinterweb
    pip install Pillow
"""

from tkinter import *
from tkinter import messagebox as mb
from tkinter import filedialog as fd
import time
import datetime as dt
import random


# =========================================================
#  ЦВЕТОВАЯ СХЕМА WINDOWS 11
# =========================================================
THEME = {
    "light": {
        "bg":           "#F3F3F3",
        "sidebar":      "#EAEAEA",
        "card":         "#FFFFFF",
        "card_hover":   "#E5F0FA",
        "text":         "#1F1F1F",
        "text_muted":   "#5C5C5C",
        "accent":       "#0067C0",
        "accent_hover": "#1975C5",
        "accent_text":  "#FFFFFF",
        "border":       "#D6D6D6",
    },
    "dark": {
        "bg":           "#202020",
        "sidebar":      "#2B2B2B",
        "card":         "#2D2D2D",
        "card_hover":   "#3A4A5A",
        "text":         "#F0F0F0",
        "text_muted":   "#A0A0A0",
        "accent":       "#4CC2FF",
        "accent_hover": "#66CBFF",
        "accent_text":  "#000000",
        "border":       "#3A3A3A",
    },
}

T = dict(THEME["light"])

FONT       = "Segoe UI"
FONT_TITLE = (FONT, 20, "bold")
FONT_BTN   = (FONT, 10)
FONT_CARD  = (FONT, 11)
FONT_BIG   = (FONT, 22, "bold")


def _error(message):
    mb.showerror("Ошибка", message)


# =========================================================
#  ХЕЛПЕРЫ
# =========================================================
def make_button(parent, text, command, primary=False):
    bg = T["accent"] if primary else T["card"]
    fg = T["accent_text"] if primary else T["text"]
    hover = T["accent_hover"] if primary else T["card_hover"]

    btn = Button(
        parent, text=text, command=command,
        font=FONT_BTN, bd=0, relief=FLAT,
        bg=bg, fg=fg, activebackground=hover, activeforeground=fg,
        padx=14, pady=6, cursor="hand2", highlightthickness=0,
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=hover))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn


def make_entry(parent, width=30):
    return Entry(
        parent, width=width, font=FONT_BTN, bd=1, relief=FLAT,
        bg=T["card"], fg=T["text"], insertbackground=T["text"],
        highlightthickness=1, highlightbackground=T["border"],
        highlightcolor=T["accent"],
    )


def new_window(title, geometry=None):
    win = Toplevel(root)
    win.title(title)
    win.configure(bg=T["bg"])
    if geometry:
        win.geometry(geometry)
    return win


def card_frame(parent, padding=16):
    f = Frame(parent, bg=T["card"], highlightthickness=1,
              highlightbackground=T["border"])
    f.pack(pady=6, padx=20, fill=X)
    inner = Frame(f, bg=T["card"])
    inner.pack(padx=padding, pady=padding, fill=BOTH, expand=True)
    return inner


# =========================================================
#  2.1.2-1. БРАУЗЕР
# =========================================================
def task_browser():
    try:
        import tkinterweb
    except ImportError:
        _error("Установите tkinterweb:\n  pip install tkinterweb")
        return

    win = new_window("2.1.2-1. Просмотр сайта", "900x650")

    bar = Frame(win, bg=T["bg"]); bar.pack(fill=X, padx=10, pady=8)
    Label(bar, text="Адрес:", font=FONT_BTN, bg=T["bg"], fg=T["text"]).pack(side=LEFT, padx=(0, 8))
    e = make_entry(bar, width=60); e.pack(side=LEFT, padx=(0, 8))

    def read():
        frame.load_website(e.get())

    make_button(bar, "Перейти", read, primary=True).pack(side=LEFT)

    frame = tkinterweb.HtmlFrame(win)
    frame.pack(fill="both", expand=1, padx=10, pady=(0, 10))
    frame.load_website("https://www.google.com")


# =========================================================
#  2.1.2-2. ДАТА И ВРЕМЯ
# =========================================================
def task_datetime():
    win = new_window("2.1.2-2. Дата и время", "420x180")
    c = card_frame(win)
    Label(c, text=time.strftime('%d %B %Y'),
          font=FONT_BIG, bg=T["card"], fg=T["text"]).pack()
    Label(c, text=time.strftime('%H:%M:%S'),
          font=(FONT, 16), bg=T["card"], fg=T["accent"]).pack(pady=(4, 0))


# =========================================================
#  2.1.2-3. ДАТА С РУССКИМ МЕСЯЦЕМ
# =========================================================
def task_date_ru():
    win = new_window("2.1.2-3. Дата на русском", "420x180")

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

    c = card_frame(win)
    Label(c, text=f"{Day} {Month} {Year}",
          font=FONT_BIG, bg=T["card"], fg=T["text"]).pack()


# =========================================================
#  2.1.2-4. ЧАСЫ
# =========================================================
def task_clock():
    win = new_window("2.1.2-4. Часы", "400x200")
    c = card_frame(win)
    m = Label(c, font=(FONT, 36, "bold"), bg=T["card"], fg=T["accent"])
    m.pack()

    def tick():
        m.config(text=time.strftime("%H:%M:%S"))
        m.after(1000, tick)

    tick()


# =========================================================
#  2.1.2-5. ДЕНЬ НЕДЕЛИ
# =========================================================
def task_weekday():
    win = new_window("2.1.2-5. Сегодня ...", "420x180")

    Day = time.strftime('%A')
    match Day:
        case "Monday":    Day = "понедельник"
        case "Tuesday":   Day = "вторник"
        case "Wednesday": Day = "среда"
        case "Thursday":  Day = "четверг"
        case "Friday":    Day = "пятница"
        case "Saturday":  Day = "суббота"
        case "Sunday":    Day = "воскресенье"

    c = card_frame(win)
    Label(c, text="Сегодня " + Day,
          font=FONT_BIG, bg=T["card"], fg=T["text"]).pack()


# =========================================================
#  2.1.2-6. НАПИТКИ
# =========================================================
def task_drinks():
    win = new_window("2.1.2-6. Любимый напиток", "400x260")
    c = card_frame(win)

    Label(c, text="Выбери любимый напиток:",
          font=FONT_CARD, bg=T["card"], fg=T["text"]).pack(anchor=W)

    drink = StringVar(value="Кофе")
    for label, value in (("Квас", "Квас"), ("Чай", "Чай"), ("Кофе", "Кофе")):
        Radiobutton(
            c, text=label, value=value, variable=drink,
            font=FONT_BTN, bg=T["card"], fg=T["text"],
            activebackground=T["card"], selectcolor=T["card"],
            bd=0, highlightthickness=0,
        ).pack(anchor=W, pady=2)

    Label(c, textvariable=drink,
          font=(FONT, 14, "bold"), bg=T["card"], fg=T["accent"]).pack(pady=(10, 0))


# =========================================================
#  2.1.2-7. ЧАСЫ С РАДИОКНОПКАМИ
# =========================================================
def task_clock_radio():
    win = new_window("2.1.2-7. Часы с режимами", "640x200")

    d = dt.datetime.now()
    Date = d.strftime('%d %B %Y')
    Time = d.strftime('%X')

    c = card_frame(win)
    m = Label(c, font=(FONT, 18, "bold"), bg=T["card"], fg=T["accent"],
              text=f"{Date} {Time}")
    m.pack(pady=10)

    bar = Frame(c, bg=T["card"]); bar.pack()
    var = IntVar(value=0)

    def show_datetime(): m.config(text=f"{Date} {Time}")
    def show_date():     m.config(text=Date)
    def show_time():     m.config(text=Time)
    def night():
        for w in (m, R1, R2, R3, R4):
            w.config(bg="#1A1A1A", fg="#E0E0E0")

    def rb(text, cmd, val):
        return Radiobutton(bar, text=text, command=cmd,
                           variable=var, value=val, font=FONT_BTN,
                           bg=T["card"], fg=T["text"],
                           activebackground=T["card"], selectcolor=T["card"],
                           bd=0, highlightthickness=0)

    R1 = rb("Дата и время", show_datetime, 0)
    R2 = rb("Дата",         show_date,     1)
    R3 = rb("Время",        show_time,     2)
    R4 = rb("Ночная тема",  night,         3)

    for r in (R1, R2, R3, R4):
        r.pack(side=LEFT, padx=6)


# =========================================================
#  2.1.2-8. ЧАСЫ С ФЛАЖКАМИ
# =========================================================
def task_clock_checks():
    win = new_window("2.1.2-8. Часы с флажками", "420x360")

    def tick():
        m.config(text=time.strftime("%H:%M:%S"))
        m.after(1000, tick)

    def bg_color(): m['bg']     = v1.get()
    def fg_color(): m['fg']     = v2.get()
    def size():     m['height'] = v4.get()

    c = card_frame(win)
    m = Label(c, font=(FONT, 16), bg="#DCE9F5", fg="#1F1F1F",
              width=20, height=2)
    m.pack(pady=10)

    v1 = StringVar(value='#DCE9F5')
    Checkbutton(c, text='Светлый / тёплый фон', variable=v1,
                onvalue='#F5DCC8', offvalue='#DCE9F5',
                command=bg_color, font=FONT_BTN,
                bg=T["card"], fg=T["text"], activebackground=T["card"],
                selectcolor=T["card"], bd=0, highlightthickness=0).pack(anchor=W)

    v2 = StringVar(value='#1F1F1F')
    Checkbutton(c, text='Тёмный / светлый текст', variable=v2,
                onvalue='#FFFFFF', offvalue='#1F1F1F',
                command=fg_color, font=FONT_BTN,
                bg=T["card"], fg=T["text"], activebackground=T["card"],
                selectcolor=T["card"], bd=0, highlightthickness=0).pack(anchor=W)

    v4 = IntVar(value=2)
    Checkbutton(c, text='Высота метки (2 ↔ 4)', variable=v4,
                onvalue=4, offvalue=2,
                command=size, font=FONT_BTN,
                bg=T["card"], fg=T["text"], activebackground=T["card"],
                selectcolor=T["card"], bd=0, highlightthickness=0).pack(anchor=W)

    tick()


# =========================================================
#  СРС 2.2-9. РИСОВАНИЕ ФИГУР
# =========================================================
def task_draw():
    win = new_window("СРС 2.2. Рисование фигур", "420x640")

    canvas = Canvas(win, width=340, height=220,
                    bg="#FADADD", highlightthickness=1,
                    highlightbackground=T["border"])
    canvas.pack(pady=12)

    def draw_circle():
        canvas.create_oval(70, 40, 210, 180,
                           fill=fill_entry.get(), outline=outline_entry.get(), width=2)
    def draw_square():
        canvas.create_rectangle(70, 40, 210, 180,
                                fill=fill_entry.get(), outline=outline_entry.get(), width=2)
    def draw_triangle():
        canvas.create_polygon([140, 30, 60, 190, 220, 190],
                              fill=fill_entry.get(), outline=outline_entry.get(), width=2)
    def clear_canvas():
        canvas.delete("all")
    def change_background():
        try:
            canvas.config(bg=bg_entry.get())
        except TclError:
            _error("Некорректный цвет: " + bg_entry.get())

    bar = Frame(win, bg=T["bg"]); bar.pack(pady=4)
    make_button(bar, "Окружность",  draw_circle).pack(side=LEFT, padx=3)
    make_button(bar, "Треугольник", draw_triangle).pack(side=LEFT, padx=3)
    make_button(bar, "Квадрат",     draw_square).pack(side=LEFT, padx=3)
    make_button(bar, "Очистить",    clear_canvas).pack(side=LEFT, padx=3)

    c = card_frame(win)
    Label(c, text="Цвет заливки:", font=FONT_BTN,
          bg=T["card"], fg=T["text"]).pack(anchor=W)
    fill_entry = make_entry(c, width=20); fill_entry.insert(0, "lightblue")
    fill_entry.pack(fill=X, pady=(2, 8))

    Label(c, text="Цвет обводки:", font=FONT_BTN,
          bg=T["card"], fg=T["text"]).pack(anchor=W)
    outline_entry = make_entry(c, width=20); outline_entry.insert(0, "blue")
    outline_entry.pack(fill=X, pady=(2, 8))

    Label(c, text="Цвет фона:", font=FONT_BTN,
          bg=T["card"], fg=T["text"]).pack(anchor=W)
    bg_entry = make_entry(c, width=20); bg_entry.insert(0, "white")
    bg_entry.pack(fill=X, pady=(2, 8))

    make_button(c, "Изменить цвет фона", change_background, primary=True).pack(pady=4)


# =========================================================
#  2.1.3-10. MESSAGEBOX
# =========================================================
def task_messagebox():
    win = new_window("2.1.3-10. Окна Messagebox", "360x300")
    c = card_frame(win)
    e = make_entry(c, width=40); e.pack(pady=6)

    def check_yesno():
        if mb.askyesno("Вопрос", "Перенести данные?"):
            s = e.get(); e.delete(0, END); m['text'] = s

    def check_okcancel():
        if mb.askokcancel("Вопрос", "Перенести данные?"):
            s = e.get(); e.delete(0, END); m['text'] = s

    def check_retrycancel():
        if mb.askretrycancel("Вопрос", "Перенести данные?"):
            s = e.get(); e.delete(0, END); m['text'] = s

    make_button(c, "askyesno",       check_yesno).pack(fill=X, pady=2)
    make_button(c, "askokcancel",    check_okcancel).pack(fill=X, pady=2)
    make_button(c, "askretrycancel", check_retrycancel).pack(fill=X, pady=2)

    m = Label(c, height=3, bg=T["card"], fg=T["accent"], font=(FONT, 12, "bold"))
    m.pack(fill=X, pady=(10, 0))


# =========================================================
#  2.1.3-11. УГАДАЙ ЧИСЛО
# =========================================================
def task_guess():
    win = new_window('2.1.3-11. Игра "Угадай число"', "420x240")
    c = card_frame(win)

    Label(c, text="Введи число, которое я загадал:",
          font=FONT_CARD, bg=T["card"], fg=T["text"]).pack()

    e = make_entry(c, width=20); e.pack(pady=8)

    def check():
        s = e.get()
        if not s.isdigit():
            mb.showerror("Ошибка", "Введите число")
            return
        rnd = random.randint(1, 2)
        if int(s) == rnd:
            mb.showinfo("Результат", "Угадал!")
        else:
            mb.showinfo("Результат", f"Неудача :(\nБыло загадано: {rnd}")
        if mb.askretrycancel("Вопрос", "Загадать еще одно число?"):
            e.delete(0, END)
        else:
            win.destroy()

    make_button(c, "Проверить", check, primary=True).pack()


# =========================================================
#  2.1.3-12. КАЛЬКУЛЯТОР (3 числа, дроби)
# =========================================================
def task_calc3():
    win = new_window("2.1.3-12. Калькулятор", "420x420")

    def validate_float(new_value):
        if new_value in ("", "-", ".", "-.", ","):
            return True
        try:
            float(new_value.replace(",", "."))
            return True
        except ValueError:
            return False

    vcmd = (win.register(validate_float), "%P")

    c = card_frame(win)
    Label(c, text="Введите три числа (целые или дробные):",
          font=FONT_CARD, bg=T["card"], fg=T["text"]).pack(anchor=W)

    e1 = make_entry(c, width=30); e1.config(validate="key", validatecommand=vcmd); e1.pack(pady=4)
    e2 = make_entry(c, width=30); e2.config(validate="key", validatecommand=vcmd); e2.pack(pady=4)
    e3 = make_entry(c, width=30); e3.config(validate="key", validatecommand=vcmd); e3.pack(pady=4)

    def summ():
        values = []
        for i, entry in enumerate((e1, e2, e3), start=1):
            s = entry.get().replace(",", ".")
            if s in ("", "-", ".", "-."):
                mb.showerror("Ошибка", f"В поле {i} введите число")
                return
            try:
                values.append(float(s))
            except ValueError:
                mb.showerror("Ошибка", f"В поле {i} должно быть число")
                return

        def fmt(x):
            return str(int(x)) if x == int(x) else str(x)

        s1, s2, s3 = (fmt(v) for v in values)
        total = sum(values)
        m1['text'] = f"{s1} + {s2} + {s3} = {fmt(total)}"

        if mb.askretrycancel("Вопрос", "Сложить еще три числа?"):
            for entry in (e1, e2, e3):
                entry.delete(0, END)
            m1['text'] = ""
        else:
            win.destroy()

    make_button(c, "Сложить три числа", summ, primary=True).pack(pady=8)

    m1 = Label(c, height=3, bg=T["card"], fg=T["accent"], font=(FONT, 13, "bold"))
    m1.pack(fill=X)


# =========================================================
#  2.1.3-13. ОКНО В ЦЕНТРЕ ЭКРАНА
# =========================================================
def task_main_window():
    win = Toplevel(root)
    win.title("2.1.3-13. Окно в центре экрана")
    win.configure(bg=T["bg"])

    w = win.winfo_screenwidth()
    h = win.winfo_screenheight()
    w2 = w // 2 - 200
    h2 = h // 2 - 150
    win.geometry(f"400x300+{w2}+{h2}")

    c = card_frame(win)
    Label(c, text="Окно расположено\nв центре экрана",
          font=FONT_TITLE, bg=T["card"], fg=T["text"],
          justify=CENTER).pack(pady=10)
    Label(c, text=f"Экран: {w} × {h}\nОкно: 400 × 300\nПозиция: +{w2} +{h2}",
          font=FONT_BTN, bg=T["card"], fg=T["text_muted"],
          justify=CENTER).pack()


# =========================================================
#  2.1.3-14. БЛОКНОТ
# =========================================================
def task_notepad():
    win = new_window("2.1.3-14. Блокнот", "640x480")

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

    bar = Frame(win, bg=T["sidebar"]); bar.pack(fill=X)
    make_button(bar, "Открыть",  open_file).pack(side=LEFT, padx=4, pady=6)
    make_button(bar, "Новый",    delete).pack(side=LEFT, padx=4, pady=6)
    make_button(bar, "Очистить", delete).pack(side=LEFT, padx=4, pady=6)
    make_button(bar, "Сохранить", save, primary=True).pack(side=LEFT, padx=4, pady=6)
    make_button(bar, "Закрыть",  close_app).pack(side=RIGHT, padx=4, pady=6)

    wrap = Frame(win, bg=T["bg"]); wrap.pack(fill=BOTH, expand=1, padx=10, pady=10)
    text = Text(wrap, width=40, height=15, wrap=WORD,
                font=(FONT, 11), bd=0, relief=FLAT,
                bg=T["card"], fg=T["text"], insertbackground=T["text"],
                padx=10, pady=10)
    text.pack(side=LEFT, fill=BOTH, expand=1)

    scroll = Scrollbar(wrap, command=text.yview)
    scroll.pack(side=LEFT, fill=Y)
    text.config(yscrollcommand=scroll.set)


# =========================================================
#  2.1.3-15. ПРОСМОТР ИЗОБРАЖЕНИЙ
# =========================================================
def task_photo():
    try:
        from PIL import Image, ImageTk
    except ImportError:
        _error("Установите Pillow:\n  pip install Pillow")
        return

    win = new_window("2.1.3-15. Просмотр изображений", "600x600")

    holder = Frame(win, bg=T["card"], highlightthickness=1,
                   highlightbackground=T["border"])
    holder.pack(fill=BOTH, expand=1, padx=10, pady=10)

    def open_image():
        try:
            file = fd.askopenfilename()
            if file:
                img = Image.open(file)
                img.thumbnail((550, 500))
                img_tk = ImageTk.PhotoImage(img)

                if hasattr(holder, 'photo_label'):
                    holder.photo_label.configure(image=img_tk)
                    holder.photo_label.image = img_tk
                else:
                    holder.photo_label = Label(holder, image=img_tk, bg=T["card"])
                    holder.photo_label.image = img_tk
                    holder.photo_label.pack(expand=True)
        except FileNotFoundError:
            mb.showerror("Ошибка", "Файл не найден")
        except OSError:
            mb.showerror("Ошибка", "Не удалось открыть файл,\nвозможно это не изображение")
        except Exception as e:
            mb.showerror("Ошибка", f"Произошла ошибка: {e}")

    bar = Frame(win, bg=T["sidebar"]); bar.pack(fill=X)
    make_button(bar, "Открыть...", open_image, primary=True).pack(side=LEFT, padx=6, pady=6)
    make_button(bar, "Закрыть", win.destroy).pack(side=RIGHT, padx=6, pady=6)


# =========================================================
#  ГЛАВНОЕ ОКНО
# =========================================================
root = Tk()
root.title("Практикум Tkinter — Windows 11 style")
root.geometry("900x600")
root.minsize(760, 520)
root.configure(bg=T["bg"])


sidebar = Frame(root, bg=T["sidebar"], width=240)
sidebar.pack(side=LEFT, fill=Y)
sidebar.pack_propagate(False)

content = Frame(root, bg=T["bg"])
content.pack(side=LEFT, fill=BOTH, expand=1)


TASKS = [
    ("1. Просмотр сайта",         "2.1.2",   task_browser),
    ("2. Дата и время",           "2.1.2",   task_datetime),
    ("3. Дата на русском",        "2.1.2",   task_date_ru),
    ("4. Часы",                   "2.1.2",   task_clock),
    ("5. День недели",            "2.1.2",   task_weekday),
    ("6. Напитки",                "2.1.2",   task_drinks),
    ("7. Часы с радиокнопками",   "2.1.2",   task_clock_radio),
    ("8. Часы с флажками",        "2.1.2",   task_clock_checks),
    ("9. Рисование фигур",        "СРС 2.2", task_draw),
    ("10. Окна Messagebox",       "2.1.3",   task_messagebox),
    ("11. Игра «Угадай число»",   "2.1.3",   task_guess),
    ("12. Калькулятор (3 числа)", "2.1.3",   task_calc3),
    ("13. Окно в центре экрана",  "2.1.3",   task_main_window),
    ("14. Блокнот",               "2.1.3",   task_notepad),
    ("15. Просмотр изображений",  "2.1.3",   task_photo),
]


def _rebuild_all():
    """Очищает и заново строит боковую панель и карточки."""
    # --- Боковая панель ---
    for w in sidebar.winfo_children():
        w.destroy()

    Label(sidebar, text="Практикум Tkinter",
          font=(FONT, 14, "bold"), fg=T["accent"], bg=T["sidebar"]
          ).pack(pady=(18, 6), padx=16, anchor="w")

    Label(sidebar, text="2.1.2 · 2.1.3 · СРС 2.2",
          font=(FONT, 9), fg=T["text_muted"], bg=T["sidebar"]
          ).pack(padx=16, anchor="w")

    current_section = None
    for title, section, command in TASKS:
        if section != current_section:
            current_section = section
            Label(sidebar, text=section.upper(),
                  font=(FONT, 9, "bold"), fg=T["text_muted"], bg=T["sidebar"],
                  anchor="w", padx=16
                  ).pack(fill=X, pady=(14, 4))     # <-- pady у pack, а не у Label

        btn = Button(sidebar, text="  " + title, command=command,
                     font=(FONT, 10), bd=0, relief=FLAT, anchor="w",
                     bg=T["sidebar"], fg=T["text"],
                     activebackground=T["card_hover"],
                     activeforeground=T["text"],
                     padx=16, pady=8, cursor="hand2",
                     highlightthickness=0)
        btn.pack(fill=X)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg=T["card_hover"]))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=T["sidebar"]))

    # --- Правая область ---
    for w in content.winfo_children():
        w.destroy()

    Label(content, text="Задачи практикума",
          font=(FONT, 20, "bold"), fg=T["text"], bg=T["bg"]
          ).pack(anchor="w", padx=20, pady=(20, 4))
    Label(content, text="Выберите задачу — она откроется в отдельном окне",
          font=(FONT, 10), fg=T["text_muted"], bg=T["bg"]
          ).pack(anchor="w", padx=20, pady=(0, 10))

    for title, section, command in TASKS:
        card = Frame(content, bg=T["card"], highlightthickness=1,
                     highlightbackground=T["border"], cursor="hand2")
        card.pack(fill=X, padx=20, pady=6)

        accent = Frame(card, bg=T["accent"], width=4)
        accent.pack(side=LEFT, fill=Y)

        inner = Frame(card, bg=T["card"])
        inner.pack(side=LEFT, fill=X, expand=1, padx=16, pady=12)

        Label(inner, text=title, font=(FONT, 12, "bold"),
              fg=T["text"], bg=T["card"], anchor="w").pack(anchor="w")
        Label(inner, text=f"Раздел {section}", font=(FONT, 9),
              fg=T["text_muted"], bg=T["card"], anchor="w").pack(anchor="w")

        def click(e=None, cmd=command): cmd()
        for w in (card, inner, *inner.winfo_children(), accent):
            w.bind("<Button-1>", click)


_rebuild_all()
root.mainloop()