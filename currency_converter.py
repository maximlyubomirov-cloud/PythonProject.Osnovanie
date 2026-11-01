from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import requests
import json


def center_window(window, width, height):
    """Центрирует окно заданного размера по центру экрана."""
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def show_centered_info(title, message):
    """Показывает информационное окно, отцентрованное по высоте."""
    win = Toplevel(root)
    win.title(title)
    win.resizable(False, False)

    Label(win, text=message, justify="center", padx=20, pady=20).pack(expand=True)
    Button(win, text="OK", width=10, command=win.destroy).pack(pady=(0, 15))

    win.update_idletasks()
    w = win.winfo_reqwidth() + 40
    h = win.winfo_reqheight() + 20
    center_window(win, w, h)

    win.transient(root)
    win.grab_set()
    root.wait_window(win)


def update_currency_label(event):
    code = target_combobox.get()
    target_label.config(text=currencies[code])


def update_base_label(event):
    code = base_combobox.get()
    base_label.config(text=currencies[code])


def update_base_label_2(event):
    code = base_combobox_2.get()
    base_label_2.config(text=currencies[code])


def get_rate(base_code, target_code):
    """Запрашивает JSON с курсом base_code -> target_code."""
    response = requests.get(
        f"https://open.er-api.com/v6/latest/{base_code}", timeout=10
    )
    response.raise_for_status()
    data = response.json()
    if target_code not in data["rates"]:
        raise ValueError(f"Курс для {target_code} не найден")
    return data["rates"][target_code]


def exchange():
    target_code = target_combobox.get()
    base_code_1 = base_combobox.get()
    base_code_2 = base_combobox_2.get()

    if not target_code or not base_code_1 or not base_code_2:
        mb.showwarning("Внимание", "Выберите все валюты")
        return

    try:
        rate_1 = get_rate(base_code_1, target_code)
        rate_2 = get_rate(base_code_2, target_code)

        result = (
            f"Целевая валюта: {target_code} ({currencies[target_code]})\n\n"
            f"1 {base_code_1} ({currencies[base_code_1]}) = "
            f"{rate_1:.4f} {target_code}\n"
            f"1 {base_code_2} ({currencies[base_code_2]}) = "
            f"{rate_2:.4f} {target_code}"
        )
        show_centered_info("Курсы обмена", result)
    except requests.RequestException as e:
        mb.showerror("Ошибка сети", f"Не удалось получить данные: {e}")
    except ValueError as e:
        mb.showerror("Ошибка данных", str(e))


currencies = {
    "USD": "Доллар США",
    "EUR": "Евро",
    "GBP": "Фунт стерлингов",
    "JPY": "Японская йена",
    "CNY": "Китайский юань",
    "RUB": "Российский рубль",
    "KZT": "Казахстанский тенге",
    "BYN": "Белорусский рубль",
}

root = Tk()
root.title("Конвертер валют (две базовые валюты)")
center_window(root, 420, 460)

container = Frame(root)
container.place(relx=0.5, rely=0.5, anchor="center")   # центрирование по высоте

Label(container, text="Первая базовая валюта:").pack(pady=5)
base_combobox = ttk.Combobox(container, values=list(currencies.keys()), state="readonly")
base_combobox.pack()
base_combobox.bind("<<ComboboxSelected>>", update_base_label)
base_combobox.set("USD")

base_label = Label(container, text=currencies["USD"])
base_label.pack()

Label(container, text="Вторая базовая валюта:").pack(pady=5)
base_combobox_2 = ttk.Combobox(container, values=list(currencies.keys()), state="readonly")
base_combobox_2.pack()
base_combobox_2.bind("<<ComboboxSelected>>", update_base_label_2)
base_combobox_2.set("EUR")

base_label_2 = Label(container, text=currencies["EUR"])
base_label_2.pack()

Label(container, text="Целевая валюта:").pack(pady=5)
target_combobox = ttk.Combobox(container, values=list(currencies.keys()), state="readonly")
target_combobox.pack()
target_combobox.bind("<<ComboboxSelected>>", update_currency_label)
target_combobox.set("RUB")

target_label = Label(container, text=currencies["RUB"])
target_label.pack()

Button(container, text="Получить курсы", command=exchange).pack(pady=20)

root.mainloop()