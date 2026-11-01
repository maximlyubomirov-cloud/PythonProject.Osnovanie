# ============================================================
# ГРАФИЧЕСКИЙ ИНТЕРФЕЙС ДЛЯ ШИФРА ЦЕЗАРЯ (tkinter)
# Поддержка русского и английского алфавита.
# Буквы сдвигаются внутри алфавита, пробелы и знаки
# препинания остаются без изменений.
# ============================================================

import tkinter as tk
from tkinter import messagebox


# ------------------------------------------------------------
# АЛФАВИТЫ
# ------------------------------------------------------------
RU_UPPER = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
RU_LOWER = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
EN_UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
EN_LOWER = 'abcdefghijklmnopqrstuvwxyz'


# ------------------------------------------------------------
# ФУНКЦИЯ ШИФРА ЦЕЗАРЯ
# ------------------------------------------------------------
def caesar(text, key, mode='encrypt'):
    """
    Шифр Цезаря для русского и английского алфавита.
    mode='encrypt' — сдвиг вперёд (+key)
    mode='decrypt' — сдвиг назад (-key)
    Пробелы, цифры и знаки препинания не меняются.
    """
    if mode == 'decrypt':
        key = -key

    result = ''
    for c in text:
        if c in RU_UPPER:
            i = RU_UPPER.index(c)
            result += RU_UPPER[(i + key) % len(RU_UPPER)]
        elif c in RU_LOWER:
            i = RU_LOWER.index(c)
            result += RU_LOWER[(i + key) % len(RU_LOWER)]
        elif c in EN_UPPER:
            i = EN_UPPER.index(c)
            result += EN_UPPER[(i + key) % len(EN_UPPER)]
        elif c in EN_LOWER:
            i = EN_LOWER.index(c)
            result += EN_LOWER[(i + key) % len(EN_LOWER)]
        else:
            result += c   # пробелы, цифры, знаки — без изменений
    return result


# ------------------------------------------------------------
# ФУНКЦИЯ ШИФРОВАНИЯ
# ------------------------------------------------------------
def encrypt():
    text = input_text.get('1.0', tk.END).rstrip('\n')

    if not text:
        messagebox.showwarning('Внимание', 'Введите текст для шифрования!')
        return

    try:
        key = int(key_entry.get())
    except ValueError:
        messagebox.showerror('Ошибка', 'Ключ должен быть целым числом!')
        return

    secret = caesar(text, key, mode='encrypt')

    output_text.delete('1.0', tk.END)
    output_text.insert('1.0', secret)

    with open('text_secret.txt', 'w', encoding='utf-8') as f:
        f.write(secret)

    status_label.config(text='✅ Текст зашифрован и сохранён в text_secret.txt')


# ------------------------------------------------------------
# ФУНКЦИЯ РАСШИФРОВКИ
# ------------------------------------------------------------
def decrypt():
    text = input_text.get('1.0', tk.END).rstrip('\n')

    if not text:
        messagebox.showwarning('Внимание', 'Введите текст для расшифровки!')
        return

    try:
        key = int(key_entry.get())
    except ValueError:
        messagebox.showerror('Ошибка', 'Ключ должен быть целым числом!')
        return

    original = caesar(text, key, mode='decrypt')

    output_text.delete('1.0', tk.END)
    output_text.insert('1.0', original)

    with open('text_decrypted.txt', 'w', encoding='utf-8') as f:
        f.write(original)

    status_label.config(text='✅ Текст расшифрован и сохранён в text_decrypted.txt')


# ------------------------------------------------------------
# ФУНКЦИЯ ОЧИСТКИ ПОЛЕЙ
# ------------------------------------------------------------
def clear_all():
    input_text.delete('1.0', tk.END)
    output_text.delete('1.0', tk.END)
    key_entry.delete(0, tk.END)
    key_entry.insert(0, '3')
    status_label.config(text='')


