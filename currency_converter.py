from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime, timezone, timedelta
import requests
import json


MSK = timezone(timedelta(hours=3))   # московское время (UTC+3)


# ---------- Вспомогательные функции ----------

def center_window(window, width, height):
    """Центрирует окно заданного размера по центру экрана."""
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def parse_api_time(s):
    """Парсит 'Mon, 03 Nov 2025 00:02:31 +0000' в datetime (UTC)."""
    try:
        return datetime.strptime(s, "%a, %d %b %Y %H:%M:%S %z")
    except (TypeError, ValueError):
        return None


def to_msk(api_time_str):
    """Переводит UTC-время из API в строку по МСК."""
    dt = parse_api_time(api_time_str)
    if not dt:
        return "—"
    return dt.astimezone(MSK).strftime("%d.%m.%Y %H:%M:%S МСК")


def format_rate(rate, target_code):
    """Биржевая точность: 4 знака, для JPY — 2 знака."""
    if target_code == "JPY":
        return f"{rate:.2f}"
    return f"{rate:.4f}"


def show_centered_info(title, message, raw_params=None):
    """Чёрное окно с зелёным текстом, копированием и сохранением в файл."""
    win = Toplevel(root)
    win.title(title)
    win.configure(bg="black")
    win.resizable(True, True)

    text = Text(win, wrap="none", bg="black", fg="#00FF00",
                insertbackground="#00FF00", font=("Consolas", 10),
                padx=10, pady=10, relief="flat", borderwidth=0)
    text.pack(fill="both", expand=True, padx=10, pady=(10, 0))
    text.insert("1.0", message)
    text.config(state="disabled")   # только чтение, но выделять/копировать можно

    btn_frame = Frame(win, bg="black")
    btn_frame.pack(fill="x", pady=8, padx=10)

    def copy_to_clipboard():
        win.clipboard_clear()
        win.clipboard_append(message)
        mb.showinfo("Скопировано", "Текст скопирован в буфер обмена", parent=win)

    def save_to_file():
        path = filedialog.asksaveasfilename(
            parent=win,
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")],
            initialfile="currency_rates.txt",
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(message)
                if raw_params:
                    f.write("\n\n--- Параметры запроса ---\n")
                    for k, v in raw_params.items():
                        f.write(f"{k}: {v}\n")
            mb.showinfo("Сохранено", f"Файл сохранён:\n{path}", parent=win)
        except OSError as e:
            mb.showerror("Ошибка", f"Не удалось сохранить файл: {e}", parent=win)

    Button(btn_frame, text="Копировать", command=copy_to_clipboard,
           bg="#111", fg="#00FF00", activebackground="#222",
           activeforeground="#00FF00").pack(side="left", padx=(0, 8))
    Button(btn_frame, text="Сохранить в файл", command=save_to_file,
           bg="#111", fg="#00FF00", activebackground="#222",
           activeforeground="#00FF00").pack(side="left")
    Button(btn_frame, text="Закрыть", command=win.destroy,
           bg="#111", fg="#00FF00", activebackground="#222",
           activeforeground="#00FF00").pack(side="right")

    win.update_idletasks()
    w = max(560, win.winfo_reqwidth())
    h = max(360, win.winfo_reqheight())
    center_window(win, w, h)

    win.transient(root)
    win.grab_set()
    root.wait_window(win)


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
        now_msk = datetime.now(MSK).strftime("%d.%m.%Y %H:%M:%S МСК")

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
            f"Время получения (локальное): {now_local}\n"
            f"Время получения (МСК):       {now_msk}\n"
            f"Последнее обновление на сервере (UTC): {upd_1 or '—'}\n"
            f"  → по московскому времени: {to_msk(upd_1)}\n"
            f"{freshness}\n\n"
            f"Источник курсов: open.er-api.com (ExchangeRate-API)\n"
            f"API отдаёт средний курс (middle); Bid/Ask недоступны."
        )

        raw_params = {
            "Дата и время запроса (локальное)": now_local,
            "Дата и время запроса (МСК)": now_msk,
            "Первая базовая валюта": f"{base_code_1} ({currencies[base_code_1]})",
            "Вторая базовая валюта": f"{base_code_2} ({currencies[base_code_2]})",
            "Целевая валюта": f"{target_code} ({currencies[target_code]})",
            f"Курс {base_code_1}/{target_code}": format_rate(rate_1, target_code),
            f"Курс {base_code_2}/{target_code}": format_rate(rate_2, target_code),
            "Последнее обновление (UTC)": upd_1 or "—",
            "Последнее обновление (МСК)": to_msk(upd_1),
            "Следующее обновление (UTC)": next_1 or "—",
            "Актуальность": freshness,
            "Источник": "open.er-api.com (ExchangeRate-API)",
            "URL запроса 1": f"https://open.er-api.com/v6/latest/{base_code_1}",
            "URL запроса 2": f"https://open.er-api.com/v6/latest/{base_code_2}",
        }

        show_centered_info("Курсы обмена", result, raw_params=raw_params)
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
center_window(root, 360, 380)   # окно уменьшено (~−15% по площади)

container = Frame(root)
container.place(relx=0.5, rely=0.5, anchor="center")   # центрирование по высоте

# Первая базовая валюта
Label(container, text="Первая базовая валюта:").pack(pady=1)
base_combobox = ttk.Combobox(container, values=list(currencies.keys()), state="readonly")
base_combobox.pack()
base_combobox.bind("<<ComboboxSelected>>", update_base_label)
base_combobox.set("USD")
base_label = Label(container, text=f"{currencies['USD']} {currency_symbols['USD']}")
base_label.pack()

# Вторая базовая валюта
Label(container, text="Вторая базовая валюта:").pack(pady=1)
base_combobox_2 = ttk.Combobox(container, values=list(currencies.keys()), state="readonly")
base_combobox_2.pack()
base_combobox_2.bind("<<ComboboxSelected>>", update_base_label_2)
base_combobox_2.set("EUR")
base_label_2 = Label(container, text=f"{currencies['EUR']} {currency_symbols['EUR']}")
base_label_2.pack()

# Целевая валюта
Label(container, text="Целевая валюта:").pack(pady=1)
target_combobox = ttk.Combobox(container, values=list(currencies.keys()), state="readonly")
target_combobox.pack()
target_combobox.bind("<<ComboboxSelected>>", update_currency_label)
target_combobox.set("RUB")
target_label = Label(container, text=f"{currencies['RUB']} {currency_symbols['RUB']}")
target_label.pack()

Button(container, text="Получить курсы", command=exchange).pack(pady=8)

# Источник курсов внизу окна
Label(container, text="Источник: open.er-api.com", font=("Arial", 8), fg="gray").pack(pady=(0, 4))

root.mainloop()