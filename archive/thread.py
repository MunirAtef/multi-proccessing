import threading

def worker():
    print("fnkvkof")


if __name__ == '__main__':
    t1 = threading.Thread(target=worker, daemon=True)


