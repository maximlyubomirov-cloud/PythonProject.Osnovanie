# for i in open('text.txt', 'r', encoding='utf-8'):
#     print(i.rstrip())

with open('text.txt', 'r', encoding='utf-8') as file:
    ls = file.read().title().split()

ls.sort()
print(ls)

with open('text1.txt', 'w', encoding='utf-8') as file:
    for n, word in enumerate(ls, 1):
        file.write(f'{n}. {word}\n')