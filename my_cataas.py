from tkinter import *
from tkinter import messagebox
from io import BytesIO
from PIL import Image, ImageTk
import requests


def load_image(url, retries=3):
    """Загружает изображение по URL и возвращает объект PhotoImage."""
    for attempt in range(retries):
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            image_data = BytesIO(resp.content)
            pil_image = Image.open(image_data)
            pil_image.thumbnail((600, 480), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(pil_image)
        except Exception as er:
            print(f'Попытка {attempt + 1}: Ошибка', er)
    return None


def update_cat(url='https://cataas.com/cat'):
    """Обновляет картинку в главном окне."""
    label.configure(text='Загрузка...', image='')
    root.update()

    img = load_image(url)

    if img:
        label.configure(image=img, text='')
        label.image = img  # Сохраняем ссылку, чтобы картинка не исчезла
    else:
        label.configure(text='Не удалось загрузить котика 😿', image='')


def open_new_window():
    """Открывает новое окно с котиком по тегу из поля ввода."""
    tag = tag_entry.get().strip()

    # Формируем URL (без дублирования тега!)
    if tag:
        url = f'https://cataas.com/cat/{tag}'
    else:
        url = 'https://cataas.com/cat'

    img = load_image(url)

    if img:
        new_window = Toplevel(root)
        new_window.title('Картинка с котиком')
        new_window.geometry('620x520')

        new_label = Label(new_window, image=img)
        new_label.image = img  # Критически важно: сохраняем ссылку!
        new_label.pack(pady=10)
    else:
        messagebox.showerror("Ошибка", "Не удалось загрузить котика по этому тегу 😿")


def search_by_tag():
    """Ищет котика по тегу в главном окне."""
    tag = tag_entry.get().strip()
    if tag:
        update_cat(f'https://cataas.com/cat/{tag}')
    else:
        update_cat('https://cataas.com/cat')


def on_exit():
    """Корректный выход из приложения."""
    root.destroy()


# --- Главное окно ---
root = Tk()
root.title('Cats')
root.geometry('620x550')

# --- Меню ---
menu_bar = Menu(root)
root.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Файл', menu=file_menu)
file_menu.add_command(label='Загрузить фото', command=open_new_window)
file_menu.add_separator()
file_menu.add_command(label='Выход', command=on_exit)

# --- Основной интерфейс ---
label = Label(root, text="Нажмите 'Файл -> Загрузить фото' или введите тег")
label.pack(pady=20)

btn_refresh = Button(root, text='Случайный котик',
                     command=lambda: update_cat('https://cataas.com/cat'))
btn_refresh.pack(pady=10)

Label(root, text="Введите тег для поиска (например, 'cute'):").pack(pady=(20, 5))
tag_entry = Entry(root, width=30)
tag_entry.pack()

Button(root, text='Найти по тегу', command=search_by_tag).pack(pady=5)

# Загружаем первого котика при старте
update_cat()

root.mainloop()