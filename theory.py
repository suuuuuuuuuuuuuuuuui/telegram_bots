'5507867442:AAE_hv9ZSvgK7Xas1LGOKDz5F60oMEcZe78'

"теория"

num_int = 5
num_float = 5.5
name = "Gleb"
first_name = "Gleb"
last_name = "ivanovski"
# print(num_int % num_float)
# print(first_name + last_name)


# if num_int > 4:
#     print(f"число {num_int} > 4 ")
# elif(num_int ) < 10:
#     print(f"число {num_int }<10")
#
# elif (num_int) < 10:
#     print(f"число {num_int}<10")
#
# elif (num_int) < 10:
#     print(f"число {num_int }<10")
#
# else:
#     print("оба условия не верны")
#
# for letter in first_name:
#     print(letter)

num_list = [1, 2, 3, 4, 5]


# for i in num_list:
#     print(i+1)
#
#
# while num_int > 1:
#     num_int += 1
#     if num_int == 8:
#         continue
#     print(num_int)


dict_ = {'0': 'Artem', 1: 'Vasya', 2: 'Vasya'}

print(dict_)
print(dict_['0'])
print(dict_[1])

dict_[2] = 'John'
print(dict_)

dict_1 = {}
print(dict_1)

dict_2 = dict()
print(dict_2)



for key, value in dict_.items():
    print(f'ключ: {key}, Значение: {value}')

for key in dict_.keys():
    print(f'ключ: {key}')

for value in dict_.values():
    print(f'Значение: {value}')

     
