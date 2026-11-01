import requests
from bs4 import BeautifulSoup

def get_main(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Ошибка {response.status_code}: {url}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    name_tag = soup.find('h1', class_='person-caption')
    name = name_tag.text.strip() if name_tag else "Имя не найдено"

    pos_tag = soup.find('span', class_='person-appointment-title')
    pos = pos_tag.text.strip() if pos_tag else "Должность не найдена"

    print(f"Имя: {name}")
    print(f"Должность: {pos}")
    print("-" * 40)

# Список адресов
pul_address = [
    'https://www.hse.ru/staff/allat/',
    'https://www.hse.ru/org/persons/135897',
    'https://www.hse.ru/org/persons/63890353',
]

# Перебор адресов в цикле
for url in pul_address:
    get_main(url)