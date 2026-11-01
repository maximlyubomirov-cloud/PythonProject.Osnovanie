import time

def time_run(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)  # 1. Сохраняем результат
        end = time.time()
        duration = round(end - start, 2)
        # 2. Выводим имя функции и время её работы
        print(f'Функция {func.__name__} выполнялась {duration} сек.')
        return result                   # 3. Возвращаем результат
    return wrapper                      # 4. Возвращаем обертку!

# --- Проверка ---
@time_run
def add(a, b):
    time.sleep(0.5)  # Имитация работы
    return a + b

# Вызов
sum_result = add(2, 3)
print(f'Результат: {sum_result}')