import logging
import threading
import time

global count
count = 0
lock = threading.Lock()
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

def worker(num):
    while(1):
        global count
        lock.acquire()
        count += 1
        time.sleep(1)
        lock.release()
        print(str(count) + "\n")
        time.sleep(1)

threading.Thread(name='my_service', target=worker,args=(1,)).start()
threading.Thread(name='worker', target=worker,args=(2,)).start()
threading.Thread(target=worker,args=(3,)).start()
