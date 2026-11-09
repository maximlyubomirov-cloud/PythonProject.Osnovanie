import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
from datetime import datetime

# ==========================================
# 1. КОНСТАНТЫ И СЛОВАРИ
# ==========================================
FIAT_CURRENCIES = ["usd", "eur", "rub"]

ALL_COINS = {
    "bitcoin": {"ticker": "BTC", "name": "Bitcoin", "icon": "₿", "type": "crypto", "desc": "Первая криптовалюта"},
    "ethereum": {"ticker": "ETH", "name": "Ethereum", "icon": "Ξ", "type": "crypto", "desc": "Смарт-контракты"},
    "tether": {"ticker": "USDT", "name": "Tether", "icon": "💵", "type": "crypto", "desc": "Стейблкоин к USD"},
    "solana": {"ticker": "SOL", "name": "Solana", "icon": "◎", "type": "crypto", "desc": "Быстрый блокчейн"},
    "binancecoin": {"ticker": "BNB", "name": "BNB", "icon": "🟡", "type": "crypto", "desc": "Монета Binance"},
    "the-open-network": {"ticker": "TON", "name": "Toncoin", "icon": "💎", "type": "crypto",
                         "desc": "Блокчейн Telegram"},
    "ripple": {"ticker": "XRP", "name": "XRP", "icon": "✕", "type": "crypto", "desc": "Переводы"},
    "cardano": {"ticker": "ADA", "name": "Cardano", "icon": "₳", "type": "crypto", "desc": "Научный подход"},
    "dogecoin": {"ticker": "DOGE", "name": "Dogecoin", "icon": "Ð", "type": "crypto", "desc": "Мем-монета"},
    "usd": {"ticker": "USD", "name": "Доллар", "icon": "💲", "type": "fiat", "desc": "США"},
    "eur": {"ticker": "EUR", "name": "Евро", "icon": "💶", "type": "fiat", "desc": "Евросоюз"},
    "rub": {"ticker": "RUB", "name": "Рубль", "icon": "₽", "type": "fiat", "desc": "Россия"},
}

THEME_LIGHT = {"bg": "#E0E0E0", "card": "#EBEBEB", "text": "#212121", "subtext": "#555555",
               "btn": "#0078D7", "btn_fg": "white", "entry_bg": "#000000", "entry_fg": "#00FF00",
               "tree_bg": "#000000", "tree_fg": "#00FF00"}

THEME_DARK = {"bg": "#1E1E1E", "card": "#2D2D2D", "text": "#E0E0E0", "subtext": "#A0A0A0",
              "btn": "#005A9E", "btn_fg": "white", "entry_bg": "#000000", "entry_fg": "#00FF00",
              "combo_bg": "#3A3A3A", "combo_fg": "#FFFFFF", "combo_select_bg": "#005A9E", "combo_select_fg": "#FFFFFF"}


# ==========================================
# 2. УТИЛИТЫ И API
# ==========================================
class CryptoAPI:
    BASE_URL = "https://api.coingecko.com/api/v3/simple/price"

    @staticmethod
    def get_rates(coin_ids, currencies="usd", change=False):
        if not coin_ids: return None
        url = f"{CryptoAPI.BASE_URL}?ids={','.join(coin_ids)}&vs_currencies={currencies}"
        if change: url += "&include_24hr_change=true"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"API Error: {e}")
            return None


class ToolTip:
    def __init__(self, widget, text_func):
        self.widget, self.text_func, self.tip_window = widget, text_func, None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        text = self.text_func()
        if not text or self.tip_window: return
        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        self.tip_window.wm_geometry(f"+{self.widget.winfo_rootx() + 15}+{self.widget.winfo_rooty() + 25}")
        self.tip_window.attributes("-topmost", True)
        tk.Label(self.tip_window, text=text, background="#FFFFE0", relief=tk.SOLID, borderwidth=1).pack()

    def hide_tip(self, event=None):
        if self.tip_window: self.tip_window.destroy(); self.tip_window = None


