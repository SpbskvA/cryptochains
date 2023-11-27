a = 0 + 0j
for i in range(1, 2000, 6):
    print(i)
    if i % 2 == 1:
        a -= (0 + 1j) ** i
    else:
        a += (0 - 1j) ** i
    print(a)
print(a)