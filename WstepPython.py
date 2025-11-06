# -*- coding: utf-8 -*-

a = 2

b = 3.

print(type(b))

c = 'Zaawansowane metody geoinformatyczne'

d = [1, -45, 78, -234, 7980, -985, 436545, 76876, 4352, -7890, -45643]



# print(c[6])
karton = 0
dodatnie = 0
ujemne = 0
for i in d:
    if i > 0:
        dodatnie += i
    elif i < 0:
        ujemne += i
    print(i)
    karton += i
# print("Suma: ", karton)

print("Suma ujemnych wartości: ", ujemne, "Suma dodatnich wartości: ", dodatnie)

# print(a > b)


