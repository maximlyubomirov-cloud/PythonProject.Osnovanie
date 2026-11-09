import tkinter as tk
from tkinter import messagebox

def validate_input(new_value):
    """
    Разрешает ввод только цифр.
    Возвращает True, если ввод допустим, и False — если нет.
    """
    # Пустая строка допустима (пользователь стирает всё поле)
    if new_value == "":
        return True
    # Разрешаем только последовательность цифр
    return new_value.isdigit()

def calculate_sum():
    """Вычисляет сумму трёх чисел."""
    try:
        num1 = int(entry1.get())
        num2 = int(entry2.get())
        num3 = int(entry3.get())
        result = num1 + num2 + num3
        messagebox.showinfo("Результат", f"Сумма трёх чисел = {result}")
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все три поля!")

def calculate_product():
    """Вычисляет произведение трёх чисел."""
    try:
        num1 = int(entry1.get())
        num2 = int(entry2.get())
        num3 = int(entry3.get())
        result = num1 * num2 * num3
        messagebox.showinfo("Результат", f"Произведение трёх чисел = {result}")
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все три поля!")

# Создаём главное окно
root = tk.Tk()
root.title("Калькулятор")
root.geometry("400x320")

# Регистрируем функцию валидации
vcmd = (root.register(validate_input), '%P')

# Текстовая подсказка
label = tk.Label(root, text="Введите три числа и нажмите на кнопку для вычисления")
label.pack(pady=10)

# Три поля ввода с валидацией
entry1 = tk.Entry(root, width=30, validate="key", validatecommand=vcmd)
entry1.pack(pady=5)

entry2 = tk.Entry(root, width=30, validate="key", validatecommand=vcmd)
entry2.pack(pady=5)

entry3 = tk.Entry(root, width=30, validate="key", validatecommand=vcmd)
entry3.pack(pady=5)

# Кнопка "Сложить три числа"
btn_sum = tk.Button(root, text="Сложить три числа", width=25, command=calculate_sum)
btn_sum.pack(pady=10)

# Кнопка "Умножить три числа"
btn_product = tk.Button(root, text="Умножить три числа", width=25, command=calculate_product)
btn_product.pack(pady=5)

# Запуск приложения
root.mainloop()
