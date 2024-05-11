
class Unique_matrix:
    @staticmethod
    def is_valid(matrix, row, col, num):
        for i in range(len(matrix)):
            if matrix[row][i] == num or matrix[i][col] == num:
                return False
        return True

    @staticmethod
    def fill_matrix(matrix, n, idx):
        if idx == n * n:
            return True

        row = idx // n
        col = idx % n

        for num in range(n):
            if Unique_matrix.is_valid(matrix, row, col, num):
                matrix[row][col] = num
                if Unique_matrix.fill_matrix(matrix, n, idx + 1):
                    return True
                matrix[row][col] = -1

        return False

    @staticmethod
    def fill_unique_matrix(n):
        matrix = [[-1 for _ in range(n)] for _ in range(n)]  # Initialize matrix with -1
        Unique_matrix.fill_matrix(matrix, n, 0)
        for r in matrix:
            print(r)
        return matrix

        # if self.fill_matrix(matrix, n, 0):
        #     for row in matrix:
        #         print(row)
        # else:
        #     print("No solution exists for the given size of the matrix.")

class PBI:
    @staticmethod
    def smallest_n(idx):
        n: int = 1
        while factorial(n) <= idx:
            n += 1
        return n

    @staticmethod
    def get_permutation_at_index(n: int, idx: int) -> list[int]:
        if n == -1:
            n = PBI.smallest_n(idx)
        numbers = list(range(n))
        permutation: list[int] = []

        for n in range(n, 0, -1):
            fact = factorial(n - 1)
            permutation.append(numbers.pop(idx // fact))
            idx %= fact

        return permutation

    @staticmethod
    def get_index_of_arrangement(arrangement: list[int]) -> int:
        n = len(arrangement)
        idx = 0
        numbers = list(range(n))

        for i in arrangement:
            n -= 1
            count = numbers.index(i)
            idx += count * factorial(n)
            numbers.remove(i)

        return idx

    @staticmethod
    def place_by_index(list_to_place: list[int], key_list: list[int]) -> list[int]:
        assert len(list_to_place) == len(key_list)
        return [list_to_place[i] for i in key_list]

    @staticmethod
    def get_cycle(idx: int) -> list[int]:
        n: int = PBI.smallest_n(idx)

        list_key: list[int] = PBI.get_permutation_at_index(n, idx)
        perm: list[int] = list(range(n))
        cycle: list[int] = []
        while True:
            perm: list[int] = PBI.place_by_index(perm, list_key)
            index_of_perm: int = PBI.get_index_of_arrangement(perm)
            if index_of_perm == 0:
                break
            cycle.append(index_of_perm)

        return [0] + cycle

    @staticmethod
    def apply_seq(pur_list: list[int]) -> int:
        n: int = PBI.smallest_n(max(pur_list))

        seq: list[int] = list(range(n))

        for key_place in pur_list:
            key_list: list[int] = PBI.get_permutation_at_index(n, key_place)
            seq: list[int] = PBI.place_by_index(seq, key_list)

        return PBI.get_index_of_arrangement(seq)

    @staticmethod
    def div_arranges(idx1, idx2):
        n: int = PBI.smallest_n(max(idx1, idx2))

        perm1 = PBI.get_permutation_at_index(n, idx1)
        perm2 = PBI.get_permutation_at_index(n, idx2)

        res = []
        for i in perm2:
            res.append(perm1.index(i))

        return PBI.get_index_of_arrangement(res)

    @staticmethod
    def inverse(idx: int) -> int:
        n: int = PBI.smallest_n(idx)

        perm = PBI.get_permutation_at_index(n, idx)
        res = [-1] * n

        for i in range(n):
            res[perm[i]] = i

        return PBI.get_index_of_arrangement(res)

    # @staticmethod
    # def get_complementary(n: int, idx: int) -> int:
    #     perm = PBI.get_permutation_at_index(n, idx)
    #     comp_perm = [n - i - 1 for i in perm]
    #     return PBI.get_index_of_arrangement(comp_perm)

    @staticmethod
    def del_zero(n: int, idx: int) -> int:
        perm = PBI.get_permutation_at_index(n, idx)
        perm.remove(0)
        return PBI.get_index_of_arrangement([i - 1 for i in perm])


# def plot_polynomial(coefficients, x_max):
#     num_points = x_max * 10
#     x = np.linspace(0, x_max, num_points)
#     y = np.polyval(coefficients, x)
#     plt.plot(x, y, label="Polynomial function")
#     plt.xlabel("x")
#     plt.ylabel("y")
#     plt.legend()


class ArIdx:
    idx: int

    def __init__(self, idx: int):
        self.idx = idx

    @staticmethod
    def from_perm(perm: list[int]):
        return ArIdx(PBI.get_index_of_arrangement(perm))

    def __add__(self, other):
        return ArIdx(PBI.apply_seq([self.idx, other.idx]))

    def __sub__(self, other):
        return ArIdx(PBI.apply_seq([self.idx, PBI.inverse(other.idx)]))

    def __neg__(self):
        return ArIdx(PBI.inverse(self.idx))

    def __rshift__(self, other):
        return ArIdx(PBI.div_arranges(self.idx, other.idx))

    def __pow__(self, other):
        cycle = PBI.get_cycle(self.idx)
        return ArIdx(cycle[other.idx % len(cycle)])

    def __eq__(self, other):
        return self.idx == other.idx

    def __ne__(self, other):
        return self.idx != other.idx

    def __gt__(self, other):
        return self.idx > other.idx

    def __ge__(self, other):
        return self.idx >= other.idx

    def __lt__(self, other):
        return self.idx < other.idx

    def __le__(self, other):
        return self.idx <= other.idx

    def __len__(self):
        return len(PBI.get_cycle(self.idx))

    def __str__(self):
        return str(self.idx)

    def __getitem__(self, item):
        return

    def perm(self, n=None):
        if n is None:
            n = PBI.smallest_n(self.idx)
        return PBI.get_permutation_at_index(n, self.idx)

    def cycle(self):
        return PBI.get_cycle(self.idx)

    def plot(self):
        n = PBI.smallest_n(self.idx)
        prm = self.perm(n)
        coe = np.polyfit(range(n), prm, n - 1)

        x = np.linspace(0, n, n * 10)
        y = np.polyval(coe, x)
        plt.plot(x, y, label=self.idx)
        # plt.legend()


    def div_mod(self, n: int):
        prm = self.perm()
        return ArIdx.from_perm([i // n for i in prm if i % n == 0])

    def true_div(self, n: int, size=None):
        prm = self.perm(size)
        return [i / n for i in prm]

    def normalize(self, size=None):
        prm = self.perm(size)
        mx = max(prm)
        return [i / mx for i in prm]






def get_factors(n: int):
    factors = list(set(reduce(list.__add__, ([i, n // i] for i in range(1, int(n ** 0.5) + 1) if n % i == 0))))
    factors.sort()
    return factors


def new_l():
    seq = [1]
    seq_index = [1]

    cycle = PBI.get_cycle(seq[0])
    cycle.insert(0, 0)
    print(cycle)
    print()

    while True:
        elem = PBI.apply_seq([seq[-1], seq[-1]])
        if elem in seq:
            seq.append(elem)
            seq_index.append(cycle.index(elem))
            break
        seq.append(elem)
        seq_index.append(cycle.index(elem))

    # 2 ** i % cycle_len
    _ = {
        2: [1, 0, 0],
        3: [1, 2, 1],
        4: [1, 2, 0, 0],
        5: [1, 2, 4, 3, 1],
        6: [1, 2, 4, 2],
        7: [1, 2, 4, 1],
        8: [1, 2, 4, 0, 0],
        9: [1, 2, 4, 8, 7, 5, 1],
        10: [1, 2, 4, 8, 6, 2],

        12: [1, 2, 4, 8, 4],

        14: [1, 2, 4, 8, 2],

        20: [1, 2, 4, 8, 16, 12, 4],

        42: [1, 2, 4, 8, 16, 32, 22, 2],
    }

    for i in range(20):
        print(2 ** i % 14, end=", ")

    print()
    print()
    print(str(len(cycle)) + ":", str(seq_index) + ",")
    print()
    print(seq_index)


def compose_perms():
    p1 = [5, 6, 7, 4, 1, 0, 2, 3]

    print(ArIdx.from_perm(p1))

    print(p1)


"""
for i in large_cycle:
    for j in large_cycle:
        add = ArIdx(i) + ArIdx(j)
        print(large_cycle.index(add.idx), end="\t")
    print()

for i in range(15):
    for j in range(15):
        print((i + j) % 15, end="\t")
    print()
"""

def nums_lead_to():
    nums_to_26 = [
        62, 84, 695, 717, 782, 804, 4535, 4557, 5102, 5124, 5735, 5757, 10862,
        10884, 14495, 14517, 36215, 36237, 36935, 36957, 40382, 40404, 41015,
        41037, 41102, 41124, 44855, 44877, 85742, 85764, 86375, 86397, 90782,
        90804, 116135, 116157, 126782, 126804, 130415, 130437, 131822, 131844,
        157775, 157797, 328535, 328557, 329255, 329277, 333575, 333597, 339335,
        339357, 362942, 362964, 363575, 363597, 363662, 363684, 367415, 367437,
        367982, 368004, 368615, 368637, 373742, 373764, 377375, 377397, 399095,
        399117, 399815, 399837, 766142, 766164, 766775, 766797, 766862, 766884,
        770615, 770637, 806462, 806484, 807095, 807117, 847502, 847524, 851135,
        851157, 1049255, 1049277, 1049975, 1049997, 1134062, 1134084, 1134695,
        1134717, 1139102, 1139124, 1164455, 1164477, 1174382, 1174404, 1175015,
        1175037, 1219742, 1219764, 1244975, 1244997, 1421495, 1421517, 1426535,
        1426557, 1497662, 1497684, 1501295, 1501317, 1502702, 1502724, 1528655,
        1528677, 1537982, 1538004, 1541615, 1541637, 1583342, 1583364, 1608575,
        1608597, 1785695, 1785717, 1790735, 1790757, 3312215, 3312237, 3312935,
        3312957, 3317255, 3317277, 3323015, 3323037, 3352535, 3352557, 3353255,
        3353277, 3397895, 3397917, 3402935, 3402957, 3438935, 3438957, 3443975,
        3443997, 3628862, 3628884, 3629495, 3629517, 3629582, 3629604, 3633335,
        3633357, 3633902, 3633924, 3634535, 3634557, 3639662, 3639684, 3643295,
        3643317, 3665015, 3665037, 3665735, 3665757, 3669182, 3669204, 3669815,
        3669837, 3669902, 3669924, 3673655, 3673677, 3714542, 3714564, 3715175,
        3715197, 3719582, 3719604, 3744935, 3744957, 3755582, 3755604, 3759215,
        3759237, 3760622, 3760644, 3786575, 3786597, 3957335, 3957357, 3958055,
        3958077, 3962375, 3962397, 3968135, 3968157, 7620542, 7620564, 7621175,
        7621197, 7621262, 7621284, 7625015, 7625037, 7625582, 7625604, 7626215,
        7626237, 7631342, 7631364, 7634975, 7634997, 7656695, 7656717, 7657415,
        7657437, 7983422, 7983444, 7984055, 7984077, 7984142, 7984164, 7987895,
        7987917, 8351342, 8351364, 8351975, 8351997, 8356382, 8356404, 8381735,
        8381757, 8714942, 8714964, 8718575, 8718597, 8719982, 8720004, 8745935,
        8745957,   # under 10000000
    ]


    # filtered = [nums_to_26[i] for i in range(len(nums_to_26)) if i % 2 == 0]
    # for i in filtered:
    #     print(ArIdx(i).perm(PBI.smallest_n(i)))
    #
    # slope = []
    # for i in range(len(nums_to_26) - 1):
    #     slope.append(nums_to_26[i + 1] - nums_to_26[i])
    #
    # plt.plot(slope)
    # plt.show()
    # print(filtered)

    num3_to_26 = [26, 1379, 4379, 5786, 9539, ]

    print(ArIdx(2) + ArIdx(2))
    print("========================")
    for i in range(1000):
        num = ArIdx(i)
        if (num + num).idx == 1:
            print(num, end=", ")
            # nums_to_26.append(num.idx)
            # cycle = num.cycle()
            # print(len(cycle), cycle)


    # print(nums_to_26)

    # for n in filtered:
    #     print(ArIdx(n).cycle())
    #
    # for i in range(len(filtered) - 1):
    #     print(filtered[i + 1] - filtered[i])




    # y = f(x, slider.val)  # Update y values based on slider value
    # y = f(x, val)  # Update y values based on slider value
    # line.set_ydata(y)  # Update the line data
    # fig.canvas.draw_idle()


def fraction():
    ar = ArIdx(23)
    div = ar.normalize()
    print(div)
    return

    for i in range(6):
        ar = ArIdx(i)
        # div = ar.div_mod(2)
        print(ar.true_div(n=2, size=5))
        continue

        if not (div.idx == 0 or div.idx == 1):
            print(i, "\t", div, "\t", ar.idx / 2)
            # print("====================================")


def valid_del(perm1: list[int], perm2: list[int]) -> list[int]:
    length = len(perm1)
    assert length == len(perm2)
    valid: list[int] = []

    for i in range(length):
        temp1 = perm1.copy()
        temp1.remove(i)

        temp2 = perm2.copy()
        temp2.remove(i)

        equal = True
        for j in range(length - 1):
            if temp1[j] != temp2[j]:
                equal = False
                break
        if equal:
            valid.append(i)

    return valid


def get_matrix(idx: int):
    perm = ArIdx(idx).perm()
    perm_len = len(perm)
    matrix = []
    for i in perm:
        row = [0] * perm_len
        row[i] = 1
        matrix.append(row)

    return matrix



def main():
    num3_to_26 = [26, 1379, 4379, 5786, 9539, ]
    nums_lead_to()

    for i in get_matrix(26):
        print(i)
    # print(get_matrix(26))

    # n = 3
    # for i in range(factorial(n) - 1):
    #     print(i, end="\t")
    #     valids = valid_del(ArIdx(i).perm(n), ArIdx(i + 1).perm(n))
    #     print(len(valids))
    #     print(ArIdx(i).perm(4))

    # nums_lead_to()

    return
    keys = []
    sub_dict: [int, list[int]] = {

    }

    for i in range(0, 10000, 1):
        sub: int = (-ArIdx(i) + ArIdx(i + 1)).idx
        if sub in keys:
            sub_dict[sub].append(i + 1)
        else:
            keys.append(sub)
            sub_dict[sub] = [i + 1]
        # print(i, "\t", )

    # print(keys)
    # for i in range(len(keys) - 1):
    #     print(keys[i] % 3)
        # print((keys[i - 1] - keys[i]) % 100)


    for key in keys:
        seq: list[int] = sub_dict[key]
        if len(seq) == 1:
            continue
        # print("{},\t\t {},\t\t {}".format(key, seq[0], seq[1] - seq[0]))

        perm = PBI.get_permutation_at_index(PBI.smallest_n(key), key)
        print(perm, "\t", seq[1] - seq[0])
        print()
        # print()
    # print(sub_dict)

    return
    # [0, 78942, 354909, 245099, 200, 79134, 354543, 245243, 488, 78775, 354717, 245339]
    print(PBI.get_permutation_at_index(4, 7))
    c = ArIdx(742).cycle()
    print(c)
    print()

    for i in c:
        print(ArIdx(i).cycle())

    print()
    print()
    c = ArIdx(627).cycle()
    print(c)
    print()

    for i in c:
        print(ArIdx(i).cycle())

    exit(0)
    c = ArIdx(805).cycle()
    print(c)

    # c.pop(0)
    # for i in c:
    #     print(i % (24 * 5 * 6 * 7))
    # print(get_factors(i))

    exit(0)
    # print(PBI.get_permutation_at_index(-1, 1435))

    # vdx = 7771
    # i1 = ArIdx(vdx)
    #
    # i2 = i1 + i1
    # i3 = i1 + i1 + i1

    i1 = 78775
    i2 = 78775
    i3 = 354909

    print(i1 + i2 + i3)
    print(i2 + i3 + i1)
    print(i3 + i2 + i1)

    return

    vycle = ArIdx(vdx).cycle()
    last_two: list[ArIdx] = [ArIdx(0), ArIdx(vdx)]

    for i in range(40):
        last_two.append(last_two[-2] + last_two[-1])
        print(vycle.index(last_two[-1].idx), end="\t")
        # print(last_two[-1])

    return
    # zom-ra
    cycle = ArIdx(7462014).cycle()

    test = cycle[5]
    c_test = ArIdx(test).cycle()
    c_idx = [cycle.index(i) for i in c_test]

    print(cycle)
    print(c_idx)

    # cycle2 = ArIdx(1133427).cycle()
    #
    # c2_idx = [large_cycle.index(i) for i in cycle2]
    # print(c2_idx)
    return

    # print(ArIdx(335) + ArIdx(285) + ArIdx(80) + ArIdx(335) + ArIdx(335))
    # print(ArIdx(335) - ArIdx(285))

    ar1 = ArIdx(800)
    ar2 = ArIdx(692)

    a = ar1 + ar2
    b = ar2 + ar1

    print(a)
    print(b)

    print(b + a)

    return
    add = []
    sub = []

    for i in range(24):
        for j in range(24):
            i1 = ArIdx(i)
            i2 = ArIdx(j)

            add.append((i1 + i2).idx)
            sub.append((i1 + i2).idx)

    plt.plot(add, sub)
    plt.show()
    return

    # i1 = ArIdx(7967)
    # i2 = ArIdx(6133)
    #
    # print([i1, i2])
    # print(-i1 + i2)
    # print(i1 >> i2)

    for i in range(6):
        for j in range(6):
            print(ArIdx(j) - ArIdx(i), end="\t")
        print()

    print()
    print()
    print()
    for i in range(6):
        for j in range(6):
            print(ArIdx(j) + ArIdx(i), end="\t")
        print()

    print(")))))))))))))))))))))))))))))))))))))))))))))))))))")

    # -(i1 - i2 + i3 - i4 + i5 - i6) = i6 - i5 + i4 - i3 + i2 - i1
    print(")))))))))))))))))))))))))))))))))))))))))))))))))))")

    # print(i1 - i2)

    # print(PBI.apply_seq([i1.idx, i2.idx, i1.idx]))
    # print(PBI.div_arranges(PBI.inverse(m1), m2))
    # print(PBI.div_arranges(i1.idx, i2.idx))

    return

    print(PBI.div_arranges(50, 0))
    print(PBI.inverse(50))
    print()

    for i in range(6):
        for j in range(6):
            print(PBI.div_arranges(j, i), end="\t")
        print()

    # print(PBI.div_arranges(50, 70))
    # print(PBI.apply_seq([50, 20]))
    print()
    print()

    rows = []
    for i in range(0, 6):
        row = []
        for j in range(0, 6):
            res = PBI.apply_seq([j, i])
            row.append(res)
            print(res, end="\t")
        rows.append(PBI.get_index_of_arrangement(row))
        print()
    return

    print()
    print()
    print(rows)

    slope = [(rows[i + 1] / (rows[i] + 1)) for i in range(len(rows) - 1)]
    print(slope)
    plt.plot(slope)
    plt.show()

    return
    # cycle = PBI.get_cycle(47961)
    # single_cycle = [i for i in range(900) if len(PBI.get_cycle(i)) == 1]
    # cycles_len = [len(PBI.get_cycle(i)) for i in range(100)]
    # slope = [log(log(single_cycle[i])) for i in range(1, len(single_cycle))]

    c = 140
    arr = [PBI.apply_seq([i, c]) for i in range(factorial(4))]
    # slope = [arr[i+1] - arr[i] for i in range(len(arr) - 1)]
    # slope2 = [slope[i+1] - slope[i] for i in range(len(slope) - 1)]
    # slope3 = [slope2[i+1] - slope2[i] for i in range(len(slope2) - 1)]

    plt.plot(arr)
    plt.show()

    return
    c = 3
    arr = [PBI.apply_seq([c, i]) for i in range(5000)]
    plt.plot(arr)

    c = 4
    arr = [PBI.apply_seq([c, i]) for i in range(5000)]
    plt.plot(arr)

    # plt.plot([0, 5000], [0, 5000])
    plt.show()

    return

    matrix = []
    for i in range(24, 48):
        row = []
        for j in range(0, 24):
            res = PBI.apply_seq([j, c])
            row.append(res % 6)
            print(res % 6, end="\t")
        print()
        matrix.append(row)

    # patterns = [0, 136, 289, 430, 583, 719]
    # = [
    # [0, 1, 2, 3, 4, 5],
    # [1, 0, 4, 5, 2, 3],
    # [2, 3, 0, 1, 5, 4],
    # [3, 2, 5, 4, 0, 1],
    # [4, 5, 1, 0, 3, 2],
    # [5, 4, 3, 2, 1, 0]
    # ]

    # matches = []
    #
    # for i in range(factorial(n)):
    #     row = []
    #     for j in range(0, factorial(n), 6):
    #         temp_sub_list = matrix[i][j:j+6]
    #         idx = PBI.get_index_of_arrangement(temp_sub_list)
    #         row.append(patterns.index(idx))
    #     matches.append(row)
    #
    # print()
    # print()
    # for row in matches:
    #     print(row)

    # print()
    # print()
    # dt = []
    # for row in matrix:
    #     try:
    #         dt.append(PBI.get_index_of_arrangement(row))
    #         print()
    #     except:
    #         print("error: ", row)
    # print(dt)
    # _sum = sum(dt) / factorial(factorial(n))
    # print(_sum / n)
    # for i in range(1, len(dt)):
    #     _sum += dt[i] / factorial(factorial(n))
    #
    #     print((dt[i] - dt[i-1]) / factorial(factorial(n)))

    # print()
    # plt.plot(dt)
    # plt.show()

    # Unique_matrix.fill_unique_matrix(6)

    # n = 4
    # opp = [PBI.get_opposite(n, i) for i in range(factorial(n))]
    # print(opp)
    # plt.plot(opp)
    # plt.show()

    #

    # idx = 22
    #
    # print(get_permutation_at_index(n, idx))
    #
    # print(get_opposite(n, idx))

    # print(get_cycle(n, idx))

    # rev_idx = []
    #
    # for i in range(0, factorial(n + 1)):
    #     perm = get_permutation_at_index(n, i)
    #     perm.reverse()
    #     rev_idx.append(get_index_of_arrangement(perm))
    #
    # print(rev_idx)

    # print("{}\t\t\t\t{}".format(factorial(first), get_index_of_arrangement(rev_idx)))
    # print(log(factorial(rev_idx[0] + 1) - get_index_of_arrangement(rev_idx)) / log(factorial(n + 1)))
    # print(factorial(first) / get_index_of_arrangement(rev_idx))

    # get_index_of_arrangement(rev_idx)


if __name__ == '__main__':
    from math import factorial
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    from functools import reduce
    import numpy as np

    main()
