import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime, timezone

# ==========================================
# ТЕМА ДЛЯ ПЕРВОГО ОКНА (СВЕТЛАЯ, С ТЕМНО-СЕРОЙ ШАПКОЙ)
# ==========================================
THEME_LIGHT = {
    "bg": "#E0E0E0",  # Фон окна
    "card": "#EBEBEB",  # Фон карточек/полей
    "text": "#212121",
    "subtext": "#555555",
    "header_bg": "#333333",  # Темно-серый фон шапки
    "header_fg": "#FFFFFF",  # Белый текст шапки
    "entry_bg": "#000000",
    "entry_fg": "#00FF00",
    "btn": "#0078D7",
    "btn_fg": "white",
    "combo_bg": "#EBEBEB",
    "combo_fg": "#000000",
    "combo_select_bg": "#0078D7",
    "combo_select_fg": "#FFFFFF",
    "tree_bg": "#000000",
    "tree_fg": "#00FF00"
}

# ==========================================
# ТЕМА ДЛЯ ВТОРОГО ОКНА (ТЕМНАЯ)
# ==========================================
THEME_DARK = {
    "bg": "#1E1E1E", "card": "#2D2D2D", "text": "#E0E0E0", "subtext": "#A0A0A0",
    "entry_bg": "#000000", "entry_fg": "#00FF00", "btn": "#005A9E", "btn_fg": "white",
    "combo_bg": "#3A3A3A", "combo_fg": "#FFFFFF",
    "combo_select_bg": "#005A9E", "combo_select_fg": "#FFFFFF",
    "tree_bg": "#000000", "tree_fg": "#00FF00"
}


# ==========================================
# ВСПЛЫВАЮЩИЕ ПОДСКАЗКИ
# ==========================================
class ToolTip:
    def __init__(self, widget, text_func):
        self.widget = widget
        self.text_func = text_func
        self.tip_window = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        text = self.text_func()
        if not text or self.tip_window:
            return
        x = self.widget.winfo_rootx() + 15
        y = self.widget.winfo_rooty() + 25
        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        self.tip_window.wm_geometry(f"+{x}+{y}")
        self.tip_window.attributes("-topmost", True)

        tk.Label(self.tip_window, text=text, justify=tk.LEFT,
                 background="#FFFFE0", foreground="#000000",
                 relief=tk.SOLID, borderwidth=1,
                 font=("Segoe UI", 9), padx=4, pady=2).pack()

    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


def position_next_to_parent(window, parent, offset_x=15, offset_y=0):
    window.update_idletasks()
    parent.update_idletasks()
    parent_x = parent.winfo_rootx()
    parent_y = parent.winfo_rooty()
    parent_w = parent.winfo_width()
    window_w = window.winfo_reqwidth()
    window_h = window.winfo_reqheight()
    window.geometry(f"{window_w}x{window_h}+{parent_x + parent_w + offset_x}+{parent_y + offset_y}")


