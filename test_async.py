# single thread but multiple coroutines
import asyncio
import multiprocessing
import threading
import time
import os
import psutil
from datetime import datetime

def get_current_cpu_core():
    process = psutil.Process(os.getpid())
    return process

def count(n):
    # CPU密集型函数
    start = time.time()
    process_id = os.getpid()
    core = get_current_cpu_core()
    print(f'process {process_id} on core {core} starts at {datetime.now()}')
    counter = 0
    while counter < n:
        counter += 1
    end = time.time()
    print(f'Counted {n} process {process_id} in {end-start} seconds')
    return counter

def hello(n):
    # I/O密集型函数
    t_name = threading.current_thread().name
    time.sleep(1)
    print(f'Hello {n} World {t_name} starts {datetime.now()}')
    time.sleep(10)
    print(f'Hello {n} is back {datetime.now()}')

async def a_hello(n):
    # I/O密集型协程
    t_name = threading.current_thread().name
    print(f'a_hello{n} {t_name} starts {datetime.now()}')
    await asyncio.sleep(10-2*n)
    print(f'a_hello{n} is done {datetime.now()}')


async def main():
    print(f'Main starts at {datetime.now()}')
# 创建3个线程
    threads = []
    for i in range(3):
        t = threading.Thread(target=hello, args=(i,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

# create tasks to launch coroutines
    tasks = []
    for i in range(3):
        tasks.append(a_hello(i))
    # register and kick off all tasks and wait for all to complete
    await asyncio.gather(*tasks)    # await必须在async定义的函数中使用
    
# create tasks to launch processes
    #with multiprocessing.Pool(processes=3) as pool:
    #    pool.map(count, [100000000, 100000000, 100000000])  # 3 processes

    # create processes
    #p1 = multiprocessing.Process(target=count, args=(100000000,))
    #p2 = multiprocessing.Process(target=count, args=(100000000,))
    #p3 = multiprocessing.Process(target=count, args=(100000000,))
    #p1.start()
    #p2.start()
    #p3.start()
    #p1.join()
    #p2.join()
    #p3.join()

    print(f'Main is back {datetime.now()}')


if __name__ == "__main__":
    asyncio.run(main())
#    main()
