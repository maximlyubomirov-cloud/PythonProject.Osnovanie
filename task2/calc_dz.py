def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Ошибка: Деление на ноль"
    return x / y

def log(result):
    with open("calculations.txt", "a") as file:
        file.write(result + "\n")  # добавлен перевод строки для читаемости

print("Выберите операцию: ")
print("1. Сложение")
print("2. Вычитание")
print("3. Умножение")
print("4. Деление")

choice = input("Введите номер операции (1/2/3/4): ")

num1 = int(input("Введите первое число: "))
num2 = int(input("Введите второе число: "))

if choice == '1':
    r = f"Результат: {num1} + {num2} = {add(num1, num2)}"
    print(r)
    log(r)
elif choice == '2':
    r = f"Результат: {num1} - {num2} = {subtract(num1, num2)}"
    print(r)
    log(r)
elif choice == '3':
    r = f"Результат: {num1} * {num2} = {multiply(num1, num2)}"
    print(r)
    log(r)
elif choice == '4':
    r = f"Результат: {num1} / {num2} = {divide(num1, num2)}"
    print(r)
    log(r)
else:
    print("Неверный ввод")