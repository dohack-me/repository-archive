# THE INTENDED SOLUTION

import math

n = 3
x1 = 2
y1 = 1

def verify(x):
    three_y_squared = x ** 2 - 1
    if three_y_squared % 3 != 0:
        return False
    
    y_squared = three_y_squared // 3
    if math.floor(math.sqrt(y_squared)) == math.sqrt(y_squared):
        return True
    
    return False

def get_next_sol(x, y):
    new_x = x1*x + n*y1*y
    new_y = x1*y + y1*x
    return (new_x, new_y)

x, y = x1, y1
store = [0]*1000
for _ in range(1000):
    store[math.floor(math.log(x, 10))] = x
    x, y = get_next_sol(x, y)

raw_key = str(input("Give me your key, I will give you the correct input for the challenge:\n")).strip().split(' ')
key = [int(i) for i in raw_key]

ans = []
for i in key:
    ans.append(store[i])
    print(store[i], end=' ')
    
