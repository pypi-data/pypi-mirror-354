from jtt_tm_utils.sync_basedata import data_manager
import aioredis
import os
import asyncio
import logging
import functools


import unittest
import json
from jtt_tm_utils.timeutil import linux_timestamp
from datetime import datetime
carid ='737-V2'

class CliTestCase(unittest.TestCase):
    def setUp(self):
        async def _setup():
            redis = await aioredis.create_redis_pool('redis://192.168.101.72:6380/0')
            self.manager.config(redis,['vehicle','vehicle.config','line.config'])
            await redis.hset('bd:vehicle:%s' % carid,'writer','candy')
            await redis.hset('bd:vehicle.config:%s' % carid, 'event_params_265', json.dumps({'test':'test0'}))
            return redis

            #

        logging.basicConfig(level=10, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        self.loop =asyncio.get_event_loop()
        self.manager = data_manager

        self.redis =self.loop.run_until_complete(_setup())



    # def test_up_project(self):
    #     os.chdir(os.path.join(self.projectname))
    #     up_project()


    def test_makemethod(self):

        async def set_writer():
            await self.redis.hset('bd:vehicle:%s' % carid, 'writer', 'candyabc')
            await self.redis.hset('bd:vehicle.config:%s' % carid,'event_params_265',json.dumps({'test':'test'}))
            await self.redis.zadd('bd_updatekeys',linux_timestamp(), 'bdupd.vehicle.%s_{"time": %s, "act": "upd", "tables": ["vehicle"]}' %(carid,linux_timestamp()))
            await self.redis.hset('sync_record', 'lastmodifytime', datetime.now().strftime('%Y%m%d%H%M%S%f'))
        async def set_lineconfig():
            await self.redis.zadd('bd_updatekeys',linux_timestamp(), 'bdupd.line_config.%s_{"time": %s, "act": "upd", "tables": ["line_config"]}' %(20,linux_timestamp()))
            await self.redis.hset('sync_record', 'lastmodifytime', datetime.now().strftime('%Y%m%d%H%M%S%f'))

        async def write_synctime():
            t = str(linux_timestamp())
            await self.redis.zadd('bd_updatekeys',linux_timestamp(), 'bdupd.basedata.recreateall_{"act":"upd","time":%s,"tables":["recreateall"]}' % t)
            await self.redis.hset('sync_record','lastmodifytime',datetime.now().strftime('%Y%m%d%H%M%S%f'))
            print('write_synctime')

        asyncio.ensure_future(data_manager.sync_data())

        vt = self.loop.run_until_complete(self.manager.get_vehicle(carid))
        config = self.loop.run_until_complete(self.manager.event_config(carid,265))
        print(vt)
        print(config)
        lineconfig = self.loop.run_until_complete(self.manager.get_line_config(20))
        print(lineconfig)
        assert vt['writer'] == 'candy'
        self.loop.run_until_complete(asyncio.sleep(1))
        # self.loop.run_until_complete(set_writer())
        self.loop.run_until_complete(set_lineconfig())
        # self.redis.publish('bdupd.vehicle.%s' % carid,
        #                    json.dumps({"act": "upd", "time": linux_timestamp(), "tables": ["vehicle"]}))
        # self.loop.run_until_complete(write_synctime())
        # self.loop.run_until_complete(asyncio.sleep(40))

        # self.manager.custom_reload()
        # self.manager.custom_reload_item('vehicle', carid)
        self.loop.run_until_complete(asyncio.sleep(30))
        # vt = self.loop.run_until_complete(self.manager.get_vehicle(carid))
        # assert vt['writer']=='candyabc','vt write is not valid %s' % vt['writer']
        # config = self.loop.run_until_complete(self.manager.event_config(carid,265))
        # assert config['test'] == 'test', 'vt load config fail.'
        # print(config)
        # print('read write ok %s' % vt['writer'])
        lineconfig = self.loop.run_until_complete(self.manager.get_line_config(20))
        print(lineconfig)

        self.loop.run_forever()


