from pathlib import Path

# 1. Проверяем, что исходный файл существует
if not Path('text.txt').exists():
    print('Ошибка: файл text.txt не найден!')
    exit()

# 2. Читаем файл
with open('text.txt', 'r', encoding='utf-8') as f:
    s = f.read()

# 3. Запрашиваем ключ с проверкой
try:
    key = int(input('Введите ключ шифрования: '))
except ValueError:
    print('Ошибка: ключ должен быть целым числом!')
    exit()

# 4. Шифруем
secret = ''
for c in s:
    code = ord(c) + key
    if code > 0x10FFFF:        # защита от переполнения
        code -= 0x110000
    secret += chr(code)

print('Текст зашифрован!')

# 5. Сохраняем результат
with open('code.txt', 'w', encoding='utf-8') as f:
    f.write(secret)

print('Файл "code.txt" для отправки сформирован.')