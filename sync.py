import multiprocessing as mp
import time


def increment(num, lock):
    for i in range(5000):
        lock.acquire()
        num.value = num.value + 1
        lock.release()

def decrement(num, lock):
    for i in range(5000):
        lock.acquire()
        num.value = num.value - 1
        lock.release()


# # just for clarification
# def increment(num):
#     temp = num.value + 1
#     time.sleep(0.01)
#     num.value = temp
#
#
# def decrement(num):
#     temp = num.value - 1
#     time.sleep(0.01)
#     num.value = temp


def main():
    shared_num = mp.Value('i', 9)

    lock = mp.Lock()

    p1 = mp.Process(target=increment, args=(shared_num, lock))
    p2 = mp.Process(target=decrement, args=(shared_num, lock))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print(shared_num.value)


if __name__ == '__main__':
    main()

