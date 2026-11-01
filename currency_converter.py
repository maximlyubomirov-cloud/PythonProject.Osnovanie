from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
from datetime import datetime, timezone
import requests
import json


# ---------- Вспомогательные функции ----------

def center_window(window, width, height):
    """Центрирует окно заданного размера по центру экрана."""
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def show_centered_info(title, message):
    """Информационное окно, отцентрированное по высоте."""
    win = Toplevel(root)
    win.title(title)
    win.resizable(False, False)

    Label(win, text=message, justify="center", padx=10, pady=10).pack(expand=True)
    Button(win, text="OK", width=10, command=win.destroy).pack(pady=(0, 10))

    win.update_idletasks()
    w = win.winfo_reqwidth() + 20
    h = win.winfo_reqheight() + 10
    center_window(win, w, h)

    win.transient(root)
    win.grab_set()
    root.wait_window(win)


def parse_api_time(s):
    """Парсит 'Mon, 03 Nov 2025 00:02:31 +0000' в datetime (UTC)."""
    try:
        return datetime.strptime(s, "%a, %d %b %Y %H:%M:%S %z")
    except (TypeError, ValueError):
        return None


def format_rate(rate, target_code):
    """Биржевая точность: 4 знака, для JPY — 2 знака."""
    if target_code == "JPY":
        return f"{rate:.2f}"
    return f"{rate:.4f}"


# ---------- Обработчики интерфейса ----------

def update_currency_label(event):
    code = target_combobox.get()
    target_label.config(text=f"{currencies[code]} {currency_symbols.get(code, '')}")


def update_base_label(event):
    code = base_combobox.get()
    base_label.config(text=f"{currencies[code]} {currency_symbols.get(code, '')}")


def update_base_label_2(event):
    code = base_combobox_2.get()
    base_label_2.config(text=f"{currencies[code]} {currency_symbols.get(code, '')}")


# ---------- Работа с API ----------

def get_rate(base_code, target_code):
    """Запрашивает JSON с курсом base_code -> target_code.
    Возвращает (rate, last_update_utc, next_update_utc)."""
    response = requests.get(
        f"https://open.er-api.com/v6/latest/{base_code}", timeout=10
    )
    response.raise_for_status()
    data = response.json()

    if data.get("result") != "success":
        raise ValueError(f"API вернул ошибку: {data.get('error-type', 'unknown')}")

    if target_code not in data["rates"]:
        raise ValueError(f"Курс для {target_code} не найден")

    return (
        data["rates"][target_code],
        data.get("time_last_update_utc"),
        data.get("time_next_update_utc"),
    )


def exchange():
    target_code = target_combobox.get()
    base_code_1 = base_combobox.get()
    base_code_2 = base_combobox_2.get()

    if not target_code or not base_code_1 or not base_code_2:
        mb.showwarning("Внимание", "Выберите все валюты")
        return

    try:
        rate_1, upd_1, next_1 = get_rate(base_code_1, target_code)
        rate_2, upd_2, next_2 = get_rate(base_code_2, target_code)

        now_local = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        # Проверка актуальности: данные не старше 24 часов
        upd_dt = parse_api_time(upd_1)
        if upd_dt:
            age = datetime.now(timezone.utc) - upd_dt
            hours = age.total_seconds() / 3600
            if hours <= 24:
                freshness = f"Данные актуальны (обновлены {hours:.1f} ч назад)"
            else:
                freshness = f"⚠ Данные устарели (обновлены {hours:.1f} ч назад)"
        else:
            freshness = "Время обновления не указано API"

        # Биржевой формат: BASE/QUOTE, Middle rate, точность по инструменту
        result = (
            f"Котировки (Base/Quote):\n"
            f"{base_code_1}/{target_code}: {format_rate(rate_1, target_code)} (Middle)\n"
            f"    {currencies[base_code_1]} → {currencies[target_code]}\n\n"
            f"{base_code_2}/{target_code}: {format_rate(rate_2, target_code)} (Middle)\n"
            f"    {currencies[base_code_2]} → {currencies[target_code]}\n\n"
            f"Время получения: {now_local}\n"
            f"Последнее обновление на сервере: {upd_1 or '—'}\n"
            f"{freshness}\n\n"
            f"Источник курсов: open.er-api.com (ExchangeRate-API)\n"
            f"API отдаёт средний курс (middle); Bid/Ask недоступны."
        )
        show_centered_info("Курсы обмена", result)
    except requests.RequestException as e:
        mb.showerror("Ошибка сети", f"Не удалось получить данные: {e}")
    except ValueError as e:
        mb.showerror("Ошибка данных", str(e))


# ---------- Справочники ----------

currencies = {
    "USD": "Доллар США",
    "EUR": "Евро",
    "GBP": "Фунт стерлингов",
    "JPY": "Японская йена",
    "CNY": "Китайский юань",
    "RUB": "Российский рубль",
    "KZT": "Казахстанский тенге",
    "BYN": "Белорусский рубль",
    "AUD": "Австралийский доллар",
    "NZD": "Новозеландский доллар",
}

currency_symbols = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "CNY": "¥",
    "RUB": "₽",
    "KZT": "₸",
    "BYN": "Br",
    "AUD": "A$",
    "NZD": "NZ$",
}


# ---------- Интерфейс ----------

root = Tk()
root.title("Конвертер валют (две базовые валюты)")
center_window(root, 400, 420)

container = Frame(root)
container.place(relx=0.5, rely=0.5, anchor="center")   # центрирование по высоте

# Первая базовая валюта
Label(container, text="Первая базовая валюта:").pack(pady=2)
base_combobox = ttk.Combobox(container, values=list(currencies.keys()), state="readonly")
base_combobox.pack()
base_combobox.bind("<<ComboboxSelected>>", update_base_label)
base_combobox.set("USD")
base_label = Label(container, text=f"{currencies['USD']} {currency_symbols['USD']}")
base_label.pack()

# Вторая базовая валюта
Label(container, text="Вторая базовая валюта:").pack(pady=2)
base_combobox_2 = ttk.Combobox(container, values=list(currencies.keys()), state="readonly")
base_combobox_2.pack()
base_combobox_2.bind("<<ComboboxSelected>>", update_base_label_2)
base_combobox_2.set("EUR")
base_label_2 = Label(container, text=f"{currencies['EUR']} {currency_symbols['EUR']}")
base_label_2.pack()

# Целевая валюта
Label(container, text="Целевая валюта:").pack(pady=2)
target_combobox = ttk.Combobox(container, values=list(currencies.keys()), state="readonly")
target_combobox.pack()
target_combobox.bind("<<ComboboxSelected>>", update_currency_label)
target_combobox.set("RUB")
target_label = Label(container, text=f"{currencies['RUB']} {currency_symbols['RUB']}")
target_label.pack()

Button(container, text="Получить курсы", command=exchange).pack(pady=10)

# Источник курсов внизу окна
Label(container, text="Источник: open.er-api.com", font=("Arial", 8), fg="gray").pack(pady=(0, 5))

root.mainloop()