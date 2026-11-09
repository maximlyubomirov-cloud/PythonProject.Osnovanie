import sqlite3

# Подключаемся к базе
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# 1. УДАЛЯЕМ старую таблицу, чтобы начать с чистого листа
cursor.execute('DROP TABLE IF EXISTS Car')

# 2. СОЗДАЕМ таблицу заново с правильными типами данных
cursor.execute('''
CREATE TABLE Car (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    model TEXT,
    year INTEGER
)
''')

# 3. Данные, которые вы хотите видеть (из вашего скриншота)
cars_data = [
    ('Volga', 'gaz-2410', 1985),
    ('Mercedes', '222', 2017),
    ('Moskvich', '412', 1979),
    ('LADA', '2106', 1979),
    ('Toyota', 'Corolla', 2019)
]

# 4. ВСТАВЛЯЕМ данные массово (executemany)
cursor.executemany('''
INSERT INTO Car (name, model, year) 
VALUES (?, ?, ?)
''', cars_data)

# Сохраняем изменения
conn.commit()

# 5. ПРОВЕРЯЕМ результат с красивым выводом
cursor.execute('SELECT * FROM Car')
rows = cursor.fetchall()

print(f"{'ID':<4} | {'Name':<12} | {'Model':<12} | {'Year'}")
print("-" * 45)
for row in rows:
    print(f"{row[0]:<4} | {row[1]:<12} | {row[2]:<12} | {row[3]}")

conn.close()