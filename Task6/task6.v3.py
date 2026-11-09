import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime, timezone


# ==========================================
# КЛАСС 1: ОКНО С КУРСАМИ
# ==========================================
class RatesWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор криптовалют (CoinGecko)")
        # Задаем точный размер окна
        self.root.geometry("520x580")
        self.root.configure(bg="#F3F3F3")
        # Запрещаем пользователю менять размер окна
        self.root.resizable(False, False)

        self.coins = {
            "bitcoin": "Bitcoin (BTC)",
            "ethereum": "Ethereum (ETH)",
            "solana": "Solana (SOL)",
            "the-open-network": "Toncoin (TON)",
            "ripple": "XRP (XRP)",
            "cardano": "Cardano (ADA)",
            "dogecoin": "Dogecoin (DOGE)",
            "binancecoin": "BNB (BNB)"
        }
        self.selected_coins_data = {}
        self.setup_ui()

    def setup_ui(self):
        header = tk.Label(self.root, text="Курсы криптовалют к USD",
                          font=("Segoe UI", 14, "bold"), bg="#F3F3F3", fg="#212121")
        header.pack(pady=10)

        selection_frame = tk.LabelFrame(self.root, text="Выберите монеты:",
                                        bg="#F3F3F3", font=("Segoe UI", 10))
        selection_frame.pack(fill="x", padx=20, pady=5)

        self.coin_vars = {}
        for i, (coin_id, coin_name) in enumerate(self.coins.items()):
            var = tk.BooleanVar(value=True)
            self.coin_vars[coin_id] = var
            chk = tk.Checkbutton(selection_frame, text=coin_name, variable=var,
                                 bg="#F3F3F3", font=("Segoe UI", 9))
            row = i // 2
            col = i % 2
            chk.grid(row=row, column=col, sticky="w", padx=10, pady=2)

        btn_frame = tk.Frame(self.root, bg="#F3F3F3")
        btn_frame.pack(pady=10)

        self.btn_get = tk.Button(btn_frame, text="Запросить курсы", command=self.get_rates,
                                 bg="#0078D7", fg="white", font=("Segoe UI", 10, "bold"),
                                 padx=15, pady=5, relief="flat", cursor="hand2")
        self.btn_get.pack(side="left", padx=5)

        self.btn_open_converter = tk.Button(btn_frame, text="Конвертировать", command=self.open_converter,
                                            bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"),
                                            padx=15, pady=5, relief="flat", cursor="hand2", state="disabled")
        self.btn_open_converter.pack(side="left", padx=5)

        columns = ("coin", "price", "change")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=8)
        self.tree.heading("coin", text="Монета")
        self.tree.heading("price", text="Цена (USD)")
        self.tree.heading("change", text="Изм. за 24ч (%)")

        self.tree.column("coin", width=150, anchor="w")
        self.tree.column("price", width=100, anchor="e")
        self.tree.column("change", width=100, anchor="e")
        self.tree.pack(fill="both", expand=True, padx=20, pady=5)

        self.time_label = tk.Label(self.root, text="Ожидание запроса...",
                                   font=("Segoe UI", 8), bg="#F3F3F3", fg="#666")
        self.time_label.pack(pady=5)

    def get_rates(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.selected_coins_data.clear()

        selected_coins = [coin_id for coin_id, var in self.coin_vars.items() if var.get()]

        if not selected_coins:
            messagebox.showwarning("Внимание", "Выберите хотя бы одну валюту!")
            return

        ids_str = ",".join(selected_coins)
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids_str}&vs_currencies=usd&include_24hr_change=true"

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

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось получить данные:\n{e}")
        finally:
            self.btn_get.config(state="normal", text="Запросить курсы")

    def open_converter(self):
        selected_ids = [coin_id for coin_id, var in self.coin_vars.items() if var.get()]
        ConverterWindow(self.root, self.selected_coins_data, selected_ids)


