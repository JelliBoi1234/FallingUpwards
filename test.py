import threading, time
import numpy as np


def func(num):
    print(num)


def manyFuncs(num):
    for i in range(num):
        func(i)


funcNum = 100
testEpochs = 10
funcs = [threading.Thread(target=func, args=(i,)) for i in range(funcNum)]
results = np.array([])
testType = 3

match testType:
    case 3:
        # ~0.0007
        for i in range(testEpochs):
            start = time.time()

            manyFuncs(funcNum)

            end = time.time()

            results = np.append(results, end - start)

    case 2:
        # ~0.001
        for i in range(testEpochs):
            start = time.time()

            x = threading.Thread(target=manyFuncs, args=(funcNum,))
            x.start()
            x.join()

            end = time.time()

            results = np.append(results, end - start)

    case 1:

        for i in range(testEpochs):
            funcs = [threading.Thread(target=func, args=(i,)) for i in range(funcNum)]

            start = time.time()

            for e in funcs:
                e.start()

            for x in funcs:
                x.join()

            end = time.time()

            results = np.append(results, end - start)

    case 0:

        for i in range(testEpochs):
            funcs = [threading.Thread(target=func, args=(i,)) for i in range(funcNum)]

            start = time.time()

            for e in funcs:
                e.start()
                e.join()

            end = time.time()

            results = np.append(results, end - start)

print("mean time: ", results.mean())
