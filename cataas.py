from tkinter import *
from tkinter import messagebox
from io import BytesIO
from PIL import Image, ImageTk
import requests


def load_image(url):
    """Загружает картинку по URL."""
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        image_data = BytesIO(resp.content)
        img = Image.open(image_data)
        img.thumbnail((600, 480), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as er:
        print('Ошибка', er)
        return None


def set_image(url='https://cataas.com/cat'):
    """Загружает картинку в главное окно."""
    label.configure(text='Загрузка...', image='')
    root.update()  # Принудительно обновляем интерфейс

    img = load_image(url)
    if img:
        label.configure(image=img, text='')
        label.image = img
    else:
        label.configure(text='Не удалось загрузить котика 😿', image='')


def open_new_window():
    """Открывает новое окно с котиком по тегу."""
    tag = tag_entry.get().strip()
    url_with_tag = (f'https://cataas.com/cat/{tag}' if tag
                    else 'https://cataas.com/cat')

    img = load_image(url_with_tag)
    if img:
        new_window = Toplevel(root)
        new_window.title('Картинка с котиком')
        new_window.geometry('620x520')

        new_label = Label(new_window, image=img)
        new_label.image = img
        new_label.pack()
    else:
        messagebox.showerror("Ошибка", "Не удалось загрузить котика по этому тегу 😿")


def on_exit():
    """Корректный выход из приложения."""
    root.destroy()


# --- Главное окно ---
root = Tk()
root.title('Cats')
root.geometry('620x520')

label = Label(root)
label.pack()

# --- Меню ---
menu_bar = Menu(root)
root.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Файл', menu=file_menu)
file_menu.add_command(label='Загрузить фото', command=open_new_window)
file_menu.add_separator()
file_menu.add_command(label='Выход', command=on_exit)

# --- Поле ввода тега ---
Label(root, text="Введите тег (например, 'cute'):").pack(pady=(10, 0))
tag_entry = Entry(root)
tag_entry.pack()

# --- Кнопки ---
load_button = Button(text='Загрузка по тегу', command=open_new_window)
load_button.pack(pady=5)

update_btn = Button(text='Следующая', command=set_image)
update_btn.pack(pady=5)

# --- Первый запуск ---
set_image()

root.mainloop()