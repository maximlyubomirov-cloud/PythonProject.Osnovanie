from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import requests
import json


def update_currency_label(event):
    code = target_combobox.get()
    target_label.config(text=currencies[code])


def update_base_label(event):
    code = base_combobox.get()
    base_label.config(text=currencies[code])


def exchange():
    target_code = target_combobox.get()
    base_code = base_combobox.get()

    if not target_code or not base_code:
        mb.showwarning("Внимание", "Выберите коды валют")
        return

    try:
        response = requests.get(f"https://open.er-api.com/v6/latest/{base_code}")
        response.raise_for_status()
        data = response.json()

        if target_code in data["rates"]:
            rate = data["rates"][target_code]
            mb.showinfo("Курс обмена", f"1 {base_code} = {rate:.2f} {target_code}")
        else:
            mb.showerror("Ошибка", f"Курс для {target_code} не найден")
    except Exception as e:
        mb.showerror("Ошибка", f"Не удалось получить данные: {e}")


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
root.title("Конвертер валют")
root.geometry("400x300")

Label(root, text="Базовая валюта:").pack(pady=5)
base_combobox = ttk.Combobox(root, values=list(currencies.keys()), state="readonly")
base_combobox.pack()
base_combobox.bind("<<ComboboxSelected>>", update_base_label)
base_combobox.set("USD")

base_label = Label(root, text=currencies["USD"])
base_label.pack()

Label(root, text="Целевая валюта:").pack(pady=5)
target_combobox = ttk.Combobox(root, values=list(currencies.keys()), state="readonly")
target_combobox.pack()
target_combobox.bind("<<ComboboxSelected>>", update_currency_label)
target_combobox.set("EUR")

target_label = Label(root, text=currencies["EUR"])
target_label.pack()

Button(root, text="Получить курс", command=exchange).pack(pady=20)

root.mainloop()