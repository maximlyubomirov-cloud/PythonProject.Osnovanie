def solve():
    # Считываем входные данные
    try:
        # input().split() разбивает строку по пробелам
        # map(int, ...) преобразует их в числа
        W, H, w, h = map(int, input().split())
    except ValueError:
        return

    # Проверяем, проходит ли декорация без поворота
    if w <= W and h <= H:
        print("YES")
    # Проверяем, проходит ли декорация с поворотом (меняем w и h местами)
    elif h <= W and w <= H:
        print("TURN")
    # Если ни один вариант не подошел
    else:
        print("NO")

if __name__ == "__main__":
    solve()