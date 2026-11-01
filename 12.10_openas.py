from pathlib import Path

Path('данные/вход').mkdir(parents=True, exist_ok=True)
Path('данные/выход').mkdir(parents=True, exist_ok=True)

with open(Path('данные/вход') / 'text.txt', 'w', encoding='utf-8') as file:
    file.write('banana apple cherry dog cat elephant\n')

with open(Path('данные/вход') / 'text.txt', 'r', encoding='utf-8') as file:
    ls = file.read().title().split()

ls.sort()

with open(Path('данные/выход') / 'text1.txt', 'w', encoding='utf-8') as file:
    for n, word in enumerate(ls, 1):
        file.write(f'{n}. {word}\n')

with open(Path('данные/выход') / 'text1.txt', 'r', encoding='utf-8') as file:
    print(file.read())