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
HEADER_BG = "#D0D0D0"       # темнее основного фона (верхняя панель)
HEADER_FG = "#111111"
DIVIDER = "#BDBDBD"
ACCENT = "#0078D7"
ACCENT_DARK = "#005A9E"
DATA_BG = "#000000"
DATA_FG = "#00FF00"
FONT_UI = ("Segoe UI", 10)
FONT_HEADER = ("Segoe UI", 12, "bold")
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


# ---------- Копирование значений ----------

def flash(widget):
    """Короткая подсветка окошка при копировании."""
    try:
        old = widget.cget("bg")
    except TclError:
        return
    widget.configure(bg="#003300")
    widget.after(300, lambda: widget.configure(bg=old))


def copy_value(value, widget):
    widget.clipboard_clear()
    widget.clipboard_append(value)
    flash(widget)


def attach_copy_menu(widget, value):
    """ПКМ → 'Копировать значение'; двойной клик — тоже копирует."""
    menu = Menu(widget, tearoff=0)
    menu.add_command(label="Копировать значение",
                     command=lambda: copy_value(value, widget))
    widget.bind("<Button-3>", lambda e: menu.tk_popup(e.x_root, e.y_root))
    widget.bind("<Double-Button-1>", lambda e: copy_value(value, widget))


# ---------- Второе окно ----------

def make_data_box(parent, text, copyable=True):
    """«Окошко» с данными: чёрный фон, ярко-зелёный текст."""
    box = Label(
        parent, text=text,
        bg=DATA_BG, fg=DATA_FG,
        font=FONT_DATA,
        padx=8, pady=2,
        relief="flat", borderwidth=0,
    )
    if copyable:
        attach_copy_menu(box, text)
    return box


def style_btn(b, primary=True):
    if primary:
        b.configure(bg=ACCENT, fg="white",
                    activebackground=ACCENT_DARK, activeforeground="white")
    else:
        b.configure(bg="#E0E0E0", fg=FG,
                    activebackground="#D0D0D0", activeforeground=FG)
    b.configure(relief="flat", borderwidth=0, padx=16, pady=6,
                font=FONT_UI, cursor="hand2")


def show_result_window(title, rows, raw_params=None, rates_only_text=""):
    """rows — (label, value, is_data, copyable).
    Окно фиксированного размера, окошки справа, копирование курсов."""
    win = Toplevel(root)
    win.title(title)
    win.configure(bg=BG)
    win.resizable(False, False)

    body = Frame(win, bg=BG)
    body.pack(fill="both", expand=True, padx=16, pady=16)
    body.columnconfigure(0, weight=1)
    body.columnconfigure(1, weight=0)

    r = 0
    for row in rows:
        label_text, value_text, is_data = row[0], row[1], row[2]
        copyable = row[3] if len(row) > 3 else False

        if label_text == "__header__":
            Label(body, text=value_text, bg=BG, fg=FG,
                  font=("Segoe UI", 11, "bold")).grid(
                row=r, column=0, columnspan=2, sticky="w", pady=(8, 4))
            r += 1
            continue

        if label_text == "__sep__":
            Frame(body, height=1, bg="#E0E0E0").grid(
                row=r, column=0, columnspan=2, sticky="ew", pady=6)
            r += 1
            continue

        Label(body, text=label_text, bg=BG, fg=FG, font=FONT_UI).grid(
            row=r, column=0, sticky="w", padx=(0, 12), pady=2)

        if is_data:
            box = make_data_box(body, value_text, copyable=copyable)
            box.grid(row=r, column=1, sticky="e", pady=2)
        else:
            Label(body, text=value_text, bg=BG, fg=FG, font=FONT_UI).grid(
                row=r, column=1, sticky="e", pady=2)
        r += 1

    # Кнопки — сразу под содержимым, отступ ≤ 2 строк
    btn_frame = Frame(win, bg=BG)
    btn_frame.pack(fill="x", padx=16, pady=(0, 12))

    def plain_text():
        lines = []
        for row in rows:
            label_text, value_text = row[0], row[1]
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

    def copy_rates_only():
        win.clipboard_clear()
        win.clipboard_append(rates_only_text)
        mb.showinfo("Скопировано", "Только курсы скопированы в буфер обмена", parent=win)

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

    b_rates = Button(btn_frame, text="Копировать курсы", command=copy_rates_only)
    style_btn(b_rates, primary=True)
    b_rates.pack(side="left", padx=(0, 8))

    b_save = Button(btn_frame, text="Сохранить в файл", command=save_to_file)
    style_btn(b_save, primary=True)
    b_save.pack(side="left")

    b_close = Button(btn_frame, text="Закрыть", command=win.destroy)
    style_btn(b_close, primary=False)
    b_close.pack(side="right")

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

        # Копирование только курсов
        rates_only_text = f"{base_code_1}/{target_code}: {v1}\n{base_code_2}/{target_code}: {v2}"

        # Строки: (label, value, is_data, copyable)
        rows = [
            ("__header__", "Котировки (Base/Quote)", False, False),

            (f"{base_code_1}/{target_code}", v1, True, True),
            ("", f"{currencies[base_code_1]} → {currencies[target_code]}", False, False),

            (f"{base_code_2}/{target_code}", v2, True, True),
            ("", f"{currencies[base_code_2]} → {currencies[target_code]}", False, False),

            ("__sep__", "", False, False),
            ("__header__", "Время", False, False),

            ("Время получения (локальное)", now_local, True, False),
            ("Время получения (МСК)", now_msk, True, False),
            ("Последнее обновление (UTC)", upd_1 or "—", True, False),
            ("Последнее обновление (МСК)", upd_msk, True, False),
            ("Актуальность", freshness, False, False),

            ("__sep__", "", False, False),
            ("Источник", "open.er-api.com (ExchangeRate-API)", False, False),
            ("Примечание", "API отдаёт средний курс (middle); Bid/Ask недоступны", False, False),
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

        show_result_window("Курсы обмена", rows,
                           raw_params=raw_params,
                           rates_only_text=rates_only_text)
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


# ---------- Главное окно (Metro UI + тёмная шапка) ----------

root = Tk()
root.title("Конвертер валют")
root.configure(bg=BG)
center_window(root, 360, 420)

# Верхняя панель — темнее
header = Frame(root, bg=HEADER_BG)
header.pack(fill="x", side="top")
Label(header, text="Конвертер валют", bg=HEADER_BG, fg=HEADER_FG,
      font=FONT_HEADER, pady=8).pack()
Frame(root, height=1, bg=DIVIDER).pack(fill="x")

# Контент
container = Frame(root, bg=BG)
container.pack(expand=True)


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