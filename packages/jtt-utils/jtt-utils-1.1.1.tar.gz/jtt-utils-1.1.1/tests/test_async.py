import asyncio
from asyncio.tasks import FIRST_COMPLETED
loop =asyncio.get_event_loop()
async def foo():
    return 42
    # raise Exception('abab')

async def foo2():
    await asyncio.sleep(1000)
    return 40

async def run():
    task = loop.create_task(foo())
    task2 = loop.create_task(foo2())
    done, pending = await asyncio.wait({task,task2},return_when=FIRST_COMPLETED)

    if task in done:
        print('ok')
        print(task._result)

loop.run_until_complete(run())
        # Everything will work as expected now.