# ==========================================
# КЛАСС 2: КОНВЕРТЕР
# ==========================================
class ConverterWindow:
    def __init__(self, parent, coins_data, selected_ids):
        self.top = tk.Toplevel(parent)
        self.top.title("Конвертер валют")
        self.top.geometry("440x520")  # Чуть увеличили высоту для отступов
        self.top.configure(bg="#F3F3F3")
        self.top.resizable(False, False)
        self.top.transient(parent)
        self.top.grab_set()

        all_coins = {
            "bitcoin": ("BTC", "Bitcoin"),
            "ethereum": ("ETH", "Ethereum"),
            "tether": ("USDT", "Tether"),
            "solana": ("SOL", "Solana"),
            "binancecoin": ("BNB", "BNB"),
            "the-open-network": ("TON", "Toncoin"),
            "ripple": ("XRP", "XRP"),
            "cardano": ("ADA", "Cardano"),
            "dogecoin": ("DOGE", "Dogecoin"),
            "usd": ("USD", "Доллар США"),
            "eur": ("EUR", "Евро"),
            "rub": ("RUB", "Российский рубль")
        }

        self.coins = {}
        for coin_id in selected_ids:
            if coin_id in all_coins:
                self.coins[coin_id] = all_coins[coin_id]

        # Всегда добавляем фиатные валюты
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

    def fetch_rates(self):
        crypto_ids = [k for k in self.coins.keys() if k not in ("usd", "eur", "rub")]
        if not crypto_ids:
            return

        ids_str = ",".join(crypto_ids)
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids_str}&vs_currencies=usd,eur,rub"

        try:
            res = requests.get(url, timeout=5).json()

            for coin_id, prices in res.items():
                if "usd" in prices: self.rates[f"{coin_id}_usd"] = prices["usd"]
                if "eur" in prices: self.rates[f"{coin_id}_eur"] = prices["eur"]
                if "rub" in prices: self.rates[f"{coin_id}_rub"] = prices["rub"]

            self.rates["usd_usd"] = 1.0
            self.rates["eur_eur"] = 1.0
            self.rates["rub_rub"] = 1.0

            self.rates["usd_eur"] = 1.0 / self.rates.get("bitcoin_eur", 1) * self.rates.get("bitcoin_usd",
                                                                                            1) if "bitcoin_eur" in self.rates else 0.92
            self.rates["eur_usd"] = 1.0 / self.rates["usd_eur"] if self.rates["usd_eur"] else 1.08
            self.rates["usd_rub"] = self.rates.get("bitcoin_rub", 90.0) / self.rates.get("bitcoin_usd",
                                                                                         1.0) if "bitcoin_rub" in self.rates else 90.0
            self.rates["rub_usd"] = 1.0 / self.rates["usd_rub"] if self.rates["usd_rub"] else 0.011
            self.rates["eur_rub"] = self.rates["usd_rub"] / self.rates["usd_eur"] if self.rates["usd_eur"] else 100.0
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
        tk.Label(self.top, text="Конвертация", font=("Segoe UI", 14, "bold"),
                 bg="#F3F3F3", fg="#212121").pack(pady=(15, 10))

        # Блок "Продаю" с увеличенными отступами
        self.from_frame = self.create_block("Продаю", "USDT", is_from=True)
        self.from_frame.pack(fill="x", padx=25, pady=(5, 15))

        # Кнопка Swap в стиле первой кнопки
        swap_btn = tk.Button(
            self.top,
            text="⇅ Поменять",
            command=self.swap,
            bg="#0078D7",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=15, pady=5,
            relief="flat",
            cursor="hand2"
        )
        swap_btn.pack(pady=5)

        # Блок "Покупаю" с увеличенными отступами
        self.to_frame = self.create_block("Покупаю", "BTC", is_from=False)
        self.to_frame.pack(fill="x", padx=25, pady=(5, 20))

        # Результаты в USD и RUB
        self.result_frame = tk.Frame(self.top, bg="#F3F3F3")
        self.result_frame.pack(fill="x", padx=25)

        self.usd_label = tk.Label(self.result_frame, text="≈ $ 0,00", font=("Segoe UI", 12, "bold"), bg="#F3F3F3",
                                  fg="#212121")
        self.usd_label.pack(anchor="e")

        self.rub_label = tk.Label(self.result_frame, text="≈ ₽ 0,00", font=("Segoe UI", 12, "bold"), bg="#F3F3F3",
                                  fg="#212121")
        self.rub_label.pack(anchor="e")

    def create_block(self, title, default_coin, is_from):
        frame = tk.Frame(self.top, bg="#FFFFFF", highlightthickness=1, highlightbackground="#DDD")

        # Увеличенные внутренние отступы
        tk.Label(frame, text=title, font=("Segoe UI", 9), bg="#FFFFFF", fg="#666").pack(anchor="w", padx=12,
                                                                                        pady=(10, 2))

        row = tk.Frame(frame, bg="#FFFFFF")
        row.pack(fill="x", padx=12, pady=(0, 15))

        coin_values = [f"{v[0]} - {v[1]}" for k, v in self.coins.items()]
        combo = ttk.Combobox(row, values=coin_values, width=14, state="readonly")
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

        entry = tk.Entry(
            row,
            font=("Consolas", 16, "bold"),
            bg="#000000",
            fg="#00FF00",
            insertbackground="#00FF00",
            selectbackground="#004400",
            selectforeground="#00FF00",
            bd=0,
            justify="right",
            validate="key",
            validatecommand=(self.top.register(self.validate_number), "%P")
        )
        entry.pack(side="right", fill="x", expand=True)

        if is_from:
            self.from_combo = combo
            self.from_entry = entry
            entry.insert(0, "1")
            entry.bind("<KeyRelease>", self.calculate)
            combo.bind("<<ComboboxSelected>>", lambda e: self.calculate())
        else:
            self.to_combo = combo
            self.to_entry = entry
            entry.config(state="readonly", readonlybackground="#000000", fg="#00FF00")

        return frame

    def get_id_by_ticker(self, ticker):
        for k, v in self.coins.items():
            if v[0] == ticker:
                return k
        return None

    def calculate(self, event=None):
        try:
            amount_str = self.from_entry.get().replace(",", ".")
            if not amount_str: return
            amount = float(amount_str)

            from_ticker = self.from_combo.get().split(" - ")[0]
            to_ticker = self.to_combo.get().split(" - ")[0]

            from_id = self.get_id_by_ticker(from_ticker)
            to_id = self.get_id_by_ticker(to_ticker)

            if not from_id or not to_id: return

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

            usd_str = f"{total_usd:,.2f}".replace(".", ",")
            self.usd_label.config(text=f"≈ $ {usd_str}")

            rub_total = total_usd * self.rates.get("usd_rub", 90.0)
            rub_str = f"{rub_total:,.2f}".replace(".", ",")
            self.rub_label.config(text=f"≈ ₽ {rub_str}")

        except ValueError:
            pass

    def swap(self):
        if not hasattr(self, 'from_combo') or not self.from_combo:
            return

        from_val = self.from_combo.get()
        to_val = self.to_combo.get()
        self.from_combo.set(to_val)
        self.to_combo.set(from_val)
        self.calculate()


# ==========================================
# ЗАПУСК
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = RatesWindow(root)
    root.mainloop()