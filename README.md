# Конвертер валют (две базовые валюты)

GUI-приложение на Python/Tkinter для получения актуальных курсов обмена валют
через API **open.er-api.com** (ExchangeRate-API). Поддерживает **две базовые валюты**
одновременно и выводит курсы в биржевом формате `BASE/QUOTE`.

![Главное окно](docs/screenshot-main.png)
![Окно результатов](docs/screenshot-result.png)

## Возможности

- Две базовые валюты + одна целевая — сразу два курса
- Биржевой формат `USD/RUB`, точность 4 знака (2 для JPY)
- Время получения (локальное и МСК) и проверка актуальности данных
- Тёмное окно результатов с копированием курсов (кнопка / ПКМ / двойной клик)
- Сохранение результатов в `.txt` с параметрами запроса
- Лог всех запросов в `history.json` и `history.csv`
- Metro UI: светлый интерфейс, акцентные кнопки, тёмная шапка

## Требования

- Python 3.10+
- `requests`

```bash
git clone https://github.com/maximlyubomirov-cloud/PythonProject.Osnovanie.git
cd PythonProject.Osnovanie
pip install requests
python currency_converter.py
```