import binascii

number_of_rounds = 4

sbox = {0x0: 0xC,
        0x1: 0x0,
        0x2: 0xF,
        0x3: 0xA,
        0x4: 0x2,
        0x5: 0xB,
        0x6: 0x9,
        0x7: 0x5,
        0x8: 0x8,
        0x9: 0x3,
        0xA: 0xD,
        0xB: 0x7,
        0xC: 0x1,
        0xD: 0xE,
        0xE: 0x6,
        0xF: 0x4}

permutation_enc = {0x0: 0x5,
                   0x1: 0x0,
                   0x2: 0x1,
                   0x3: 0x4,
                   0x4: 0x7,
                   0x5: 0xC,
                   0x6: 0x3,
                   0x7: 0x8,
                   0x8: 0xD,
                   0x9: 0x6,
                   0xA: 0x9,
                   0xB: 0x2,
                   0xC: 0xF,
                   0xD: 0xA,
                   0xE: 0xB,
                   0xF: 0xE}

permutation_dec = {0x0: 0x1,
                   0x1: 0x2,
                   0x2: 0xB,
                   0x3: 0x6,
                   0x4: 0x3,
                   0x5: 0x0,
                   0x6: 0x9,
                   0x7: 0x4,
                   0x8: 0x7,
                   0x9: 0xA,
                   0xA: 0xD,
                   0xB: 0xE,
                   0xC: 0x5,
                   0xD: 0x8,
                   0xE: 0xF,
                   0xF: 0xC}

con = {0x01: 0x01,
       0x02: 0x02,
       0x03: 0x04,
       0x04: 0x08,
       0x05: 0x10,
       0x06: 0x20,
       0x07: 0x03,
       0x08: 0x06,
       0x09: 0x0C,
       0x0A: 0x18,
       0x0B: 0x30,
       0x0C: 0x23,
       0x0D: 0x05,
       0x0E: 0x0A,
       0x0F: 0x14,
       0x10: 0x28,
       0x11: 0x13,
       0x12: 0x26,
       0x13: 0x0F,
       0x14: 0x1E,
       0x15: 0x3C,
       0x16: 0x3B,
       0x17: 0x35,
       0x18: 0x29,
       0x19: 0x11,
       0x1A: 0x22,
       0x1B: 0x07,
       0x1C: 0x0E,
       0x1D: 0x1C,
       0x1E: 0x38,
       0x1F: 0x33,
       0x20: 0x25,
       0x21: 0x09,
       0x22: 0x12,
       0x23: 0x24}


def CON_L(r):
    return con[r] & 0b111


def CON_H(r):
    return con[r] >> 3 & 0b111


def key_schedule(key):
    key = key.encode("utf-8").hex()

    w_key = {}
    for i in range(len(key)):
        w_key[i] = int(key[i], 16)
    # print(w_key.values())
    round_table = [[0 for i in range(8)] for j in range(36)]

    for r in range(35):
        round_table[r][0] = w_key[1]
        round_table[r][1] = w_key[3]
        round_table[r][2] = w_key[4]
        round_table[r][3] = w_key[6]
        round_table[r][4] = w_key[13]
        round_table[r][5] = w_key[14]
        round_table[r][6] = w_key[15]
        round_table[r][7] = w_key[16]

        w_key[1] = w_key[1] ^ sbox[w_key[0]]
        w_key[4] = w_key[4] ^ sbox[w_key[16]]
        w_key[7] = w_key[7] ^ CON_H(r + 1)
        w_key[19] = w_key[19] ^ CON_L(r + 1)

        temp1 = w_key[0]
        temp2 = w_key[1]
        temp3 = w_key[2]
        temp4 = w_key[3]
        for j in range(4):
            w_key[j * 4] = w_key[j * 4 + 4]
            w_key[j * 4 + 1] = w_key[j * 4 + 5]
            w_key[j * 4 + 2] = w_key[j * 4 + 6]
            w_key[j * 4 + 3] = w_key[j * 4 + 7]

        w_key[16] = temp2
        w_key[17] = temp3
        w_key[18] = temp4
        w_key[19] = temp1

    round_table[35][0] = w_key[1]
    round_table[35][1] = w_key[3]
    round_table[35][2] = w_key[4]
    round_table[35][3] = w_key[6]
    round_table[35][4] = w_key[13]
    round_table[35][5] = w_key[14]
    round_table[35][6] = w_key[15]
    round_table[35][7] = w_key[16]

    return round_table


def encryption(plain_text, round_key):
    X = {}
    Y = {}
    for i in range(len(plain_text)):
        X[i] = int(plain_text[i], 16)

    for i in range(number_of_rounds - 1):
        for j in range(8):
            X[2 * j + 1] = sbox[X[2 * j] ^ round_key[i][j]] ^ X[2 * j + 1]

        for h in range(16):
            Y[permutation_enc[h]] = X[h]
        X = Y.copy()

    for j in range(8):
        X[2 * j + 1] = sbox[X[2 * j] ^ round_key[number_of_rounds - 1][j]] ^ X[2 * j + 1]

    Cip = ""
    for i in range(16):
        Cip = Cip + hex(X[i])[2:]
    return Cip


def decryption(cipher, round_key):
    X = {}
    Y = {}
    for i in range(len(cipher)):
        X[i] = int(cipher[i], 16)

    for i in range(number_of_rounds - 1, 0, -1):
        for j in range(8):
            X[2 * j + 1] = sbox[X[2 * j] ^ round_key[i][j]] ^ X[2 * j + 1]
        for h in range(16):
            Y[permutation_dec[h]] = X[h]

        X = Y.copy()

    for j in range(8):
        X[2 * j + 1] = sbox[X[2 * j] ^ round_key[0][j]] ^ X[2 * j + 1]

    plain = ""
    for i in range(16):
        plain = plain + hex(X[i])[2:]
    return binascii.unhexlify(plain).decode("utf-8")


key1 = "qwertyuiop"
while len(key1) != 10:
    print("size error")
    key1 = input("enter 80bit key")
round_key = key_schedule(key1)


def create_block_enc(plain_text):
    pointer = 0
    i = 0
    cipher_text = ""
    while pointer < len(plain_text):
        if len(plain_text[pointer:]) > 16:
            cipher_text = cipher_text + encryption(plain_text[pointer:pointer + 17], round_key)
            pointer = pointer + 16
        else:
            if len(plain_text) == 16:
                cipher_text = cipher_text + encryption(plain_text[pointer:], round_key)
                pointer = pointer + 16
            else:
                temp = plain_text[pointer:]
                for i in range(16 - len(temp)):
                    temp = '0' + temp
                cipher_text = cipher_text + encryption(temp, round_key)
                pointer = pointer + 16
        # print(f"done {i}")
        i = i + 1
    # print(cipher_text)
    return cipher_text


def dec_by_blocks(cipher_text):
    pointer = 0

    plain_text = ""
    while pointer < len(cipher_text):
        if len(cipher_text[pointer:]) > 16:
            plain_text = plain_text + decryption(cipher_text[pointer:pointer + 17], round_key)
            pointer = pointer + 16
        else:
            plain_text = plain_text + decryption(cipher_text[pointer:], round_key)
            pointer = pointer + 16

    print(plain_text)


plain_text1 = "Biswa002"
plain_text1 = plain_text1.encode("utf-8").hex()
cipher_txt = create_block_enc(plain_text1)
print(cipher_txt)
dec_by_blocks(cipher_txt)

def test_my_hex(test_num):
    cipher_txt = create_block_enc(test_num)
    return cipher_txt

