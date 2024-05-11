
def encrypt_rail_fence(text: str, key: int) -> str:
    rail = [['\n' for _ in range(len(text))]
            for _ in range(key)]

    # to find the direction
    dir_down = False
    row, col = 0, 0

    for i in range(len(text)):
        if (row == 0) or (row == key - 1):
            dir_down = not dir_down

        # fill the corresponding alphabet
        rail[row][col] = text[i]
        col += 1

        # find the next row using
        # direction flag
        if dir_down:
            row += 1
        else:
            row -= 1
    # now we can construct the cipher
    # using the rail matrix

    result = []
    for i in range(key):
        for j in range(len(text)):
            if rail[i][j] != '\n':
                result.append(rail[i][j])
    return "".join(result)


def gen_text_with_len(length: int) -> str:
    characters = string.ascii_letters + string.digits + string.punctuation
    generated_text = ''.join(random.choices(characters, k=length))
    return generated_text


def find_enc_rel(key: int) -> list[int]:
    rel: list[int] = []

    for i in range(1, 101):
        original = gen_text_with_len(i)
        enc = original

        count: int = 0
        while True:
            count += 1
            enc = encrypt_rail_fence(enc, key)
            # print("{}\t: \t\t{}".format(count, enc))
            if enc == original:
                # rel.append((i, count))
                rel.append(count)
                # print(i)
                break

    return rel


def rail_fence_list(numbers: list[int], rails: int) -> list[int]:
    fence = [[] for _ in range(rails)]

    direction = 1
    row = 0

    for num in numbers:
        fence[row].append(num)
        row += direction
        if row == rails - 1 or row == 0:
            direction *= -1

    encrypted_list = [num for row in fence for num in row]

    return encrypted_list


def num_tracking(list_len: int, key: int, num_search: int) -> list[int]:
    nums: list[int] = [i for i in range(list_len)]
    search_list: list[int] = [num_search]

    while True:
        nums = rail_fence_list(nums, key)
        index = nums.index(num_search)
        if index == num_search:
            break
        search_list.append(index)

    return search_list


def lcm_for_n(n):
    return math_two.lcm(*[i for i in range(2, n + 1)])


def main():
    lcm_list = [lcm_for_n(i) for i in range(1, 100)]
    lcm_ratio_list = []

    for i in range(len(lcm_list) - 1):
        lcm_ratio = int(lcm_list[i + 1] / lcm_list[i])
        lcm_ratio_list.append(lcm_ratio)

    print(lcm_ratio_list)
    plt.plot(lcm_ratio_list)
    plt.show()

    sum_list = 0
    for i in lcm_list:
        sum_list += 1 / i
    print(sum_list)

    plt.plot(lcm_list)
    print(lcm_list)
    plt.show()

    n = 25
    track_nums = [i for i in range(n)]

    for i in track_nums:
        track = num_tracking(list_len=n, key=4, num_search=i)
        plt.plot(track)
        print(track)
        print(len(track))
        print()

    plt.show()


if __name__ == '__main__':
    import random
    import string
    from maths import math_two
    import matplotlib.pyplot as plt

    main()



'''
0 * * * 4 * * * 8 * * * 12
* 1 * 3 * 5 * 7 * 9 * 11 *
* * 2 * * * 6 * * * 10 * *
'''

relations = [
    [1, 1, 2, 2, 4, 4, 3, 3, 6, 6, 10, 10, 12, 12, 4, 4, 8, 8, 18, 18, 6, 6, 11, 11, 20, 20, 18, 18, 28, 28, 5, 5,
     10, 10, 12, 12, 36, 36, 12, 12, 20, 20, 14, 14, 12, 12, 23, 23, 21, 21, 8, 8, 52, 52, 20, 20, 18, 18, 58, 58,
     60, 60, 6, 6, 12, 12, 66, 66, 22, 22, 35, 35, 9, 9, 20, 20, 30, 30, 39, 39, 54, 54, 82, 82, 8, 8, 28, 28, 11,
     11, 12, 12, 10, 10, 36, 36, 48, 48, 30, 30],
    [1, 1, 1, 2, 3, 4, 4, 6, 12, 6, 6, 21, 18, 4, 4, 12, 15, 12, 12, 132, 19, 24, 24, 22, 42, 8, 8, 153, 24, 24, 24,
     408, 84, 60, 60, 690, 207, 420, 420, 420, 140, 60, 60, 620, 406, 105, 105, 120, 1209, 546, 546, 516, 360, 36,
     36, 1290, 1320, 342, 342, 6270, 264, 84, 84, 132, 4797, 120, 120, 66, 7140, 504, 504, 390, 13464, 24, 24, 660,
     138, 504, 504, 180, 1482, 1092, 1092, 1860, 3720, 120, 120, 1020, 13650, 24, 24, 13398, 1650, 465, 465, 2065,
     2030, 28, 28, 47124],
    [1, 1, 1, 1, 2, 3, 6, 7, 8, 8, 10, 30, 28, 40, 14, 14, 63, 70, 20, 28, 14, 14, 168, 156, 99, 132, 12, 12, 84,
     18, 390, 120, 12, 12, 180, 132, 70, 300, 38, 38, 420, 240, 102, 78, 156, 156, 42, 2574, 372, 760, 44, 44, 50,
     858, 1050, 180, 252, 252, 846, 342, 936, 19040, 50, 50, 240, 28014, 495, 3198, 174, 174, 1980, 8580, 12121,
     9240, 462, 462, 1260, 2940, 3720, 79, 1560, 1560, 2856, 6068, 162, 75900, 780, 780, 216, 9240, 2244, 340, 780,
     780, 3960, 990, 4230, 2520, 396, 396],
    [1, 1, 1, 1, 1, 2, 3, 6, 4, 4, 9, 10, 10, 12, 12, 84, 16, 90, 6, 6, 6, 12, 84, 156, 120, 60, 136, 13, 13, 115,
     29, 280, 92, 208, 120, 30, 30, 570, 304, 380, 186, 216, 336, 38, 38, 558, 264, 1740, 510, 2736, 1260, 228, 228,
     660, 480, 1122, 840, 234, 364, 280, 280, 132, 72, 24752, 546, 741, 3655, 855, 855, 60, 192, 8580, 120, 30702,
     4350, 240, 240, 11284, 630, 336, 370, 990, 2360, 120, 120, 7480, 1428, 18648, 180, 2800, 332, 300, 300, 172,
     360, 22200, 240, 9350, 210, 380]
]

