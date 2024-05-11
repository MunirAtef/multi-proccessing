
import multiprocessing as mp
import time


def receive_messages(queue: mp.Queue):
    while True:
        message = queue.get(timeout=5)
        print(message)
        if message is None:
            break

    # time.sleep(1)
    # while not queue.empty():
    #     message = queue.get(timeout=2)
    #     print(message)


def send_messages(queue):
    queue.put("Hello")
    time.sleep(1)
    queue.put("message 1")
    time.sleep(1)
    queue.put("message 2")
    time.sleep(1)
    queue.put(None)



def main():
    queue = mp.Queue()
    queue.put("first message from main")

    p2 = mp.Process(target=send_messages, args=(queue,))
    p1 = mp.Process(target=receive_messages, args=(queue,))

    p1.start()
    p2.start()


if __name__ == '__main__':
    main()

