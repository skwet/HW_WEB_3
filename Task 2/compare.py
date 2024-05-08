import time
import factorize
import factorize2


def compare():
    data = (128, 255, 99999, 10651060, 70651060, 70651062)

    start_factorize = time.time()
    factorize.factorize(*data)
    end = time.time()
    print(f"Синхронний: {end - start_factorize} секунд\n\n")

    start_multi_pr = time.time()
    factorize2.factorize(*data)
    print(f"Паралельний: {time.time() - start_multi_pr} секунд")


if __name__ == '__main__':
    compare()