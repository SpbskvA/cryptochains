from cmath import sqrt

m1 = 1.21
m2 = 1.23
m3 = 1.2
m4 = 1.21
mav = 1.2125
s = sqrt(((m1 - mav) ** 2 + (m2 - mav) ** 2 + (m3 - mav) ** 2 + (m4 - mav) ** 2) / 3)
print(3*s)
