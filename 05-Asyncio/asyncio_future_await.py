# asyncio_future_event_loop.py

# https://pymotw.com/3/asyncio/futures.html

import asyncio
import time

def mark_done(future, result):
    
    time.sleep(10)
    
    print('setting future result to {!r}'.format(result))
    future.set_result(result)

@asyncio.coroutine
def main(loop):
    
    all_done = asyncio.Future()

    print('scheduling mark_done')
    loop.call_soon(mark_done, all_done, 'the result')

    result = yield from all_done
    print('returned result: {!r}'.format(result))

event_loop = asyncio.get_event_loop()

try:

    event_loop.run_until_complete(main(event_loop))

finally:
    
    event_loop.close()