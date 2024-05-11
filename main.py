
import multiprocessing as mp

def square_list(nums):
    for i in range(len(nums)):
        nums[i] **= 2

def print_list(nums):
    for i in nums:
        print(i)


if __name__ == '__main__':
    nums = [1, 2, 3, 4]

    shared_list: object = mp.Array('i', nums)

    p1 = mp.Process(target=square_list, args=(shared_list,))
    p1.start()
    p1.join()

    p2 = mp.Process(target=print_list, args=(shared_list,))
    p2.start()
    p2.join()
    # square_list(nums)
    # print(nums)




