
import multiprocessing as mp


def square_list(nums):
    for i in range(len(nums)):
        nums[i] **= 2

def print_list(nums):
    for i in nums:
        print(i)


def append_to_list(_list: list[int], num: int):

    if num not in _list:
        for i in range(100000):
            pass
        _list.append(num)


if __name__ == '__main__':
    nums = [1, 2, 3, 4]

    mp.freeze_support()

    manager = mp.Manager()
    shared_list: list[int] = manager.list(nums)

    p1 = mp.Process(target=square_list, args=(shared_list,))
    p1.start()
    p1.join()

    p2 = mp.Process(target=print_list, args=(shared_list,))
    p2.start()
    p2.join()


    p3 = mp.Process(target=append_to_list, args=(shared_list, 8))
    p4 = mp.Process(target=append_to_list, args=(shared_list, 8))

    p3.start()
    p4.start()
    p3.join()
    p4.join()

    print(shared_list)
    # square_list(nums)
    # print(nums)


