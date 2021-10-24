import twine1

table = [[0 for i in range(16)] for j in range(16)]

max_size = 2 ** 4
for x1 in range(max_size):
    y1 = twine1.sbox[x1]
    for dx in range(max_size):
        x2 = x1 ^ dx
        y2 = twine1.sbox[x2]
        dy = y2 ^ y1

        table[dx][dy] = table[dx][dy] + 1

for i in table:
    print(i)

# for i in range(16):
#     for j in range(16):
#         if table[i][j] == 4:
#             print(f"dx = {i} and dy = {j}")
