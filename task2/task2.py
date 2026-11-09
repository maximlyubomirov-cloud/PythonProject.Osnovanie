111def add(x, y):
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
    """Записывает результат в файл истории."""
    with open("calculations.txt", "a", encoding="utf-8") as file:
        file.write(result + "\n")

def show_history():
    """Читает файл calculations.txt и выводит историю вычислений."""
    print("История вычислений:")ф
    try:
        with open("calculations.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            if not lines:
                print("История пуста.")
            else:
                for line in lines:
                    print(line, end="")
    except FileNotFoundError:
        print("История пуста (нет сохранённых вычислений).")

def perform_operation(choice, num1, num2):
    """Выполняет выбранную операцию и возвращает строку с результатом."""
    if choice == '1':
        return f"Результат: {num1} + {num2} = {add(num1, num2)}"
    elif choice == '2':
        return f"Результат: {num1} - {num2} = {subtract(num1, num2)}"
    elif choice == '3':
        return f"Результат: {num1} * {num2} = {multiply(num1, num2)}"
    elif choice == '4':
        result = divide(num1, num2)
        if isinstance(result, float):
            return f"Результат: {num1} / {num2} = {result:.2f}"
        else:
            return f"Результат: {num1} / {num2} = {result}"
    return None

def get_numbers():
    """Запрашивает у пользователя два числа с обработкой ошибок."""
    while True:
        try:
            num1 = float(input("Введите первое число: "))
            num2 = float(input("Введите второе число: "))
            # Если числа целые, преобразуем их в int для красивого вывода
            if num1.is_integer():
                num1 = int(num1)
            if num2.is_integer():
                num2 = int(num2)
            return num1, num2
        except ValueError:
            print("Ошибка: нужно вводить числа. Попробуйте снова.")

def main():
    # Переменные для хранения текущих чисел между итерациями
    num1, num2 = None, None

    while True:
        print("\nВыберите операцию: ")
        print("1. Сложение")
        print("2. Вычитание")
        print("3. Умножение")
        print("4. Деление")
        print("5. Просмотр истории вычислений")
        print("0. Выход")

        choice = input("Введите номер операции (1/2/3/4/5/0): ")

        # Выход из программы
        if choice == '0':
            print("До свидания!")
            break

        # Просмотр истории
        if choice == '5':
            show_history()
            continue

        # Проверка корректности выбора
        if choice not in ('1', '2', '3', '4'):
            print("Неверный ввод. Попробуйте снова.")
            continue

        # Если числа ещё не введены — запрашиваем их
        # Если пользователь ранее выбрал "повторить" — числа уже есть, и мы их не трогаем
        if num1 is None or num2 is None:
            num1, num2 = get_numbers()

        # Выполняем операцию
        r = perform_operation(choice, num1, num2)
        print(r)
        log(r)

        # Спрашиваем, хочет ли пользователь повторить с теми же числами
        repeat = input("Повторить вычисление с этими же числами? (да/нет): ").strip().lower()
        if repeat in ('да', 'д', 'y', 'yes'):
            # Оставляем num1 и num2 как есть — при следующей итерации
            # программа спросит только операцию
            print(f"Используем числа: {num1} и {num2}")
        else:
            # Сбрасываем числа, чтобы в следующий раз запросить новые
            num1, num2 = None, None

if __name__ == "__main__":
    main()