# for key 2 (len 100): [1, 1, 2, 2, 4, 4, 3, 3, 6, 6, 10, 10, 12, 12, 4, 4, 8, 8, 18, 18, 6, 6, 11, 11, 20, 20, 18, 18, 28, 28, 5, 5, 10, 10, 12, 12, 36, 36, 12, 12, 20, 20, 14, 14, 12, 12, 23, 23, 21, 21, 8, 8, 52, 52, 20, 20, 18, 18, 58, 58, 60, 60, 6, 6, 12, 12, 66, 66, 22, 22, 35, 35, 9, 9, 20, 20, 30, 30, 39, 39, 54, 54, 82, 82, 8, 8, 28, 28, 11, 11, 12, 12, 10, 10, 36, 36, 48, 48, 30, 30]

# for key 3 (len 100): [1, 1, 1, 2, 3, 4, 4, 6, 12, 6, 6, 21, 18, 4, 4, 12, 15, 12, 12, 132, 19, 24, 24, 22, 42, 8, 8, 153, 24, 24, 24, 408, 84, 60, 60, 690, 207, 420, 420, 420, 140, 60, 60, 620, 406, 105, 105, 120, 1209, 546, 546, 516, 360, 36, 36, 1290, 1320, 342, 342, 6270, 264, 84, 84, 132, 4797, 120, 120, 66, 7140, 504, 504, 390, 13464, 24, 24, 660, 138, 504, 504, 180, 1482, 1092, 1092, 1860, 3720, 120, 120, 1020, 13650, 24, 24, 13398, 1650, 465, 465, 2065, 2030, 28, 28, 47124]

# for key 4 (len 100): [1, 1, 1, 1, 2, 3, 6, 7, 8, 8, 10, 30, 28, 40, 14, 14, 63, 70, 20, 28, 14, 14, 168, 156, 99, 132, 12, 12, 84, 18, 390, 120, 12, 12, 180, 132, 70, 300, 38, 38, 420, 240, 102, 78, 156, 156, 42, 2574, 372, 760, 44, 44, 50, 858, 1050, 180, 252, 252, 846, 342, 936, 19040, 50, 50, 240, 28014, 495, 3198, 174, 174, 1980, 8580, 12121, 9240, 462, 462, 1260, 2940, 3720, 79, 1560, 1560, 2856, 6068, 162, 75900, 780, 780, 216, 9240, 2244, 340, 780, 780, 3960, 990, 4230, 2520, 396, 396]

# for key 5 (len 100): [1, 1, 1, 1, 1, 2, 3, 6, 4, 4, 9, 10, 10, 12, 12, 84, 16, 90, 6, 6, 6, 12, 84, 156, 120, 60, 136, 13, 13, 115, 29, 280, 92, 208, 120, 30, 30, 570, 304, 380, 186, 216, 336, 38, 38, 558, 264, 1740, 510, 2736, 1260, 228, 228, 660, 480, 1122, 840, 234, 364, 280, 280, 132, 72, 24752, 546, 741, 3655, 855, 855, 60, 192, 8580, 120, 30702, 4350, 240, 240, 11284, 630, 336, 370, 990, 2360, 120, 120, 7480, 1428, 18648, 180, 2800, 332, 300, 300, 172, 360, 22200, 240, 9350, 210, 380]
