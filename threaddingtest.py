import time

class MyData:
    G = 0

def update1(A, i):
    threadLock.acquire()
    for i in range(100):
        y = A.G
        time.sleep(0.0001)
        A.G = y + 1
    threadLock.release()

import threading
threadLock = threading.Lock()
thread_list = []
for i in range(100):
    x = threading.Thread(target=update1, args = (MyData, i, ))
    x.start()
    thread_list.append(x)

for x in thread_list:
        x.join() # wait for x to terminate.

print(MyData.G)