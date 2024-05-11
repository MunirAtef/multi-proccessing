
import multiprocessing as mp
import time


def append_if_not_exists(set_ds, num, lock):
    lock.acquire()
    if num not in set_ds:
        time.sleep(0.01)
        set_ds.append(num)
    lock.release()


def main():
    shared_set: list[int] = mp.Manager().list([])

    lock = mp.Lock()
    p1 = mp.Process(target=append_if_not_exists, args=(shared_set, 8, lock))
    p2 = mp.Process(target=append_if_not_exists, args=(shared_set, 8, lock))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print(shared_set)


if __name__ == '__main__':
    main()
