import asyncio
import time

# Borrowed from http://curio.readthedocs.org/en/latest/tutorial.html.
@asyncio.coroutine
def countdown(number, n):
    while n > 0:
        print('Step1', n, '({})'.format(number), end="---->")
        print('T-minus', n, '({})'.format(number))
        time.sleep(5)
        print('T-minus', n, '({})'.format(number))
        yield from asyncio.sleep(10)
        n -= 1
        print('Step3', n, '({})'.format(number))


loop = asyncio.get_event_loop()
tasks = [
    asyncio.ensure_future(countdown("A", 2)),
    asyncio.ensure_future(countdown("B", 3))]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

        print('Step2', n, '({})'.format(number), end="---->")