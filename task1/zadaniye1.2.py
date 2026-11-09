password = input("Введите пароль: ")
while len(password) < 8:
    print("Пароль слишком короткий! Минимальная длина — 8 символов.")
    password = input("Введите пароль ещё раз: ")
print("Пароль принят!")