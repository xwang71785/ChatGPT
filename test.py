import asyncio
import time


async def main():
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, blocking)
    print(f'{time.ctime()} hello!')
    await asyncio.sleep(3)
    print(f'{time.ctime()} goodbye!')


def blocking():
    time.sleep(4)
    print(f'{time.ctime()} hello from blocking!')


if __name__ == '__main__':
    asyncio.run(main())