# crypto_tracker.py
# Приложение для отображения курсов криптовалют
# Python 3 + Tkinter + requests + CoinGecko API

import json
import threading
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox

import requests


# ----------------------------- Конфигурация -----------------------------

API_URL = "https://api.coingecko.com/api/v3/simple/price"

# Список отслеживаемых криптовалют:
# (ID в CoinGecko, тикер, отображаемое название)
COINS = [
    ("bitcoin", "BTC", "Bitcoin"),
    ("ethereum", "ETH", "Ethereum"),
    ("binancecoin", "BNB", "BNB"),
    ("solana", "SOL", "Solana"),
    ("ripple", "XRP", "XRP"),
    ("cardano", "ADA", "Cardano"),
    ("dogecoin", "DOGE", "Dogecoin"),
    ("polkadot", "DOT", "Polkadot"),
    ("chainlink", "LINK", "Chainlink"),
    ("avalanche-2", "AVAX", "Avalanche"),
]

AUTO_REFRESH_MS = 60_000  # автообновление раз в 60 секунд
REQUEST_TIMEOUT = 10      # таймаут запроса, секунд


# ----------------------------- Работа с API -----------------------------

class CryptoAPI:
    """Класс для загрузки курсов криптовалют через CoinGecko API."""

    def __init__(self, url: str, coins: list[tuple[str, str, str]]):
        self.url = url
        self.coins = coins
        self.coin_ids = [coin[0] for coin in coins]

    def fetch_prices(self) -> dict:
        """
        Загружает курсы и возвращает словарь:
        {coin_id: {"usd": float, "usd_24h_change": float}}
        """
        params = {
            "ids": ",".join(self.coin_ids),
            "vs_currencies": "usd",
            "include_24hr_change": "true",
            "include_24hr_vol": "true",
        }

        try:
            response = requests.get(
                self.url,
                params=params,
                timeout=REQUEST_TIMEOUT,
                headers={"Accept": "application/json"},
            )
            response.raise_for_status()
        except requests.exceptions.Timeout as exc:
            raise RuntimeError("Превышено время ожидания ответа API.") from exc
        except requests.exceptions.ConnectionError as exc:
            raise RuntimeError(
                "Нет соединения с API. Проверьте подключение к интернету."
            ) from exc
        except requests.exceptions.HTTPError as exc:
            status = exc.response.status_code if exc.response is not None else "?"
            if status == 429:
                raise RuntimeError(
                    "Превышен лимит запросов к API. Подождите и повторите."
                ) from exc
            raise RuntimeError(f"Ошибка HTTP: {status}.") from exc
        except requests.exceptions.RequestException as exc:
            raise RuntimeError(f"Ошибка сетевого запроса: {exc}") from exc

        try:
            data = response.json()
        except (ValueError, json.JSONDecodeError) as exc:
            raise RuntimeError("API вернул некорректный JSON.") from exc

        if not isinstance(data, dict) or not data:
            raise RuntimeError("API вернул пустой или неожиданный ответ.")

        return data


# ----------------------------- GUI -----------------------------

class CryptoApp(tk.Tk):
    """Главное окно приложения."""

    def __init__(self):
        super().__init__()
        self.title("Курсы криптовалют")
        self.geometry("880x460")
        self.minsize(760, 360)

        self.api = CryptoAPI(API_URL, COINS)
        self.is_loading = False
        self.after_id = None

        self._build_ui()
        self._schedule_auto_refresh()
        self.refresh_data()

    # ---------- Построение интерфейса ----------

    def _build_ui(self):
        # Верхняя панель
        top_frame = ttk.Frame(self, padding=(10, 8))
        top_frame.pack(fill="x")

        title_label = ttk.Label(
            top_frame,
            text="Курсы криптовалют",
            font=("Segoe UI", 16, "bold"),
        )
        title_label.pack(side="left")

        self.refresh_button = ttk.Button(
            top_frame,
            text="Обновить",
            command=self.refresh_data,
        )
        self.refresh_button.pack(side="right")

        # Таблица
        table_frame = ttk.Frame(self, padding=(10, 0))
        table_frame.pack(fill="both", expand=True)

        columns = ("id", "symbol", "name", "price", "change")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        headings = {
            "id": "ID",
            "symbol": "Тикер",
            "name": "Название",
            "price": "Цена (USD)",
            "change": "24ч (%)",
        }
        widths = {
            "id": 150,
            "symbol": 80,
            "name": 160,
            "price": 140,
            "change": 100,
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            anchor = "e" if col in ("price", "change") else "w"
            self.tree.column(col, width=widths[col], anchor=anchor, stretch=True)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Статусная строка
        status_frame = ttk.Frame(self, padding=(10, 6))
        status_frame.pack(fill="x")

        self.status_var = tk.StringVar(value="Готово")
        self.updated_var = tk.StringVar(value="")

        ttk.Label(
            status_frame,
            textvariable=self.status_var,
            anchor="w",
        ).pack(side="left", fill="x", expand=True)

        ttk.Label(
            status_frame,
            textvariable=self.updated_var,
            anchor="e",
        ).pack(side="right")

    # ---------- Обновление данных ----------

    def refresh_data(self):
        """Запускает загрузку данных в отдельном потоке."""
        if self.is_loading:
            return

        self.is_loading = True
        self.refresh_button.configure(state="disabled")
        self.status_var.set("Загрузка данных...")

        thread = threading.Thread(target=self._load_data_worker, daemon=True)
        thread.start()

    def _load_data_worker(self):
        """Фоновый поток: запрос к API и передача результата в GUI."""
        try:
            data = self.api.fetch_prices()
            self.after(0, self._on_success, data)
        except Exception as exc:  # noqa: BLE001 — намеренно широкий перехват для GUI
            self.after(0, self._on_error, str(exc))

    def _on_success(self, data: dict):
        """Обновляет таблицу после успешной загрузки."""
        self.tree.delete(*self.tree.get_children())

        for coin_id, symbol, name in COINS:
            coin_data = data.get(coin_id, {})
            price = coin_data.get("usd")
            change = coin_data.get("usd_24h_change")

            price_text = f"{price:,.2f}" if isinstance(price, (int, float)) else "—"

            if isinstance(change, (int, float)):
                change_text = f"{change:+.2f}"
            else:
                change_text = "—"

            self.tree.insert(
                "",
                "end",
                values=(coin_id, symbol, name, price_text, change_text),
            )

        now = datetime.now().strftime("%H:%M:%S")
        self.status_var.set("Данные обновлены.")
        self.updated_var.set(f"Последнее обновление: {now}")

        self._finish_loading()

    def _on_error(self, message: str):
        """Обрабатывает ошибку загрузки, не закрывая приложение."""
        self.status_var.set(f"Ошибка: {message}")
        self._finish_loading()

    def _finish_loading(self):
        self.is_loading = False
        self.refresh_button.configure(state="normal")

    # ---------- Автообновление ----------

    def _schedule_auto_refresh(self):
        """Планирует следующее автообновление через after."""
        if self.after_id is not None:
            self.after_cancel(self.after_id)
        self.after_id = self.after(AUTO_REFRESH_MS, self._auto_refresh_tick)

    def _auto_refresh_tick(self):
        self.refresh_data()
        self._schedule_auto_refresh()

    def destroy(self):
        """Отменяет таймер при закрытии окна."""
        if self.after_id is not None:
            try:
                self.after_cancel(self.after_id)
            except tk.TclError:
                pass
        super().destroy()


# ----------------------------- Точка входа -----------------------------

if __name__ == "__main__":
    app = CryptoApp()
    app.mainloop()