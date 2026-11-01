from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime, timezone, timedelta
import requests


MSK = timezone(timedelta(hours=3))

# ---- Metro UI палитра ----
BG = "#FAFAFA"
FG = "#212121"
ACCENT = "#0078D7"
ACCENT_DARK = "#005A9E"
DATA_BG = "#000000"
DATA_FG = "#00FF00"
FONT_UI = ("Segoe UI", 10)
FONT_DATA = ("Consolas", 10, "bold")


# ---------- Вспомогательные функции ----------

def center_window(window, width, height):
    window.update_idletasks()
    sw = window.winfo_screenwidth()
    sh = window.winfo_screenheight()
    x = (sw - width) // 2
    y = (sh - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def position_near_parent(win, offset_x=40, offset_y=40):
    """Смещает окно относительно главного, чтобы не перекрывать его."""
    win.update_idletasks()
    root.update_idletasks()
    x = root.winfo_rootx() + offset_x
    y = root.winfo_rooty() + offset_y
    win.geometry(f"+{x}+{y}")


def parse_api_time(s):
    try:
        return datetime.strptime(s, "%a, %d %b %Y %H:%M:%S %z")
    except (TypeError, ValueError):
        return None


def to_msk(api_time_str):
    dt = parse_api_time(api_time_str)
    if not dt:
        return "—"
    return dt.astimezone(MSK).strftime("%d.%m.%Y %H:%M:%S МСК")


def format_rate(rate, target_code):
    return f"{rate:.2f}" if target_code == "JPY" else f"{rate:.4f}"


# ---------- Второе окно ----------

def make_data_box(parent, text):
    """«Окошко» с данными: чёрный фон, ярко-зелёный текст."""
    return Label(
        parent, text=text,
        bg=DATA_BG, fg=DATA_FG,
        font=FONT_DATA,
        padx=8, pady=2,
        relief="flat", borderwidth=0,
    )


def style_btn(b, primary=True):
    if primary:
        b.configure(bg=ACCENT, fg="white",
                    activebackground=ACCENT_DARK, activeforeground="white")
    else:
        b.configure(bg="#E0E0E0", fg=FG,
                    activebackground="#D0D0D0", activeforeground=FG)
    b.configure(relief="flat", borderwidth=0, padx=16, pady=6,
                font=FONT_UI, cursor="hand2")


def show_result_window(title, rows, raw_params=None):
    """rows — список кортежей (label, value, is_data).
    is_data=True → value выводится в «окошечке» (чёрный/зелёный).
    Окно фиксированного размера, все данные видны, окошки справа."""
    win = Toplevel(root)
    win.title(title)
    win.configure(bg=BG)
    win.resizable(False, False)

    body = Frame(win, bg=BG)
    body.pack(fill="both", expand=True, padx=16, pady=16)

    body.columnconfigure(0, weight=1)   # подписи
    body.columnconfigure(1, weight=0)   # окошки — по содержимому

    r = 0
    for label_text, value_text, is_data in rows:
        if label_text == "__header__":
            lbl = Label(body, text=value_text, bg=BG, fg=FG,
                        font=("Segoe UI", 11, "bold"))
            lbl.grid(row=r, column=0, columnspan=2, sticky="w", pady=(8, 4))
            r += 1
            continue

        if label_text == "__sep__":
            Frame(body, height=1, bg="#E0E0E0").grid(
                row=r, column=0, columnspan=2, sticky="ew", pady=6)
            r += 1
            continue

        lbl = Label(body, text=label_text, bg=BG, fg=FG, font=FONT_UI)
        lbl.grid(row=r, column=0, sticky="w", padx=(0, 12), pady=2)

        if is_data:
            box = make_data_box(body, value_text)
            box.grid(row=r, column=1, sticky="e", pady=2)
        else:
            val = Label(body, text=value_text, bg=BG, fg=FG, font=FONT_UI)
            val.grid(row=r, column=1, sticky="e", pady=2)
        r += 1

    # Кнопки — сразу под содержимым, отступ ≤ 2 строк
    btn_frame = Frame(win, bg=BG)
    btn_frame.pack(fill="x", padx=16, pady=(0, 12))

    # Плоский текст для буфера/файла
    def plain_text():
        lines = []
        for label_text, value_text, _ in rows:
            if label_text == "__header__":
                lines.append(value_text)
            elif label_text == "__sep__":
                lines.append("")
            else:
                lines.append(f"{label_text}: {value_text}")
        return "\n".join(lines)

    def copy_to_clipboard():
        win.clipboard_clear()
        win.clipboard_append(plain_text())
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
                f.write(plain_text())
                if raw_params:
                    f.write("\n\n--- Параметры запроса ---\n")
                    for k, v in raw_params.items():
                        f.write(f"{k}: {v}\n")
            mb.showinfo("Сохранено", f"Файл сохранён:\n{path}", parent=win)
        except OSError as e:
            mb.showerror("Ошибка", f"Не удалось сохранить файл: {e}", parent=win)

    b_copy = Button(btn_frame, text="Копировать", command=copy_to_clipboard)
    style_btn(b_copy, primary=True)
    b_copy.pack(side="left", padx=(0, 8))

    b_save = Button(btn_frame, text="Сохранить в файл", command=save_to_file)
    style_btn(b_save, primary=True)
    b_save.pack(side="left")

    b_close = Button(btn_frame, text="Закрыть", command=win.destroy)
    style_btn(b_close, primary=False)
    b_close.pack(side="right")

    # Фиксированный размер ровно под содержимое + смещение от главного
    win.update_idletasks()
    w = win.winfo_reqwidth()
    h = win.winfo_reqheight()
    win.geometry(f"{w}x{h}")
    position_near_parent(win, offset_x=40, offset_y=40)

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

        v1 = format_rate(rate_1, target_code)
        v2 = format_rate(rate_2, target_code)
        upd_msk = to_msk(upd_1)

        # Строки: (label, value, is_data)
        rows = [
            ("__header__", "Котировки (Base/Quote)", False),

            (f"{base_code_1}/{target_code}", v1, True),
            ("", f"{currencies[base_code_1]} → {currencies[target_code]}", False),

            (f"{base_code_2}/{target_code}", v2, True),
            ("", f"{currencies[base_code_2]} → {currencies[target_code]}", False),

            ("__sep__", "", False),
            ("__header__", "Время", False),

            ("Время получения (локальное)", now_local, True),
            ("Время получения (МСК)", now_msk, True),
            ("Последнее обновление (UTC)", upd_1 or "—", True),
            ("Последнее обновление (МСК)", upd_msk, True),
            ("Актуальность", freshness, False),

            ("__sep__", "", False),
            ("Источник", "open.er-api.com (ExchangeRate-API)", False),
            ("Примечание", "API отдаёт средний курс (middle); Bid/Ask недоступны", False),
        ]

        raw_params = {
            "Дата и время запроса (локальное)": now_local,
            "Дата и время запроса (МСК)": now_msk,
            "Первая базовая валюта": f"{base_code_1} ({currencies[base_code_1]})",
            "Вторая базовая валюта": f"{base_code_2} ({currencies[base_code_2]})",
            "Целевая валюта": f"{target_code} ({currencies[target_code]})",
            f"Курс {base_code_1}/{target_code}": v1,
            f"Курс {base_code_2}/{target_code}": v2,
            "Последнее обновление (UTC)": upd_1 or "—",
            "Последнее обновление (МСК)": upd_msk,
            "Следующее обновление (UTC)": next_1 or "—",
            "Актуальность": freshness,
            "Источник": "open.er-api.com (ExchangeRate-API)",
            "URL запроса 1": f"https://open.er-api.com/v6/latest/{base_code_1}",
            "URL запроса 2": f"https://open.er-api.com/v6/latest/{base_code_2}",
        }

        show_result_window("Курсы обмена", rows, raw_params=raw_params)
    except requests.RequestException as e:
        mb.showerror("Ошибка сети", f"Не удалось получить данные: {e}")
    except ValueError as e:
        mb.showerror("Ошибка данных", str(e))


# ---------- Справочники ----------

currencies = {
    "USD": "Доллар США", "EUR": "Евро", "GBP": "Фунт стерлингов",
    "JPY": "Японская йена", "CNY": "Китайский юань", "RUB": "Российский рубль",
    "KZT": "Казахстанский тенге", "BYN": "Белорусский рубль",
    "AUD": "Австралийский доллар", "NZD": "Новозеландский доллар",
}

currency_symbols = {
    "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥", "CNY": "¥",
    "RUB": "₽", "KZT": "₸", "BYN": "Br", "AUD": "A$", "NZD": "NZ$",
}


# ---------- Главное окно (Metro UI) ----------

root = Tk()
root.title("Конвертер валют")
root.configure(bg=BG)
center_window(root, 360, 380)

container = Frame(root, bg=BG)
container.place(relx=0.5, rely=0.5, anchor="center")

def metro_label(text, small=False):
    return Label(container, text=text, bg=BG, fg=FG,
                 font=("Segoe UI", 9) if small else FONT_UI)

def metro_button(parent, text, command, primary=True):
    b = Button(parent, text=text, command=command)
    style_btn(b, primary=primary)
    return b

metro_label("Первая базовая валюта:").pack(pady=1)
base_combobox = ttk.Combobox(container, values=list(currencies.keys()), state="readonly")
base_combobox.pack()
base_combobox.bind("<<ComboboxSelected>>", update_base_label)
base_combobox.set("USD")
base_label = metro_label(f"{currencies['USD']} {currency_symbols['USD']}", small=True)
base_label.pack()

metro_label("Вторая базовая валюта:").pack(pady=1)
base_combobox_2 = ttk.Combobox(container, values=list(currencies.keys()), state="readonly")
base_combobox_2.pack()
base_combobox_2.bind("<<ComboboxSelected>>", update_base_label_2)
base_combobox_2.set("EUR")
base_label_2 = metro_label(f"{currencies['EUR']} {currency_symbols['EUR']}", small=True)
base_label_2.pack()

metro_label("Целевая валюта:").pack(pady=1)
target_combobox = ttk.Combobox(container, values=list(currencies.keys()), state="readonly")
target_combobox.pack()
target_combobox.bind("<<ComboboxSelected>>", update_currency_label)
target_combobox.set("RUB")
target_label = metro_label(f"{currencies['RUB']} {currency_symbols['RUB']}", small=True)
target_label.pack()

metro_button(container, "Получить курсы", exchange, primary=True).pack(pady=8)
metro_label("Источник: open.er-api.com", small=True).pack(pady=(0, 4))

root.mainloop()