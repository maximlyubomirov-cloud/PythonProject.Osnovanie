h =int(input())
m =int(input())
cost =20
if m <= 5:
    cost = m * 20
elif m <= 20:
    cost = 5 * 20 + (m - 5) * 12
else:
    cost = 5 * 20 + 15 * 12 + (m - 20) * 8
if h >= 22 or h <=  5:
    discount = cost // 4
    cost -= discount

print(cost)
