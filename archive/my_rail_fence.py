
def encrypt_rail_fence(text: str, key: int) -> str:
    rail: list[str] = ["" for _ in range(key)]

    dir_down = False
    row = 0

    for i in range(len(text)):
        if row == 0 or row == key - 1:
            dir_down = not dir_down

        rail[row] += text[i]

        if dir_down:
            row += 1
        else:
            row -= 1

    return "".join(rail)


def decrypt_rail_fence(cipher: str, key: int) -> str:
    rail: list[list[str]] = [['\n' for _ in range(len(cipher))] for _ in range(key)]

    dir_down = False
    row, col = 0, 0

    for i in range(len(cipher)):
        if row == 0 or row == key - 1:
            dir_down = not dir_down

        rail[row][col] = '*'
        col += 1

        if dir_down:
            row += 1
        else:
            row -= 1

    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if rail[i][j] == '*':
                rail[i][j] = cipher[index]
                index += 1

    result = ""
    dir_down = False
    row, col = 0, 0
    for i in range(len(cipher)):
        if row == 0 or row == key - 1:
            dir_down = not dir_down

        if rail[row][col] != '*':
            result += rail[row][col]
            col += 1

        if dir_down:
            row += 1
        else:
            row -= 1

    return result



if __name__ == "__main__":
    print(encrypt_rail_fence("Thank you", 2))  # result: 'Takyuhn o'
    print(encrypt_rail_fence("Thank you", 3))  # result: 'Tkuhn oay'

    print(decrypt_rail_fence("Takyuhn o", 2))
    print(decrypt_rail_fence("Tkuhn oay", 3))

