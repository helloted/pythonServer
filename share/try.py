
import time

if __name__ == '__main__':
    i = 0
    while True:
        time.sleep(1)
        i += 1
        if i == 10:
            raise Exception("a", "b")


