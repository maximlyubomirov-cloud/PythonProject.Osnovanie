
from string import ascii_letters, digits
import re
import random

def get_password(m):
    data = ''.join(set(ascii_letters + digits) - {'0', '1', 'o', 'O', 'l', 'I'})
    data1 = ''.join(re.findall(r'[^01oOlI]', ascii_letters + digits))
    return data, data1
    password = random.sample(data1, m)
    pos = random.sample(range(m), k: 3)
    password[pos[0]].lower()
    password[pos[1]].lower()
    return password




# Пример вызова функции
result = get_password("Введите подсказку: ")
print(result)