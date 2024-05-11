import matplotlib.pyplot as plt


def eqv_digit_bin(num: float, digit: str) -> float:
    num_parts: list[str] = str(num).split('.')
    integer = num_parts[0]

    res = 0

    for i in range(len(integer)):
        if integer[-i - 1] == digit:
            res += 2 ** i

    if len(num_parts) == 1:
        return res

    fraction = num_parts[1]
    for i in range(len(fraction)):
        if fraction[i] == digit:
            res += 2 ** (-i - 1)

    return res


def test_digit():
    print(eqv_digit_bin(0.888, '8'))
    lis_for_first = []
    lis_for_second = []

    for i in range(10000):
        lis_for_first.append(eqv_digit_bin(i, '5'))
        lis_for_second.append(eqv_digit_bin(i, '6'))


    plt.plot(lis_for_first, lis_for_second)
    plt.show()


def main():
    test_digit()


if __name__ == '__main__':
    main()
