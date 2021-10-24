# i = 2, 4, 5, 6, 7, 8, 9, 14

def join_tuple_string(strings_tuple) -> str:
    return ''.join(strings_tuple)


import itertools
from pprint import pprint

inputdata = [
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'],  # 0th
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'],  # 1st
    ['E'],
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'],  # 3
    ['8'],
    ['A'],
    ['1'],
    ['2'],
    ['1'],
    ['1'],
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'],  # 10
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'],  # 11
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'],  # 12
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'],  # 13
    ['5'],
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'],
]
print(type(itertools.product(*inputdata)))
count = 1
f_count = 1
l = []
for line in itertools.product(*inputdata):
    result = ''.join(list(map(join_tuple_string, line)))
    # print(result)
    # break
    l.append(result)
    count = count + 1
    if count == pow(2, 22):
        with open('D:\\twine3\\plain_texts\\' + str(f_count) + '_plain.txt', 'w') as fp:
            fp.write('\n'.join(l))
            print(str(f_count) + '_plain.txt')
        f_count = f_count + 1
        count = 0
        l = []

# result = list(itertools.product(*inputdata))

result = list(map(join_tuple_string, result))

print(len(result))
# for i in result:
#     print(i)
