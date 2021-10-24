from pathlib import Path
import twine1

next_hex = {
    '0': '1', '1': '2', '2': '3', '3': '4', '4': '5', '5': '6', '6': '7', '7': '8', '8': '9', '9': 'A', 'A': 'B',
    'B': 'C', 'C': 'D', 'D': 'E', 'E': 'F', 'F': '0'
}
skip_pos = [2, 4, 5, 6, 7, 8, 9, 14]
test_pos = [0, 1, 3, 10, 11, 12, 13, 15]
# i = 0x001011111100001f
# i = i + 0x1
# print(hex(i))
root_dir = Path('D:\\twine3\\plain_texts')
total_files = 687


def xor_two_num(num1, num2):
    x_or_result = int(num1, 16) ^ int(num2, 16)
    x_or_result = str(hex(x_or_result))[2:]
    return x_or_result


def first_line_from_file(file_num):
    filename = root_dir.joinpath(str(file_num) + '_plain.txt')
    with open(filename, 'r') as fp:
        for line in fp:
            # print(line)
            return line


def read_file(file_num):
    filename = root_dir.joinpath(str(file_num) + '_plain.txt')
    with open(filename, 'r') as fp:
        lines = fp.read().splitlines()
        # print(lines[0])
        # print(fp[0])
        return lines


# num = '731C111111FD4014'


def next_hex_line(line):
    f_num = ''
    for n in range(len(line)):
        if n in skip_pos:
            f_num = f_num + line[n]
        else:
            f_num = f_num + next_hex[line[n]]
    return f_num


def search_next_possible_file(current_file_num, hex_num):
    for next_file_num in range(current_file_num + 1, total_files):
        possible_line = first_line_from_file(next_file_num)
        if int(possible_line, 16) - int(hex_num, 16) > 0:
            return next_file_num - 1
        elif int(possible_line, 16) - int(hex_num, 16) == 0:
            return next_file_num
    return -1


def search_delta_x_in_files(file_num_to_read_from, value_to_test):
    possible_delta_x_lines = read_file(file_num_to_read_from)
    for possible_delta_x_line in possible_delta_x_lines:
        x_or_result = int(possible_delta_x_line, 16) ^ int(value_to_test, 16)
        x_or_result = str(hex(x_or_result))[2:]
        suppose_valid_delta_x = True
        for pos_to_check in test_pos:
            if x_or_result[pos_to_check] == '0':
                suppose_valid_delta_x = False
                break
        if suppose_valid_delta_x:
            encrypted_text1 = twine1.test_my_hex(possible_delta_x_line)
            encrypted_text2 = twine1.test_my_hex(value_to_test)
            xor_result = xor_two_num(encrypted_text1, encrypted_text2)
            flag = True
            for bit_pos in range(len(xor_result)):
                if bit_pos == 1 and xor_result[bit_pos] == '0':
                    flag = False
                    break
                elif bit_pos != 1 and xor_result[bit_pos] != '0':
                    flag = False
                    break
            if flag:
                print(value_to_test, possible_delta_x_line, encrypted_text1, encrypted_text2)


for i in range(5, total_files):
    lines = read_file(i)
    for current_hex_value in lines:
        hex_num = next_hex_line(current_hex_value)
        next_file_num = search_next_possible_file(i, hex_num)
        if next_file_num == -1:
            continue
        print('Expected:;' + str(next_file_num))
        for file_to_search in range(next_file_num, total_files):
            print("now processing : " + str(file_to_search))
            search_delta_x_in_files(file_to_search, current_hex_value)

        # exit(0)

# with open()
# if int(f_num, 16) - int(num, 16) > 0:
#     print("OOOOo")
