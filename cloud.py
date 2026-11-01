from tkinter import *
from tkinter import ttk, filedialog as fd, messagebox
import requests
import json
import os

# Define the history file path once, at module level
HISTORY_FILE = 'history.json'


def load_history():
    """Load history from disk, returning an empty list if the file is missing/corrupt."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_history(file_path, download_link):
    """Append a new entry to the history file."""
    history = load_history()
    history.append({
        'file_path': os.path.basename(file_path),
        'download_link': download_link
    })
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4, ensure_ascii=False)


def show_history():
    """Open a window displaying the download history."""
    history = load_history()

    history_window = Toplevel(root)
    history_window.title('История загрузок')

    files_listbox = Listbox(history_window, width=50, height=20)
    files_listbox.grid(row=0, column=0, padx=(10, 0), pady=10)

    links_listbox = Listbox(history_window, width=50, height=20)
    links_listbox.grid(row=0, column=1, padx=(0, 10), pady=10)

    for entry in history:
        files_listbox.insert(END, entry.get('file_path', ''))
        links_listbox.insert(END, entry.get('download_link', ''))


def upload():
    filepath = fd.askopenfilename()
    if not filepath:
        return

    url = 'https://store1.gofile.io/contents/uploadfile'

    try:
        with open(filepath, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files)

        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'ok':
                download_link = result['data']['downloadPage']
                save_history(filepath, download_link)  # <-- actually save it
                messagebox.showinfo(
                    "Success",
                    f"File uploaded successfully!\nLink: {download_link}"
                )
            else:
                messagebox.showerror(
                    "Upload Failed",
                    f"Server responded with: {result.get('status')}"
                )
        else:
            messagebox.showerror(
                "Upload Failed",
                f"HTTP Error: {response.status_code}\n{response.text}"
            )

    except ValueError as err:
        messagebox.showerror("Error", f"Invalid response: {err}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")


root = Tk()
root.title('Облачное хранилище файлов')
root.geometry('400x200')

upload_button = ttk.Button(text='загрузить файл', command=upload)
upload_button.pack(pady=20)

history_button = ttk.Button(text='История загрузок', command=show_history)
history_button.pack(pady=5)

entry = ttk.Entry()
entry.pack(pady=10)

root.mainloop()