# ------------------------------------------------------------
# КОПИРОВАНИЕ РЕЗУЛЬТАТА В БУФЕР ОБМЕНА
# ------------------------------------------------------------
def copy_result():
    result = output_text.get('1.0', tk.END).rstrip('\n')
    if not result:
        messagebox.showinfo('Информация', 'Результат пуст — нечего копировать.')
        return
    root.clipboard_clear()
    root.clipboard_append(result)
    status_label.config(text='📋 Результат скопирован в буфер обмена')


# ============================================================
# СОЗДАНИЕ ОКНА
# ============================================================
root = tk.Tk()
root.title('Шифр Цезаря')
root.geometry('700x600')
root.configure(bg='#f0f0f0')


# ----- ЗАГОЛОВОК -----
tk.Label(
    root,
    text='🔐 Шифр Цезаря',
    font=('Arial', 18, 'bold'),
    bg='#f0f0f0',
    fg='#333333'
).pack(pady=10)


# ----- ПОЛЕ ВВОДА ТЕКСТА -----
tk.Label(
    root,
    text='Введите текст:',
    font=('Arial', 11),
    bg='#f0f0f0',
    anchor='w'
).pack(fill='x', padx=20)

input_text = tk.Text(
    root,
    height=6,
    font=('Consolas', 11),
    wrap='word',
    bg='white',
    fg='#000000',
    insertbackground='black'
)
input_text.pack(fill='x', padx=20, pady=(0, 10))


# ----- ПОЛЕ ДЛЯ КЛЮЧА -----
key_frame = tk.Frame(root, bg='#f0f0f0')
key_frame.pack(fill='x', padx=20)

tk.Label(
    key_frame,
    text='Ключ шифрования:',
    font=('Arial', 11),
    bg='#f0f0f0'
).pack(side='left')

key_entry = tk.Entry(
    key_frame,
    width=10,
    font=('Arial', 11),
    justify='center'
)
key_entry.pack(side='left', padx=10)
key_entry.insert(0, '3')   # значение по умолчанию


# ----- КНОПКИ -----
button_frame = tk.Frame(root, bg='#f0f0f0')
button_frame.pack(pady=15)

tk.Button(
    button_frame,
    text='🔒 Зашифровать',
    font=('Arial', 11, 'bold'),
    bg='#4CAF50',
    fg='white',
    activebackground='#45a049',
    width=15,
    command=encrypt
).pack(side='left', padx=5)

tk.Button(
    button_frame,
    text='🔓 Расшифровать',
    font=('Arial', 11, 'bold'),
    bg='#2196F3',
    fg='white',
    activebackground='#1976D2',
    width=15,
    command=decrypt
).pack(side='left', padx=5)

tk.Button(
    button_frame,
    text='🗑 Очистить',
    font=('Arial', 11, 'bold'),
    bg='#f44336',
    fg='white',
    activebackground='#d32f2f',
    width=12,
    command=clear_all
).pack(side='left', padx=5)


# ----- ПОЛЕ ВЫВОДА РЕЗУЛЬТАТА -----
tk.Label(
    root,
    text='Результат:',
    font=('Arial', 11),
    bg='#f0f0f0',
    anchor='w'
).pack(fill='x', padx=20)

output_text = tk.Text(
    root,
    height=6,
    font=('Consolas', 11),
    wrap='word',
    bg='#fffde7',
    fg='#000000',
    insertbackground='black'
)
output_text.pack(fill='x', padx=20, pady=(0, 10))


# ----- КНОПКА КОПИРОВАНИЯ -----
tk.Button(
    root,
    text='📋 Скопировать результат',
    font=('Arial', 10),
    bg='#9E9E9E',
    fg='white',
    activebackground='#757575',
    command=copy_result
).pack(pady=5)


# ----- СТРОКА СОСТОЯНИЯ -----
status_label = tk.Label(
    root,
    text='',
    font=('Arial', 10, 'italic'),
    bg='#f0f0f0',
    fg='#555555'
)
status_label.pack(pady=5)


# ============================================================
# ЗАПУСК ОКНА
# ============================================================
root.mainloop()