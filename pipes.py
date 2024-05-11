import multiprocessing as mp
from multiprocessing.connection import Connection
import time


def pipe_zero(pipe: tuple[Connection, Connection]):
    pipe[1].send("message 0 from process one")
    pipe[1].send("message 1 from process one")
    pipe[1].send("message 2 from process one")
    pipe[1].send(None)

    while True:
        time.sleep(0.5)
        msg = pipe[0].recv()
        if msg is None:
            break
        print(msg)


def pipe_one(pipe: tuple[Connection, Connection]):
    pipe[0].send("message 0 from process two")
    pipe[0].send("message 1 from process two")
    pipe[0].send("message 2 from process two")
    pipe[0].send(None)

    while True:
        time.sleep(0.5)
        msg = pipe[1].recv()
        if msg is None:
            break
        print(msg)



def main():
    pipe: tuple[Connection, Connection] = mp.Pipe()

    p1 = mp.Process(target=pipe_zero, args=(pipe,))
    p1.start()

    p2 = mp.Process(target=pipe_one, args=(pipe,))
    p2.start()


if __name__ == '__main__':
    main()

