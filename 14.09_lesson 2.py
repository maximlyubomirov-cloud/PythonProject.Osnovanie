# # # # # """
# # # # # """
# # #
# # #
# # # #
# # # # # Конкатенация строк
# # # # s1 = "Hello"
# # # # s2 = "World"
# # # # result = s1 + s2          # "HelloWorld"
# # # # print(result)
# # # #
# # # # # Конкатенация списков
# # # # list1 = [1, 2, 3]
# # # # list2 = [4, 5, 6]
# # # # result_list = list1 + list2   # [1, 2, 3, 4, 5, 6]
# # # # print(result_list)
# # # # print(num[1:-2])
# # # # print(num[::2])
# # # # print(num[::-1])
# # # # # num[1, 2, [32, 4]] = 3333
# # # # nn = num
# # # # nn = num[:]
# # # # n#
# # # # num[1, 2, [32, 4]]
# # #
# # # # print(num, id(num))
# # # # print(nn, id(nn))
# # # # print
# # # # # print(nn), print(id())
# # # # x = 100
# # # # y = 100
# # # # print ( id(x) ,id(y))
# # # # num = [22, 33, 44, 55, 66, 77, 88, 99]
# # # # print(sum(num))          # 484
# # # # print(sum(num)/len(num)) # 60.5
# # # # even = [x for x in num if x % 2 == 0]  # [22, 44, 66, 88]
# # # # odd  = [x for x in num if x % 2 != 0]  # [33, 55, 77, 99]
# # # # num = [22, 100, 44, 100, 99]
# # # # print (num[1:-2])
# # # #
# # # #
# # # # print(num)
# # # # num.append(100) #добавить в конец списка 0(1) константная
# # # # print(num)
# # # # # num.insert(index: 0, object: 300) # 0(n) линейная
# # # # print (num)
# # # # num.extend([1,2])
# # # # print (num)
# # # #
# # # # num += [1, 2]
# # # # n= num.pop()
# # # # nn = num.pop(0)
# # # # print (n)
# # # # print (num)
# # # # # while 100 in num:
# # # # #     num.remove(100)
# # # # #     print (num)
# # # # print(num.index(100))
# # # # print(num.count(100))
# # # # # num.clear()
# # # # # print(num)
# # # # num = [22, 33, 44, 55, 99]
# # # # for i in range (len(num)):
# # # #    print(i, num[i], end='  ')
# # # #
# # # # for r, i in enumerate (num):
# # # #     print(i, end=' ')
# # # print ()
# # #     names = ['Dasha', 'Masha', 'Sasha', 'Glasha', 'Andryusha']
# # #     names.reverse()
# # # print(names)
# # # names.sort()
# # # for k,i in enumerate(names, num):
# # #     print(f'{k}: {i}'
# # #           for in zip(names, num):
# # #     print(i)
# # #
# # #
# # #
# # """кортеж (Tuple) """
# # tp = (22, 33, 44, 99)
# # k,i, *z = 7, 5, 9, 10, 1, 32, 56, 100
# # print(k, i, z)
# # print(tp, type(tp))
# # tp = ('login', 'password')
# # print(tp, id(tp))
# # buf = list(tp)
# # buf[-1] = 'new_password'
# # tp = tuple(buf)
# # print(tp, id(tp))
# # """левый циклический сдвиг"""
# # l = [22, 33, 44, 55, 99]
# # temp = l[0]
# # n = len(l)
# # for i in range(n-1):
# #     l[i] = l[i + 1]
# # l[-1] = temp
# # print(l)
# # temp = l.pop(0)
# # l.append(temp)
# # print(l)
# #
# #
# # x = 10
# # y = 15
# # z = x
# # x = y
# # y = z
# # print (x, y)
# # x, y = y, x
# # print (x, y)
# #
# #
# #
# # #    arr[i] = i + 1
# # #    print(arr)
# # #    ls = []
# # #    for i in range(10):
# # #        ls.append(i + 1)
# # '''левый циклический сдвиг'''
# # l = [22, 33, 44, 55, 99]
# # temp = l[0]
# # n = len(l)
# # for i in range(10):
# #     if i > 1:
# #         if i+1 // 2 == 0:
# #             print(i+1)
# #             ls.append(i + 1)
# #         else:
# #             ls.append(i)
# #             else:
# #             ls.append(i + 1)
# # print(5 if len(ls))
#
# ls = []
# for i in range(5):
#     if i % 2 == 0:
#         pass  # Какое-то действие для четных чисел
#     else:
#         ls.append(i)
#
# print(ls)
#
# print(5 if len(ls) < 7 else 125)
#
# ls = [i + 1 if (i + 1) % 2 == 0 else i for i in range(10) if i > 1]
# print(ls)
#
# """ кортеж (Tuple) """
# # y = z
# # print(x, y)
# # x, y = y, x
# # print(x, y)

names = ['Dasha', 'Masha', 'Sasha', 'Glasha', 'Andryusha']
age = [22, 33, 44, 55, 11]
persons =[('Dasha', 22), ('Masha', 33)]
for r, (n, a) in enumerate(zip(names, age)/ 1):
    print(f'{r}.- {n} - {a}')