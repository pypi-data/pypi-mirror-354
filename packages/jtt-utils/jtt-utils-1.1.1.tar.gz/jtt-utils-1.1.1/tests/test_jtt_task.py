import asynctest
from tests.redis_manager import redis_manager
from jtt_tm_utils.jtt_task import JttTaskManager
class TestJttTask(asynctest.TestCase):
    async def setUp(self):
        await redis_manager.aload_configs(['jtt_task'])
        self.manager = JttTaskManager(redis_manager.jtt_task)
        self.carid = '101-FX'
        print('setup')


    async def test_create_task(self):
        # await asyncio.sleep(2)
        # print('ok')

        task =await self.manager.create_task('101-FX', 'upgrade', {}, user='super')
        print(task)
        # await self.manager.create_task('101-FX', 'upgrade', {}, user='super')