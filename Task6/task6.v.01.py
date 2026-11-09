import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime, timezone


class CryptoCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор криптовалют (CoinGecko)")
        self.root.geometry("450x500")
        self.root.configure(bg="#F3F3F3")

        # Словарь популярных монет (ID в API CoinGecko : Отображаемое название)
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

        self.setup_ui()

    def setup_ui(self):
        # Заголовок
        header = tk.Label(self.root, text="Курсы криптовалют к USD",
                          font=("Segoe UI", 14, "bold"), bg="#F3F3F3", fg="#212121")
        header.pack(pady=10)

        # Фрейм для кнопок выбора (чекбоксы)
        selection_frame = tk.LabelFrame(self.root, text="Выберите монеты:",
                                        bg="#F3F3F3", font=("Segoe UI", 10))
        selection_frame.pack(fill="x", padx=20, pady=5)

        self.coin_vars = {}
        for i, (coin_id, coin_name) in enumerate(self.coins.items()):
            var = tk.BooleanVar(value=True)  # По умолчанию все выбраны
            self.coin_vars[coin_id] = var
            chk = tk.Checkbutton(selection_frame, text=coin_name, variable=var,
                                 bg="#F3F3F3", font=("Segoe UI", 9))
            # Размещаем в 2 колонки
            row = i // 2
            col = i % 2
            chk.grid(row=row, column=col, sticky="w", padx=10, pady=2)

        # Кнопка запроса
        btn_frame = tk.Frame(self.root, bg="#F3F3F3")
        btn_frame.pack(pady=10)

        self.btn_get = tk.Button(btn_frame, text="Запросить курсы", command=self.get_rates,
                                 bg="#0078D7", fg="white", font=("Segoe UI", 10, "bold"),
                                 padx=15, pady=5, relief="flat", cursor="hand2")
        self.btn_get.pack()

        # Таблица (Treeview) для вывода
        columns = ("coin", "price", "change")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=8)
        self.tree.heading("coin", text="Монета")
        self.tree.heading("price", text="Цена (USD)")
        self.tree.heading("change", text="Изм. за 24ч (%)")

        self.tree.column("coin", width=150, anchor="w")
        self.tree.column("price", width=100, anchor="e")
        self.tree.column("change", width=100, anchor="e")

        self.tree.pack(fill="both", expand=True, padx=20, pady=5)

        # Метка времени
        self.time_label = tk.Label(self.root, text="Ожидание запроса...",
                                   font=("Segoe UI", 8), bg="#F3F3F3", fg="#666")
        self.time_label.pack(pady=5)

    def get_rates(self):
        # Очищаем таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Собираем выбранные ID
        selected_coins = [coin_id for coin_id, var in self.coin_vars.items() if var.get()]

        if not selected_coins:
            messagebox.showwarning("Внимание", "Выберите хотя бы одну валюту!")
            return

        # Формируем запрос к API
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

                    # Форматируем цену (если больше 1, то 2 знака, если меньше - 4 знака)
                    if price >= 1:
                        price_str = f"${price:,.2f}"
                    else:
                        price_str = f"${price:,.4f}"

                    # Окрашиваем изменение (зеленый/красный)
                    change_str = f"{change:.2f}%" if change is not None else "—"

                    self.tree.insert("", "end", values=(name, price_str, change_str))

            # Обновляем время
            now = datetime.now(timezone.utc).astimezone().strftime("%d.%m.%Y %H:%M:%S")
            self.time_label.config(text=f"Последнее обновление: {now} (МСК)")

        except requests.exceptions.Timeout:
            messagebox.showerror("Ошибка", "Превышено время ожидания ответа от API.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка сети", f"Не удалось получить данные:\n{e}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла непредвиденная ошибка:\n{e}")
        finally:
            self.btn_get.config(state="normal", text="Запросить курсы")


if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoCalculatorApp(root)
    root.mainloop()