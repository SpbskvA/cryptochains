from math import factorial
n = factorial(85)
cnt = 0
while n % 2 == 0:
    n = n // 2
    cnt += 1
print(cnt)