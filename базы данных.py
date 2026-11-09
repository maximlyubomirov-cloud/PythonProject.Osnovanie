import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Car (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    name   TEXT,
    model  TEXT,
    year   INTEGER,
    activ  INTEGER,
    amount REAL
);''')

cursor.executemany('''INSERT INTO Car (name, model, year, activ, amount)
    VALUES (?,?,?,?,?)''', [
    ('LADA',   '2106', 1979, 1, 100.0),
    ('Mazda',  '3',    2019, 1, 250.0),
    ('Moskvich','412', 1975, 0, 50.0),
    ('Mazda',  '6',    2021, 1, 300.0),
])
conn.commit()

# Grouped aggregate
cursor.execute('''SELECT name, SUM(amount) FROM Car GROUP BY name;''')
for row in cursor.fetchall():
    print(row)

conn.close()