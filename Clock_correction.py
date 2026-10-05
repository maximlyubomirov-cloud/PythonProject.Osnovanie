h = int(input())
m = int(input())
s = int(input())
d = int(input())

total_seconds = h * 3600 + m * 60 +s
new_total = total_seconds + d
days = new_total//86400
seconds_in_day = new_total%86400
new_h = seconds_in_day // 3600
new_m = (seconds_in_day % 3600) // 60
new_s = seconds_in_day % 60

print(days, new_h, new_m, new_s)
