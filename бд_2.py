import sqlite3

conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

# --- СОЗДАЕМ ТАБЛИЦУ (если её нет) ---
cursor.execute('''
CREATE TABLE IF NOT EXISTS Car (
    id INTEGER PRIMARY KEY,
    name TEXT,
    model TEXT,
    year INTEGER
)
''')
# -------------------------------------

# И добавим пару тестовых данных, чтобы запрос что-то нашел
cursor.execute("INSERT INTO Car (name, model, year) VALUES ('Mazda', '6', 2015)")
cursor.execute("INSERT INTO Car (name, model, year) VALUES ('BMW', 'X5', 2019)")
conn.commit() # сохраняем изменения

# --- ВАШ ЗАПРОС ---
cursor.execute('''SELECT name, model, year FROM Car
WHERE year BETWEEN 1970 and 2020 ORDER BY name DESC LIMIT 3 OFFSET 1;''')

rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()