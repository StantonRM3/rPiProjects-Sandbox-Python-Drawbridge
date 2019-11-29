import asyncio
import functools

def callback(n):
    print('callback {} invoked'.format(n))

@asyncio.coroutine
def main(loop):
    
    print('registering callbacks')
    loop.call_later(5, callback, 1)
    loop.call_later(10, callback, 2)
    loop.call_soon(callback, 3)

    yield from asyncio.sleep(12)

event_loop = asyncio.get_event_loop()

try:

    print('entering event loop')
    event_loop.run_until_complete(main(event_loop))

finally:

    print('closing event loop')
    event_loop.close()
