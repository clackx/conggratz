import asyncio
import datetime
from config import DBUSER, DBNAME
import asyncpg


class Evdb:

    def __init__(self):
        self.pool = None

    async def create_pool(self):
        if not self.pool:
            dsn = f"postgres://{DBUSER}@127.0.0.1:5432/{DBNAME}"
            self.pool = await asyncpg.create_pool(dsn=dsn)
            print('[ evdb connection ok ]')

    async def try_commit(self, query, values):
        if not self.pool:
            await self.create_pool()

        async with self.pool.acquire() as con:
            try:
                await con.execute(query, *values)
            except asyncpg.exceptions.PostgresError as error:
                print('!! echoer postgres error ::', error)

    async def add_to_events(self, tstamp, evt, usr, txt):
        query = f"INSERT INTO events VALUES (to_timestamp($1), $2, $3, $4)"
        values = (tstamp, evt, usr, txt)
        await self.try_commit(query, values)

    async def add_datawarn(self, entity, message):
        query = f"INSERT INTO datawarn VALUES ($1, $2) ON CONFLICT DO NOTHING"
        values = (entity, message)
        await self.try_commit(query, values)


async def echo(message):
    tstamp = float(datetime.datetime.now().strftime('%s.%f'))
    if message[0] == 'I':
        usr = message.split()[2]
        evt = message.split()[3]
        txt = message[7 + len(usr) + len(evt):]
    elif message[0] == 'W':
        usr = message.split()[1]
        txt = message[3 + len(usr):]
        evt = 'WRN'
    elif message[0] == 'E':
        usr = message.split()[1]
        txt = message[2:]
        evt = 'ERR'
    else:
        (evt, usr, txt) = ('', '', '')

    await evdb.add_to_events(tstamp, evt, usr, txt)


async def dwarn(message):
    strips = message.split()
    entity = strips[0]
    message = message[len(entity) + 1:]
    await evdb.add_datawarn(entity, message)


evdb = Evdb()
