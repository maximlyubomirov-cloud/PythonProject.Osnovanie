import time

# 1. Декоратор для замера времени выполнения
def time_run(func):
    def wrapper(*args, **kwargs):
        start = time.time()                 # Засекаем время ДО
        result = func(*args, **kwargs)      # Вызываем функцию и сохраняем результат
        end = time.time()                   # Засекаем время ПОСЛЕ
        duration = round(end - start, 2)    # Считаем разницу и округляем
        print(f'Функция {func.__name__} выполнялась {duration} сек.')
        return result                       # Возвращаем результат работы функции
    return wrapper                          # Возвращаем обертку


# 2. Декоратор для демонстрации (BEFORE / AFTER)
def decor(func):
    def wrapper():
        print('BEFORE')
        func()
        print('AFTER')
    return wrapper


# 3. Обычная функция без декоратора
def proba():
    print('PROBA')


# 4. Функция с декоратором времени
@time_run
def etalon(n):
    print('ETALON')
    time.sleep(n)                           # Имитация долгой работы


# --- Запуск ---
proba()                                     # Вызов обычной функции
print('---')
etalon(3)                                   # Вызов функции с декоратором