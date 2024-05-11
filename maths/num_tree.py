
class ConsoleColors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

    RESET = '\033[0m'


class NumTree:
    def __init__(self, val):
        self.val = val

    @staticmethod
    def get_digits_keys(num: int) -> dict[int, int]:
        integer = str(num)
        res: dict[int, int] = {}

        for i in range(len(integer)):
            digit = int(integer[-i - 1])
            if digit == 0:
                continue
            if res.get(digit) is None:
                res[digit] = 2 ** i
            else:
                res[digit] += 2 ** i

        return res

    def get_tree(self, current_dict: dict[int, int]) -> dict[int, object]:
        result: dict[int, object] = current_dict.copy()
        for key in current_dict:
            value = current_dict[key]
            if value > 9:
                result[key] = self.get_tree(self.get_digits_keys(value))

        return result

    def tree(self):
        return self.get_tree({1: self.val})

    def __str__(self):
        return str(self.tree())


class UnderTest:
    @staticmethod
    def get_digits_keys(num: float) -> dict[int, float]:
        num_parts: list[str] = str(num).split('.')
        integer = num_parts[0]

        res = {}

        for i in range(len(integer)):
            digit = int(integer[-i - 1])
            if res.get(digit) is None:
                res[digit] = 2 ** i
            else:
                res[digit] += 2 ** i

        if len(num_parts) == 1:
            return res

        fraction = num_parts[1]
        for i in range(len(fraction)):
            digit = int(fraction[i])
            if res.get(digit) is None:
                res[digit] = 2 ** (-i - 1)
            else:
                res[digit] += 2 ** (-i - 1)

        return res

    def get_tree(self, current_dict: dict[int, float]) -> dict[int, object]:
        result: dict[int, object] = current_dict.copy()
        for key in current_dict:
            value = current_dict[key]
            if value > 9:
                result[key] = self.get_tree(self.get_digits_keys(value))

        return result


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


def print_tree_two(tree, indent=0):
    for key, value in tree.items():
        if isinstance(value, dict):
            print("\t" * indent + str(key) + ": ")
            print_tree_two(value, indent + 1)
        else:
            print("\t" * indent + str(key) + ": " + str(value))



def main():
    # num_tree = {1: {2: {6: 1, 3: 2}, 1: {4: 1, 6: 2, 2: 4}, 9: {6: 1, 1: 2}, 8: {8: 3, 1: 8}, 7: {4: 2, 6: 4}}}
    num_tree: dict[int, object] = NumTree(26265502256).tree()
    print(num_tree)
    print(tree_branches(num_tree))
    # print(num_tree)
    #
    # for key in num_tree[1]:
    #     print(key, end="\t")

    # bin: 11010
    # hex: 1a
    # oct: 32

    print_tree(num_tree)

    # print(tree_to_num(num_tree[1]))
    # print(math.factorial(14))
    #
    # print(NumTree(math.factorial(14)))


if __name__ == '__main__':
    main()
