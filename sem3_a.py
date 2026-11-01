import sys

input_data = sys.stdin.read().split()

if len(input_data) != 2:
    print(0)
else:
    try:
        mood = int(input_data[0])
        change = int(input_data[1])
        if -1000 <= mood <= 1000 and -1000 <= change <= 1000:
            print(min(1000, max(-1000, mood + change)))
        else:
            print(0)
    except ValueError:
        print(0)