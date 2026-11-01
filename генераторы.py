# l = [22, 33, 44]
#
# def gen()
#     i=0
#     while i < 3:
#         i += 1
#         yield i


    #    print(res)
    # print('1',next(res))
    # print('2',next(res))
    # print('3',next(res))
    #
    #
    #     res = gen()
    #
    #     for i in res:
    #         print(i)
    #
    #         for i in res:
    #             print(i)
res = (i for i in gen())
print(list(res))
res = [i for i in gen())
for i in res:
print(res)
