import _thread as thread
import time


global count
count = 0

def counter(threadId, delay):
    global count 
    count += 1
    print(count)


try:
    thread.start_new_thread(counter, ("th",0))
    thread.start_new_thread(counter, ("thread2",0))
except:
    print("bruh")
    
print(count)
