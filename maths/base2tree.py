from typing import List


class ConsoleColors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

    RESET = '\033[0m'


class BaseTwoTree:
    def __init__(self, b2num: int):
        self.b2num = b2num

    @staticmethod
    def __get_dig_values(base2num: int) -> dict[int, int]:
        base2num = str(base2num)
        res = {}
        for i in range(len(base2num)):
            dig = int(base2num[-i - 1])
            if res.get(dig) is None:
                res[dig] = 10 ** (i // 2) * (i % 2 + 1)
            else:
                res[dig] += 10 ** (i // 2) * (i % 2 + 1)

        return res

    def __get_tree(self, current_dict: dict[int, int]) -> dict[int, object]:
        result: dict[int, object] = current_dict.copy()
        for key in current_dict:
            value = current_dict[key]
            if value > 9:
                result[key] = self.__get_tree(self.__get_dig_values(value))

        return result

    def tree(self):
        return self.__get_tree({1: self.b2num})


"""
{1: 201, 3: 3002, 2: 10110, 0: 20}
"""

"""
000    0
001    1
010    2
011    3
100    4
101    5
110    6
111    7
"""

def kv_mul(key: int, val: int) -> int:
    return int(bin(val)[2:]) * key


def tree_to_num(tree: dict[int, object]) -> int:
    num: int = 0

    for key, val in tree.items():
        if isinstance(val, dict):
            val = tree_to_num(val)
        num += kv_mul(key, val)

    return num


def tree_branches(tree: dict[int, object], parent="") -> list[str]:
    branches: list[str] = []

    for key, val in tree.items():
        if isinstance(val, dict):
            branches += tree_branches(val, parent + str(key))
        else:
            branches.append(parent + str(key) + str(val))

    return branches


def print_tree(tree: dict[int, object], depth=0):
    tab = 0 if depth == 0 else 1

    for key, val in tree.items():
        if isinstance(val, int):
            print(ConsoleColors.CYAN, end="")
            print("    |" * (depth - 1) + "___ " * tab, end="")
            print(ConsoleColors.RED, end="")
            print(key, ConsoleColors.GREEN + "->" + ConsoleColors.RED, val)
        elif isinstance(val, dict):
            print(ConsoleColors.CYAN, end="")
            print("    |" * (depth - 1) + "___ " * tab, end="")
            print(ConsoleColors.RED, end="")
            print(key)
            print_tree(val, depth + 1)
            print(ConsoleColors.CYAN, end="")
            print("    |" * (depth - 1))


def main():
    # {2: '100010100', 3: '11000010', 1: '100001', 0: '1000'}

    num_tree = BaseTwoTree(1201201202)
    print_tree(num_tree.tree())
    branches: list[str] = tree_branches(num_tree.tree())
    branches.sort()

    for branch in branches:
        # print(int(branch, 4))
        print(branch[1:])
    

    # print(BaseTwoTree.get_dig_values(233120231))
    # print(num_tree.to_tree())

    # print(BaseTwoTree.get_digits_keys("233120231"))
    # print(BaseTwoTree.get_dig_values("233120231"))


"""
0   
1

00  0
01  1
10  2
11  3
"""

if __name__ == '__main__':
    main()
