import turtle
#
# # Создаём экран и переключаем режим на 255
# screen = turtle.Screen()
# screen.colormode(255)  # Обязательно нужно вызвать перед использованием RGB-кортежей
#
# # Теперь можно задавать цвета как кортежи
# turtle.pencolor(255, 0, 0)  # Красный
# turtle.pencolor(0, 255, 0)  # Зелёный
# turtle.pencolor(0, 0, 255)  # Синий
#
# turtle.forward(100)
#
#
# import turtle as t
# t. colormode(255)
#
# t.ht()
#
# t.pensize(5)
#
# for r in range(40, 0, -10):
#
#     for i in range(6):
#         t.color(255, 165, r * 6)
#
#         t.fillcolor(162, r * 6, 255)
#
#         t.begin_fill()
#
#         t.tiltangle(r)
#
#         t.end_fill()
#
#         t.rt(60)
from turtle import *
forward(100)
left(120)
forward(100)
home()
pos()
for steps in range(15):
    for c in ('blue', 'red', 'green'):
        color(c)
        forward(steps)
        right(30)
        color('red')
begin_fill()
start = pos()

while True:
    forward(200)
    left(170)
    if distance(start) < 1:
        break
