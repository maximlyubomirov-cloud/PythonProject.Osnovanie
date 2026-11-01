import json

with open('dict.json', 'r', encoding='utf-8') as file:
    d = json.load(file)

while True:
    word = input('Введите слово для перевода (или "exit" для выхода): ').strip().lower()

    if word == 'exit':
        print('До свидания!')
        break
    elif not word:
        print('Вы ничего не ввели, попробуйте снова.')
        continue
    elif word in d:
        print(f'{word} - {d[word]}')
    else:
        translate = input(f'Слово "{word}" не найдено. Введите перевод: ')
        d[word] = translate

        with open('dict.json', 'w', encoding='utf-8') as file:
            json.dump(d, file, indent=4, ensure_ascii=False)

        print(f'Слово "{word}" добавлено в словарь!')