# ==========================================
# КЛАСС 1: ОКНО С КУРСАМИ (СВЕТЛАЯ, С ЛОГОТИПОМ)
# ==========================================
class RatesWindow:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()
        self.root.title("CryptoBeaver")
        self.root.resizable(False, False)
        self.root.geometry("520x1")

        self.theme = THEME_LIGHT
        self.root.configure(bg=self.theme["bg"])

        # --- ИКОНКА И ЛОГОТИП ---
        self.icon_image = None
        self.header_image = None
        try:
            self.icon_image = tk.PhotoImage(file="icon.png")
            self.root.iconphoto(True, self.icon_image)
            # Делаем картинку поменьше для шапки
            self.header_image = self._make_header_image("icon.png", max_height=40)
        except Exception as e:
            print(f"Не удалось загрузить иконку: {e}")

        self.coins = {
            "bitcoin": "₿ Bitcoin (BTC)",
            "ethereum": "Ξ Ethereum (ETH)",
            "solana": "◎ Solana (SOL)",
            "the-open-network": "💎 Toncoin (TON)",
            "ripple": "✕ XRP (XRP)",
            "cardano": "₳ Cardano (ADA)",
            "dogecoin": "Ð Dogecoin (DOGE)",
            "binancecoin": "🟡 BNB (BNB)"
        }
        self.coins_tooltips = {
            "bitcoin": "Bitcoin (BTC) — первая криптовалюта, 'цифровое золото'.",
            "ethereum": "Ethereum (ETH) — платформа для смарт-контрактов.",
            "solana": "Solana (SOL) — быстрый блокчейн для DeFi и NFT.",
            "the-open-network": "Toncoin (TON) — валюта блокчейна Telegram.",
            "ripple": "XRP — криптовалюта для мгновенных переводов.",
            "cardano": "Cardano (ADA) — научный блокчейн-проект.",
            "dogecoin": "Dogecoin (DOGE) — мем-монета, ставшая популярной.",
            "binancecoin": "BNB — нативная монета биржи Binance."
        }

        self.selected_coins_data = {}
        self.converter = None

        self.setup_ui()
        self.root.deiconify()
        self.root.geometry("")

    @staticmethod
    def _make_header_image(path, max_height=40):
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
        t = self.theme

        # --- ТЕМНО-СЕРАЯ ШАПКА С КАРТИНКОЙ И ТЕКСТОМ ---
        header_frame = tk.Frame(self.root, bg=t["header_bg"], height=60)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)

        # Если картинка загрузилась, показываем её слева
        if self.header_image is not None:
            img_label = tk.Label(header_frame, image=self.header_image, bg=t["header_bg"])
            img_label.image = self.header_image  # защита от сборщика мусора
            img_label.pack(side="left", padx=(20, 10), pady=10)

            # А рядом пишем название белым
            text_label = tk.Label(header_frame, text="CryptoBeaver",
                                  font=("Segoe UI", 18, "bold"),
                                  bg=t["header_bg"], fg=t["header_fg"])
            text_label.pack(side="left", pady=10)
        else:
            # Если картинки нет, просто текст по центру
            self.header_label = tk.Label(header_frame, text="CryptoBeaver",
                                         font=("Segoe UI", 18, "bold"),
                                         bg=t["header_bg"], fg=t["header_fg"])
            self.header_label.pack(expand=True)
        # ------------------------------------------------

        self.selection_frame = tk.LabelFrame(self.root, text="Выберите криптовалюты:",
                                             bg=t["bg"], fg=t["text"],
                                             font=("Segoe UI", 10))
        self.selection_frame.pack(fill="x", padx=20, pady=10)

        self.coin_vars = {}
        for i, (coin_id, coin_name) in enumerate(self.coins.items()):
            var = tk.BooleanVar(value=True)
            self.coin_vars[coin_id] = var
            chk = tk.Checkbutton(self.selection_frame, text=coin_name, variable=var,
                                 bg=t["bg"], fg=t["text"],
                                 activebackground=t["bg"],
                                 activeforeground=t["text"],
                                 selectcolor=t["card"],
                                 font=("Segoe UI", 9))
            tip_text = self.coins_tooltips.get(coin_id, "Описание отсутствует")
            ToolTip(chk, lambda text=tip_text: text)
            chk.grid(row=i // 2, column=i % 2, sticky="w", padx=10, pady=2)

        self.btn_frame = tk.Frame(self.root, bg=t["bg"])
        self.btn_frame.pack(pady=10)

        self.btn_get = tk.Button(self.btn_frame, text="Запросить курсы", command=self.get_rates,
                                 bg=t["btn"], fg=t["btn_fg"],
                                 font=("Segoe UI", 10, "bold"),
                                 padx=15, pady=5, relief="flat", cursor="hand2")
        self.btn_get.pack(side="left", padx=5)

        self.btn_open_converter = tk.Button(self.btn_frame, text="Конвертировать", command=self.open_converter,
                                            bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"),
                                            padx=15, pady=5, relief="flat", cursor="hand2", state="disabled")
        self.btn_open_converter.pack(side="left", padx=5)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading",
                        background="#000000", foreground="#00FF00",
                        font=("Consolas", 10, "bold"), relief="flat")
        style.map("Treeview.Heading", background=[('active', '#003300')])
        style.configure("Treeview",
                        background=t["tree_bg"], foreground=t["tree_fg"],
                        fieldbackground=t["tree_bg"],
                        font=("Consolas", 10, "bold"), rowheight=25)
        style.map("Treeview",
                  background=[('selected', '#004400')],
                  foreground=[('selected', '#00FF00')])

        columns = ("coin", "price", "change")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=8)
        self.tree.heading("coin", text="Криптовалюта")
        self.tree.heading("price", text="Цена (USD)")
        self.tree.heading("change", text="Изм. за 24ч (%)")
        self.tree.column("coin", width=180, anchor="w")
        self.tree.column("price", width=100, anchor="e")
        self.tree.column("change", width=100, anchor="e")
        self.tree.pack(fill="both", expand=True, padx=20, pady=5)

        self.time_label = tk.Label(self.root, text="Ожидание запроса...",
                                   font=("Segoe UI", 8),
                                   bg=t["bg"], fg=t["subtext"])
        self.time_label.pack(pady=5)

        self.source_label = tk.Label(self.root, text="Источник данных: CoinGecko API (coingecko.com)",
                                     font=("Segoe UI", 7),
                                     bg=t["bg"], fg=t["subtext"])
        self.source_label.pack(pady=(0, 10))

    def get_rates(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.selected_coins_data.clear()

        selected_coins = [coin_id for coin_id, var in self.coin_vars.items() if var.get()]
        if not selected_coins:
            messagebox.showwarning("Внимание", "Выберите хотя бы одну валюту!")
            return

        ids_str = ",".join(selected_coins)
        url = (f"https://api.coingecko.com/api/v3/simple/price?"
               f"ids={ids_str}&vs_currencies=usd&include_24hr_change=true")

        self.btn_get.config(state="disabled", text="Загрузка...")
        self.root.update()

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            for coin_id in selected_coins:
                if coin_id in data:
                    name = self.coins[coin_id]
                    price = data[coin_id].get("usd", 0)
                    change = data[coin_id].get("usd_24h_change", 0)
                    price_str = f"${price:,.2f}" if price >= 1 else f"${price:,.4f}"
                    change_str = f"{change:.2f}%" if change is not None else "—"
                    self.tree.insert("", "end", values=(name, price_str, change_str))
                    self.selected_coins_data[coin_id] = {
                        "name": name, "price": price, "change": change_str
                    }

            now = datetime.now(timezone.utc).astimezone().strftime("%d.%m.%Y %H:%M:%S")
            self.time_label.config(text=f"Последнее обновление: {now} (МСК)")
            self.btn_open_converter.config(state="normal")
            self.root.geometry("")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось получить данные:\n{e}")
        finally:
            self.btn_get.config(state="normal", text="Запросить курсы")

    def open_converter(self):
        selected_ids = [coin_id for coin_id, var in self.coin_vars.items() if var.get()]
        if self.converter is not None and self.converter.top.winfo_exists():
            self.converter.top.destroy()
        self.converter = ConverterWindow(self.root, self.selected_coins_data, selected_ids)


# ==========================================
# КЛАСС 2: КОНВЕРТЕР (ТЕМНАЯ ТЕМА)
# ==========================================
class ConverterWindow:
    def __init__(self, parent, coins_data, selected_ids):
        self.top = tk.Toplevel(parent)
        self.top.withdraw()
        self.top.title("Конвертер валют")
        self.top.resizable(False, False)

        self.theme = THEME_DARK
        self.top.configure(bg=self.theme["bg"])

        try:
            self.icon_image = tk.PhotoImage(file="icon.png")
            self.top.iconphoto(True, self.icon_image)
        except Exception as e:
            print(f"Не удалось загрузить иконку: {e}")

        self.full_names = {
            "bitcoin": "Bitcoin — первая и самая популярная криптовалюта в мире.",
            "ethereum": "Ethereum — платформа для смарт-контрактов и децентрализованных приложений.",
            "tether": "Tether (USDT) — стейблкоин, привязанный к доллару США (1 USDT ≈ 1 USD).",
            "solana": "Solana — высокопроизводительный блокчейн для DeFi и NFT.",
            "binancecoin": "BNB — нативная монета экосистемы Binance.",
            "the-open-network": "Toncoin — криптовалюта блокчейна TON (The Open Network).",
            "ripple": "XRP — криптовалюта для быстрых международных платежей.",
            "cardano": "Cardano — блокчейн-платформа с научным подходом к разработке.",
            "dogecoin": "Dogecoin — мем-криптовалюта, ставшая популярной благодаря сообществу.",
            "usd": "Доллар США (USD) — официальная валюта Соединённых Штатов.",
            "eur": "Евро (EUR) — официальная валюта Евросоюза.",
            "rub": "Российский рубль (RUB) — официальная валюта Российской Федерации."
        }

        all_coins = {
            "bitcoin": ("BTC", "₿ Bitcoin"),
            "ethereum": ("ETH", "Ξ Ethereum"),
            "tether": ("USDT", "💵 Tether"),
            "solana": ("SOL", "◎ Solana"),
            "binancecoin": ("BNB", "🟡 BNB"),
            "the-open-network": ("TON", "💎 Toncoin"),
            "ripple": ("XRP", "✕ XRP"),
            "cardano": ("ADA", "₳ Cardano"),
            "dogecoin": ("DOGE", "Ð Dogecoin"),
            "usd": ("USD", "💲 Доллар США"),
            "eur": ("EUR", "💶 Евро"),
            "rub": ("RUB", "₽ Российский рубль")
        }

        self.coins = {}
        for coin_id in selected_ids:
            if coin_id in all_coins:
                self.coins[coin_id] = all_coins[coin_id]
        self.coins["usd"] = all_coins["usd"]
        self.coins["eur"] = all_coins["eur"]
        self.coins["rub"] = all_coins["rub"]

        self.from_combo = None
        self.to_combo = None
        self.from_entry = None
        self.to_entry = None

        self.rates = {}
        self.fetch_rates()
        self.setup_ui()
        self.apply_theme()

        self.top.deiconify()
        position_next_to_parent(self.top, parent, offset_x=15)
        self.top.transient(parent)

    def fetch_rates(self):
        crypto_ids = [k for k in self.coins.keys() if k not in ("usd", "eur", "rub")]
        if not crypto_ids:
            return
        ids_str = ",".join(crypto_ids)
        url = (f"https://api.coingecko.com/api/v3/simple/price?"
               f"ids={ids_str}&vs_currencies=usd,eur,rub")
        try:
            res = requests.get(url, timeout=5).json()
            for coin_id, prices in res.items():
                if "usd" in prices: self.rates[f"{coin_id}_usd"] = prices["usd"]
                if "eur" in prices: self.rates[f"{coin_id}_eur"] = prices["eur"]
                if "rub" in prices: self.rates[f"{coin_id}_rub"] = prices["rub"]
            self.rates["usd_usd"] = 1.0
            self.rates["eur_eur"] = 1.0
            self.rates["rub_rub"] = 1.0
            self.rates["usd_eur"] = (1.0 / self.rates.get("bitcoin_eur", 1)
                                     * self.rates.get("bitcoin_usd", 1)
                                     if "bitcoin_eur" in self.rates else 0.92)
            self.rates["eur_usd"] = 1.0 / self.rates["usd_eur"] if self.rates["usd_eur"] else 1.08
            self.rates["usd_rub"] = (self.rates.get("bitcoin_rub", 90.0)
                                     / self.rates.get("bitcoin_usd", 1.0)
                                     if "bitcoin_rub" in self.rates else 90.0)
            self.rates["rub_usd"] = 1.0 / self.rates["usd_rub"] if self.rates["usd_rub"] else 0.011
            self.rates["eur_rub"] = (self.rates["usd_rub"] / self.rates["usd_eur"]
                                     if self.rates["usd_eur"] else 100.0)
            self.rates["rub_eur"] = 1.0 / self.rates["eur_rub"] if self.rates["eur_rub"] else 0.01
        except Exception as e:
            print(f"Ошибка загрузки курсов: {e}")

    def validate_number(self, new_value):
        if new_value == "":
            return True
        check_val = new_value.replace(",", ".")
        try:
            float(check_val)
            return True
        except ValueError:
            if new_value in (".", ","):
                return True
            if new_value.startswith("-") and len(new_value) > 1:
                try:
                    float(check_val[1:])
                    return True
                except ValueError:
                    pass
            return False

    def setup_ui(self):
        self.title_label = tk.Label(self.top, text="Конвертация",
                                    font=("Segoe UI", 14, "bold"),
                                    bg=self.theme["bg"], fg=self.theme["text"])
        self.title_label.pack(pady=(15, 10))

        self.from_frame = self.create_block("Продаю", "USDT", is_from=True)
        self.from_frame.pack(fill="x", padx=25, pady=(5, 15))

        self.swap_btn = tk.Button(
            self.top, text="⇅ Поменять", command=self.swap,
            bg=self.theme["btn"], fg=self.theme["btn_fg"],
            font=("Segoe UI", 10, "bold"), padx=15, pady=5,
            relief="flat", cursor="hand2"
        )
        self.swap_btn.pack(pady=5)

        self.to_frame = self.create_block("Покупаю", "BTC", is_from=False)
        self.to_frame.pack(fill="x", padx=25, pady=(5, 20))

        self.result_frame = tk.Frame(self.top, bg=self.theme["bg"])
        self.result_frame.pack(fill="x", padx=25)

        self.usd_label = tk.Label(self.result_frame, text="≈ $ 0,00",
                                  font=("Segoe UI", 12, "bold"),
                                  bg=self.theme["bg"], fg=self.theme["text"])
        self.usd_label.pack(anchor="e")

        self.rub_label = tk.Label(self.result_frame, text="≈ ₽ 0,00",
                                  font=("Segoe UI", 12, "bold"),
                                  bg=self.theme["bg"], fg=self.theme["text"])
        self.rub_label.pack(anchor="e")

        self.source_label = tk.Label(self.top, text="Данные: CoinGecko API",
                                     font=("Segoe UI", 7),
                                     bg=self.theme["bg"], fg=self.theme["subtext"])
        self.source_label.pack(side="bottom", pady=10)

    def create_block(self, title, default_coin, is_from):
        frame = tk.Frame(self.top, bg=self.theme["card"], highlightthickness=1,
                         highlightbackground=self.theme["subtext"])

        title_lbl = tk.Label(frame, text=title, font=("Segoe UI", 9),
                             bg=self.theme["card"], fg=self.theme["subtext"])
        title_lbl.pack(anchor="w", padx=12, pady=(10, 2))

        row = tk.Frame(frame, bg=self.theme["card"])
        row.pack(fill="x", padx=12, pady=(0, 15))

        coin_values = [f"{v[0]} - {v[1]}" for k, v in self.coins.items()]
        combo = ttk.Combobox(row, values=coin_values, width=16,
                             state="readonly", font=("Segoe UI", 10))
        combo.pack(side="left")

        default_id = None
        for k, v in self.coins.items():
            if v[0] == default_coin:
                default_id = k
                break
        if default_id:
            combo.set(f"{self.coins[default_id][0]} - {self.coins[default_id][1]}")
        else:
            combo.set(coin_values[0])

        def get_tooltip_text():
            current_val = combo.get()
            ticker = current_val.split(" - ")[0]
            coin_id = self.get_id_by_ticker(ticker)
            if coin_id and coin_id in self.full_names:
                return self.full_names[coin_id]
            return "Описание отсутствует"

        ToolTip(combo, get_tooltip_text)

        entry = tk.Entry(
            row, font=("Consolas", 16, "bold"),
            bg=self.theme["entry_bg"], fg=self.theme["entry_fg"],
            insertbackground=self.theme["entry_fg"],
            selectbackground="#004400", selectforeground="#00FF00",
            bd=0, justify="right",
            validate="key",
            validatecommand=(self.top.register(self.validate_number), "%P")
        )
        entry.pack(side="right", fill="x", expand=True, padx=(10, 0))

        if is_from:
            self.from_combo = combo
            self.from_entry = entry
            entry.insert(0, "1")
            entry.bind("<KeyRelease>", self.calculate)
            combo.bind("<<ComboboxSelected>>", lambda e: self.calculate())
        else:
            self.to_combo = combo
            self.to_entry = entry
            entry.config(state="readonly",
                         readonlybackground=self.theme["entry_bg"],
                         fg=self.theme["entry_fg"])

        frame._title_lbl = title_lbl
        frame._row = row
        return frame

    def get_id_by_ticker(self, ticker):
        for k, v in self.coins.items():
            if v[0] == ticker:
                return k
        return None

    def calculate(self, event=None):
        try:
            amount_str = self.from_entry.get().replace(",", ".")
            if not amount_str:
                return
            amount = float(amount_str)

            from_ticker = self.from_combo.get().split(" - ")[0]
            to_ticker = self.to_combo.get().split(" - ")[0]
            from_id = self.get_id_by_ticker(from_ticker)
            to_id = self.get_id_by_ticker(to_ticker)
            if not from_id or not to_id:
                return

            if from_id in ("usd", "eur", "rub"):
                if from_id == "usd":
                    from_to_usd = 1.0
                elif from_id == "eur":
                    from_to_usd = 1.0 / self.rates.get("usd_eur", 0.92)
                elif from_id == "rub":
                    from_to_usd = 1.0 / self.rates.get("usd_rub", 90.0)
            else:
                from_to_usd = self.rates.get(f"{from_id}_usd", 0)

            if to_id in ("usd", "eur", "rub"):
                if to_id == "usd":
                    usd_to_target = 1.0
                elif to_id == "eur":
                    usd_to_target = self.rates.get("usd_eur", 0.92)
                elif to_id == "rub":
                    usd_to_target = self.rates.get("usd_rub", 90.0)
            else:
                price_usd = self.rates.get(f"{to_id}_usd", 0)
                usd_to_target = 1.0 / price_usd if price_usd else 0

            if from_to_usd == 0 or usd_to_target == 0:
                self.to_entry.config(state="normal")
                self.to_entry.delete(0, tk.END)
                self.to_entry.insert(0, "Нет данных")
                self.to_entry.config(state="readonly")
                return

            total_usd = amount * from_to_usd
            total_target = total_usd * usd_to_target

            self.to_entry.config(state="normal")
            self.to_entry.delete(0, tk.END)
            if total_target < 0.01:
                res_str = f"{total_target:.6f}".replace(".", ",")
            else:
                res_str = f"{total_target:.4f}".replace(".", ",")
            self.to_entry.insert(0, res_str)
            self.to_entry.config(state="readonly")

            self.usd_label.config(text=f"≈ $ {total_usd:,.2f}".replace(".", ","))
            rub_total = total_usd * self.rates.get("usd_rub", 90.0)
            self.rub_label.config(text=f"≈ ₽ {rub_total:,.2f}".replace(".", ","))
        except ValueError:
            pass

    def swap(self):
        if not self.from_combo:
            return
        from_val = self.from_combo.get()
        to_val = self.to_combo.get()
        self.from_combo.set(to_val)
        self.to_combo.set(from_val)
        self.calculate()

    def apply_theme(self):
        t = self.theme

        self.top.configure(bg=t["bg"])
        self.title_label.configure(bg=t["bg"], fg=t["text"])

        for frame in (self.from_frame, self.to_frame):
            frame.configure(bg=t["card"], highlightbackground=t["subtext"])
            if hasattr(frame, "_title_lbl"):
                frame._title_lbl.configure(bg=t["card"], fg=t["subtext"])
            if hasattr(frame, "_row"):
                frame._row.configure(bg=t["card"])

        self.swap_btn.configure(bg=t["btn"], fg=t["btn_fg"])

        for entry in (self.from_entry, self.to_entry):
            if entry is None:
                continue
            entry.configure(
                bg=t["entry_bg"], fg=t["entry_fg"],
                insertbackground=t["entry_fg"],
                readonlybackground=t["entry_bg"],
            )

        self.result_frame.configure(bg=t["bg"])
        self.usd_label.configure(bg=t["bg"], fg=t["text"])
        self.rub_label.configure(bg=t["bg"], fg=t["text"])
        self.source_label.configure(bg=t["bg"], fg=t["subtext"])

        self._apply_combobox_theme()

    def _apply_combobox_theme(self):
        t = self.theme
        style = ttk.Style(self.top)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "TCombobox",
            fieldbackground=t["combo_bg"],
            background=t["combo_bg"],
            foreground=t["combo_fg"],
            arrowcolor=t["combo_fg"],
            bordercolor=t["subtext"],
            lightcolor=t["combo_bg"],
            darkcolor=t["combo_bg"],
            selectbackground=t["combo_select_bg"],
            selectforeground=t["combo_select_fg"],
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", t["combo_bg"])],
            foreground=[("readonly", t["combo_fg"])],
            background=[("readonly", t["combo_bg"])],
            selectbackground=[("readonly", t["combo_select_bg"])],
            selectforeground=[("readonly", t["combo_select_fg"])],
        )

        self.top.option_add("*TCombobox*Listbox.background", t["combo_bg"])
        self.top.option_add("*TCombobox*Listbox.foreground", t["combo_fg"])
        self.top.option_add("*TCombobox*Listbox.selectBackground", t["combo_select_bg"])
        self.top.option_add("*TCombobox*Listbox.selectForeground", t["combo_select_fg"])
        self.top.option_add("*TCombobox*Listbox.font", ("Segoe UI", 10))


# ==========================================
# ЗАПУСК
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = RatesWindow(root)
    root.mainloop()