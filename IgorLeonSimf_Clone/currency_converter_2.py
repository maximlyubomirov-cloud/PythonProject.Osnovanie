# currency_converter.py — итоговая версия
from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import requests


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
        f"https://open.er-api.com/v6/latest/{base_code}",
        timeout=10
    )
    response.raise_for_status()
    data = response.json()               # данные в формате JSON
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
        # Запрашиваем курсы для ОБЕИХ базовых валют
        rate_1 = get_rate(base_code_1, target_code)
        rate_2 = get_rate(base_code_2, target_code)

        result = (
            f"Целевая валюта: {target_code} ({currencies[target_code]})\n\n"
            f"1 {base_code_1} ({currencies[base_code_1]}) = "
            f"{rate_1:.4f} {target_code}\n"
            f"1 {base_code_2} ({currencies[base_code_2]}) = "
            f"{rate_2:.4f} {target_code}"
        )
        mb.showinfo("Курсы обмена", result)
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
root.geometry("420x420")

# --- Первая базовая валюта ---
Label(root, text="Первая базовая валюта:").pack(pady=5)
base_combobox = ttk.Combobox(root, values=list(currencies.keys()), state="readonly")
base_combobox.pack()
base_combobox.bind("<<ComboboxSelected>>", update_base_label)
base_combobox.set("USD")
base_label = Label(root, text=currencies["USD"])
base_label.pack()

# --- Вторая базовая валюта ---
Label(root, text="Вторая базовая валюта:").pack(pady=5)
base_combobox_2 = ttk.Combobox(root, values=list(currencies.keys()), state="readonly")
base_combobox_2.pack()
base_combobox_2.bind("<<ComboboxSelected>>", update_base_label_2)
base_combobox_2.set("EUR")
base_label_2 = Label(root, text=currencies["EUR"])
base_label_2.pack()

# --- Целевая валюта ---
Label(root, text="Целевая валюта:").pack(pady=5)
target_combobox = ttk.Combobox(root, values=list(currencies.keys()), state="readonly")
target_combobox.pack()
target_combobox.bind("<<ComboboxSelected>>", update_currency_label)
target_combobox.set("RUB")
target_label = Label(root, text=currencies["RUB"])
target_label.pack()

Button(root, text="Получить курсы", command=exchange).pack(pady=20)

root.mainloop()