# ==========================================
# 3. ГЛАВНОЕ ОКНО
# ==========================================
class RatesWindow:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()
        self.root.title("CryptoBeaver")
        self.root.configure(bg=THEME_LIGHT["bg"])
        self.root.resizable(False, False)
        self.root.geometry("520x1")

        self.converter = None

        self.icon_image = None
        self.header_image = None
        try:
            self.icon_image = tk.PhotoImage(file="icon.png")
            self.root.iconphoto(True, self.icon_image)
            self.header_image = self._make_header_image("icon.png", max_height=64)
        except Exception as e:
            print(f"Не удалось загрузить иконку: {e}")

        self.setup_ui()
        self.root.deiconify()
        self.root.geometry("")

    @staticmethod
    def _make_header_image(path, max_height):
        try:
            img = tk.PhotoImage(file=path)
        except Exception:
            return None
        h = img.height()
        if h <= max_height:
            return img
        factor = max(1, (h + max_height - 1) // max_height)
        return img.subsample(factor, factor)

    def setup_ui(self):
        t = THEME_LIGHT

        if self.header_image:
            lbl = tk.Label(self.root, image=self.header_image, bg=t["bg"])
            lbl.image = self.header_image
            lbl.pack(pady=10)
        else:
            tk.Label(self.root, text="CryptoBeaver", font=("Segoe UI", 16, "bold"),
                     bg=t["bg"], fg=t["text"]).pack(pady=10)

        frame = tk.LabelFrame(self.root, text="Выберите криптовалюты:", bg=t["bg"], fg=t["text"], font=("Segoe UI", 10))
        frame.pack(fill="x", padx=20, pady=5)

        self.coin_vars = {}
        crypto_list = [k for k, v in ALL_COINS.items() if v["type"] == "crypto"]
        for i, coin_id in enumerate(crypto_list):
            self.coin_vars[coin_id] = tk.BooleanVar(value=True)
            c_info = ALL_COINS[coin_id]
            chk = tk.Checkbutton(frame, text=f"{c_info['icon']} {c_info['name']} ({c_info['ticker']})",
                                 variable=self.coin_vars[coin_id], bg=t["bg"], fg=t["text"],
                                 selectcolor=t["card"], font=("Segoe UI", 9))
            ToolTip(chk, lambda c=c_info: c["desc"])
            chk.grid(row=i // 2, column=i % 2, sticky="w", padx=10, pady=2)

        btn_frame = tk.Frame(self.root, bg=t["bg"])
        btn_frame.pack(pady=10)

        self.btn_get = tk.Button(btn_frame, text="Запросить курсы", command=self.get_rates,
                                 bg=t["btn"], fg=t["btn_fg"], font=("Segoe UI", 10, "bold"),
                                 padx=15, pady=5, relief="flat", cursor="hand2")
        self.btn_get.pack(side="left", padx=5)

        self.btn_convert = tk.Button(btn_frame, text="Конвертировать", command=self.open_converter,
                                     bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"),
                                     padx=15, pady=5, relief="flat", cursor="hand2", state="disabled")
        self.btn_convert.pack(side="left", padx=5)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="#000000", foreground="#00FF00", font=("Consolas", 10, "bold"))
        style.configure("Treeview", background=t["tree_bg"], foreground=t["tree_fg"], fieldbackground=t["tree_bg"],
                        rowheight=25)

        self.tree = ttk.Treeview(self.root, columns=("coin", "price", "change"), show="headings", height=8)
        self.tree.heading("coin", text="Криптовалюта")
        self.tree.heading("price", text="Цена (USD)")
        self.tree.heading("change", text="Изм. за 24ч (%)")
        self.tree.column("coin", width=180, anchor="w")
        self.tree.column("price", width=100, anchor="e")
        self.tree.column("change", width=100, anchor="e")
        self.tree.pack(fill="both", expand=True, padx=20, pady=5)

        self.time_label = tk.Label(self.root, text="Ожидание запроса...", font=("Segoe UI", 8), bg=t["bg"],
                                   fg=t["subtext"])
        self.time_label.pack(pady=5)

    def get_rates(self):
        self.btn_get.config(state="disabled", text="Загрузка...")
        self.root.update()

        selected = [k for k, v in self.coin_vars.items() if v.get()]
        if not selected:
            messagebox.showwarning("Внимание", "Выберите валюту!")
            self.btn_get.config(state="normal", text="Запросить курсы")
            return

        self.tree.delete(*self.tree.get_children())
        data = CryptoAPI.get_rates(selected, "usd", change=True)

        if data:
            for coin_id in selected:
                if coin_id in data:
                    c_info = ALL_COINS[coin_id]
                    price = data[coin_id].get("usd", 0)
                    change = data[coin_id].get("usd_24h_change", 0) or 0
                    price_str = f"${price:,.2f}" if price >= 1 else f"${price:,.4f}"
                    self.tree.insert("", "end",
                                     values=(f"{c_info['icon']} {c_info['name']}", price_str, f"{change:.2f}%"))

            self.time_label.config(text=f"Обновлено: {datetime.now().strftime('%H:%M:%S')}")
            self.btn_convert.config(state="normal")
        else:
            messagebox.showerror("Ошибка", "Нет данных от API")

        self.btn_get.config(state="normal", text="Запросить курсы")

    def open_converter(self):
        if self.converter and self.converter.top.winfo_exists(): self.converter.top.destroy()
        self.converter = ConverterWindow(self.root, [k for k, v in self.coin_vars.items() if v.get()])


# ==========================================
# 4. КОНВЕРТЕР
# ==========================================
class ConverterWindow:
    def __init__(self, parent, selected_ids):
        self.top = tk.Toplevel(parent)
        self.top.withdraw()
        self.top.title("Конвертер")
        self.top.configure(bg=THEME_DARK["bg"])
        self.top.resizable(False, False)

        self.selected_ids = selected_ids
        self.rates = self._fetch_and_calc_rates()
        self.setup_ui()

        self.top.deiconify()
        self.top.geometry(f"+{parent.winfo_rootx() + parent.winfo_width() + 15}+{parent.winfo_rooty()}")
        self.top.geometry("")
        self.top.transient(parent);
        self.top.grab_set()

    def _fetch_and_calc_rates(self):
        rates = {}
        crypto_ids = [k for k in self.selected_ids if ALL_COINS[k]["type"] == "crypto"]
        data = CryptoAPI.get_rates(crypto_ids, "usd,eur,rub")
        if data:
            for coin_id, prices in data.items():
                for cur, val in prices.items():
                    rates[f"{coin_id}_{cur}"] = val

        base_usd = rates.get("tether_usd", rates.get("bitcoin_usd", 1))
        rates["usd_rub"] = rates.get("tether_rub", rates.get("bitcoin_rub", 90)) / base_usd
        rates["usd_eur"] = rates.get("tether_eur", rates.get("bitcoin_eur", 0.92)) / base_usd
        return rates

    def setup_ui(self):
        t = THEME_DARK

        # --- НАСТРОЙКА СТИЛЕЙ ДЛЯ COMBOBOX ---
        style = ttk.Style()
        style.theme_use("clam")

        # Настройка поля ввода (когда список закрыт)
        style.configure(
            "TCombobox",
            fieldbackground=t["combo_bg"],  # Темно-серый фон
            background=t["combo_bg"],  # Фон кнопки со стрелочкой
            foreground=t["combo_fg"],  # Белый текст
            arrowcolor=t["combo_fg"],  # Белая стрелочка
            selectbackground=t["combo_select_bg"],
            selectforeground=t["combo_select_fg"]
        )

        # Принудительно фиксируем цвета в состоянии readonly
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", t["combo_bg"])],
            foreground=[("readonly", t["combo_fg"])],
            background=[("readonly", t["combo_bg"])],
            selectbackground=[("readonly", t["combo_select_bg"])],
            selectforeground=[("readonly", t["combo_select_fg"])]
        )

        # Настройка раскрывающегося списка
        self.top.option_add("*TCombobox*Listbox.background", t["combo_bg"])
        self.top.option_add("*TCombobox*Listbox.foreground", t["combo_fg"])
        self.top.option_add("*TCombobox*Listbox.selectBackground", t["combo_select_bg"])
        self.top.option_add("*TCombobox*Listbox.selectForeground", t["combo_select_fg"])
        # ---------------------------------------

        tk.Label(self.top, text="Конвертация", font=("Segoe UI", 14, "bold"), bg=t["bg"], fg=t["text"]).pack(pady=10)

        self.from_combo, self.from_entry = self.create_input_block("Продаю", "USDT")
        tk.Button(self.top, text="⇅ Поменять", command=self.swap, bg=t["btn"], fg="white",
                  font=("Segoe UI", 10, "bold"), padx=15, pady=5, relief="flat").pack(pady=5)
        self.to_combo, self.to_entry = self.create_input_block("Покупаю", "BTC")

        self.usd_label = tk.Label(self.top, text="≈ $ 0,00", bg=t["bg"], fg=t["text"], font=("Segoe UI", 12, "bold"))
        self.usd_label.pack(anchor="e", padx=30)
        self.rub_label = tk.Label(self.top, text="≈ ₽ 0,00", bg=t["bg"], fg=t["text"], font=("Segoe UI", 12, "bold"))
        self.rub_label.pack(anchor="e", padx=30)

        tk.Button(self.top, text="💾 Сохранить в файл", command=self.save_to_file,
                  bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"), padx=15, pady=5, relief="flat").pack(pady=15)

    def create_input_block(self, title, default_ticker):
        t = THEME_DARK
        frame = tk.Frame(self.top, bg=t["card"], highlightthickness=1, highlightbackground=t["subtext"])
        frame.pack(fill="x", padx=20, pady=5)
        tk.Label(frame, text=title, bg=t["card"], fg=t["subtext"], font=("Segoe UI", 9)).pack(anchor="w", padx=10,
                                                                                              pady=(5, 0))

        row = tk.Frame(frame, bg=t["card"])
        row.pack(fill="x", padx=10, pady=(0, 10))

        available = [k for k in self.selected_ids if ALL_COINS[k]["type"] == "crypto"] + FIAT_CURRENCIES
        combo_values = [f"{ALL_COINS[k]['ticker']} - {ALL_COINS[k]['name']}" for k in available]

        combo = ttk.Combobox(row, values=combo_values, state="readonly", font=("Segoe UI", 10))
        combo.pack(side="left")
        combo.set(next((v for v in combo_values if v.startswith(default_ticker)), combo_values[0]))
        combo.bind("<<ComboboxSelected>>", self.calculate)

        def get_tooltip():
            ticker = combo.get().split(" ")[0]
            for k, v in ALL_COINS.items():
                if v["ticker"] == ticker: return v["desc"]
            return ""

        ToolTip(combo, get_tooltip)

        entry = tk.Entry(row, font=("Consolas", 16, "bold"), bg=t["entry_bg"], fg=t["entry_fg"],
                         insertbackground=t["entry_fg"],
                         selectbackground="#004400", selectforeground="#00FF00",
                         justify="right", bd=0)
        entry.pack(side="right", fill="x", expand=True, padx=(10, 0))

        if title == "Продаю":
            entry.insert(0, "1")
            entry.bind("<KeyRelease>", self.calculate)
        else:
            entry.config(state="readonly", readonlybackground=t["entry_bg"])
        return combo, entry

    def _get_usd_rate(self, coin_id):
        if coin_id == "usd": return 1.0
        if coin_id == "eur": return 1.0 / self.rates.get("usd_eur", 0.92)
        if coin_id == "rub": return 1.0 / self.rates.get("usd_rub", 90)
        return self.rates.get(f"{coin_id}_usd", 0)

    def calculate(self, event=None):
        try:
            amount = float(self.from_entry.get().replace(",", "."))
        except ValueError:
            return

        from_id = next(k for k, v in ALL_COINS.items() if v["ticker"] == self.from_combo.get().split(" ")[0])
        to_id = next(k for k, v in ALL_COINS.items() if v["ticker"] == self.to_combo.get().split(" ")[0])

        rate_f = self._get_usd_rate(from_id)
        rate_t = self._get_usd_rate(to_id)
        if not rate_f or not rate_t: return

        total_usd = amount * rate_f
        total_target = total_usd / rate_t

        self.to_entry.config(state="normal")
        self.to_entry.delete(0, tk.END)
        self.to_entry.insert(0, f"{total_target:.6f}".replace(".", ","))
        self.to_entry.config(state="readonly")

        self.usd_label.config(text=f"≈ $ {total_usd:,.2f}".replace(".", ","))
        self.rub_label.config(text=f"≈ ₽ {total_usd * self.rates.get('usd_rub', 90):,.2f}".replace(".", ","))

    def swap(self):
        f_val, t_val = self.from_combo.get(), self.to_combo.get()
        self.from_combo.set(t_val);
        self.to_combo.set(f_val)
        self.calculate()

    def save_to_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", title="Сохранить отчет")
        if not path: return

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"=== ОТЧЕТ О КОНВЕРТАЦИИ ===\nДата: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n")
                f.write(
                    f"Обмен: {self.from_entry.get()} {self.from_combo.get()} -> {self.to_entry.get()} {self.to_combo.get()}\n\n")
                f.write("--- АКТУАЛЬНЫЕ КУРСЫ ---\n")

                for key, val in self.rates.items():
                    if key.endswith("_usd"):
                        name = ALL_COINS.get(key.replace("_usd", ""), {}).get("name", key)
                        f.write(f"{name}: ${val:,.2f}\n")
                    elif key == "usd_rub":
                        f.write(f"USD/RUB: {val:,.2f}\n")
                    elif key == "usd_eur":
                        f.write(f"USD/EUR: {val:,.2f}\n")

            messagebox.showinfo("Готово", "Файл сохранен!")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = RatesWindow(root)
    root.mainloop()