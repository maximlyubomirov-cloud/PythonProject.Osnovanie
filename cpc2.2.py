import tkinter as tk

# --- Создание окна ---
root = tk.Tk()
root.title("Рисование фигур")
root.geometry("400x650")
root.configure(bg="#f0f0f0")

# --- Холст ---
canvas = tk.Canvas(root, width=300, height=200, bg="salmon")
canvas.pack(pady=10)

# =========================================================
#  ФУНКЦИИ РИСОВАНИЯ ФИГУР
# =========================================================

def draw_circle():
    """Рисует окружность на холсте."""
    fill = fill_entry.get().strip() or "lightblue"
    outline = outline_entry.get().strip() or "blue"
    # Координаты: x0, y0, x1, y1 — описывают прямоугольник, в который вписана окружность
    canvas.create_oval(50, 30, 150, 130, fill=fill, outline=outline, width=2)


def draw_square():
    """Рисует квадрат на холсте."""
    fill = fill_entry.get().strip() or "lightblue"
    outline = outline_entry.get().strip() or "blue"
    canvas.create_rectangle(50, 30, 150, 130, fill=fill, outline=outline, width=2)


def draw_triangle():
    """Рисует треугольник на холсте (равнобедренный)."""
    fill = fill_entry.get().strip() or "lightblue"
    outline = outline_entry.get().strip() or "blue"
    # Три вершины треугольника: (x0,y0), (x1,y1), (x2,y2)
    points = [100, 20,   40, 140,   160, 140]
    canvas.create_polygon(points, fill=fill, outline=outline, width=2)


def clear_canvas():
    """Очищает холст от всех фигур."""
    canvas.delete("all")


# =========================================================
#  ФУНКЦИЯ ИЗМЕНЕНИЯ ЦВЕТА ФОНА
# =========================================================

def change_background():
    """Меняет цвет фона холста."""
    color = bg_entry.get().strip()
    if color:
        try:
            canvas.config(bg=color)
        except tk.TclError:
            print(f"Некорректный цвет: {color}")


# =========================================================
#  ИНТЕРФЕЙС
# =========================================================

# --- Кнопки рисования фигур ---
tk.Button(root, text="Окружность", width=20, command=draw_circle).pack(pady=3)
tk.Button(root, text="Треугольник", width=20, command=draw_triangle).pack(pady=3)
tk.Button(root, text="Квадрат", width=20, command=draw_square).pack(pady=3)
tk.Button(root, text="Очистить", width=20, command=clear_canvas).pack(pady=3)

# --- Поле ввода: цвет заливки ---
tk.Label(root, text="Цвет заливки:").pack()
fill_entry = tk.Entry(root)
fill_entry.insert(0, "lightblue")
fill_entry.pack()

# --- Поле ввода: цвет обводки ---
tk.Label(root, text="Цвет обводки:").pack()
outline_entry = tk.Entry(root)
outline_entry.insert(0, "blue")
outline_entry.pack()

# --- Поле ввода: цвет фона ---
tk.Label(root, text="Цвет фона:").pack()
bg_entry = tk.Entry(root)
bg_entry.insert(0, "white")
bg_entry.pack()

# --- Кнопка изменения цвета фона ---
tk.Button(root, text="Изменить цвет фона", width=20, command=change_background).pack(pady=5)

# --- Запуск ---
root.mainloop()