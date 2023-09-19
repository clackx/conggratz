import asyncio
import asyncpg
import aiosqlite
from config import DBUSER, DBNAME
import elogger


def to_tuple_string(elements):
    if type(elements) == str:
        return f"('{elements}')"
    else:
        if len(elements) == 1:
            return f"('{tuple(elements)[0]}')"
        else:
            return str(tuple(map(str, elements)))


class Mdb:
    (ALL, ONE) = (8, 0)

    def __init__(self):
        self.pool = None


    async def create_pool(self):
        if not self.pool:
            dsn = f"postgres://{DBUSER}@127.0.0.1:5432/{DBNAME}"
            self.pool =  await asyncpg.create_pool(dsn=dsn)
            print('[ maindb connection ok ]')


    async def try_fetch(self, query, qtype):
        if not self.pool:
            await self.create_pool()

        async with self.pool.acquire() as con:
            data = ''
            try:
                if qtype == Mdb.ALL:
                    data = await con.fetch(query)
                elif qtype == Mdb.ONE:
                    data = await con.fetchval(query)
            except asyncpg.exceptions.PostgresError as error:
                await elogger.error(f'!! postgres error :: {error}')
            elogger.exiter(f'[OK] {len(data) if data else 0} elms {len(str(data))} chrs', data)
            return data

    async def try_commit(self, query):
        if not self.pool:
            await self.create_pool()

        async with self.pool.acquire() as con:
            try:
                await con.execute(query)
                return True
            except asyncpg.exceptions.PostgresError as error:
                await elogger.error(f'!! postgres error :: {error}')

    def get_day_intro(self, bdate, locale, offset, count):
        elogger.enter(f'^^ get_day_intro {bdate} in ({locale}) locale with offset {offset}')
        query = f"SELECT {locale}wde FROM presorted WHERE bday='{bdate}' LIMIT {count} OFFSET {offset}"
        return self.try_fetch(query, Mdb.ALL)

    def get_ids_by_name(self, name):
        elogger.enter(f'^^ get_people {name}')
        query = f"SELECT wdentity, qrank FROM people WHERE tsv @@ to_tsquery('{name}') ORDER BY qrank DESC"
        return self.try_fetch(query, Mdb.ONE)

    def get_universal(self, utypename, wdentities):
        elogger.enter(f'^^ get: {utypename} {wdentities}')
        tuplestr = to_tuple_string(wdentities)
        query = {
            'labels': f"SELECT occu_entity, descr_cache FROM occupations WHERE occu_entity IN {tuplestr}",
            'descriptions': f"SELECT wdentity, descrs FROM people WHERE wdentity IN {tuplestr}",
            'sitelinks': f"SELECT wdentity, links FROM people WHERE wdentity IN {tuplestr}"
        }.get(utypename)
        return self.try_fetch(query, Mdb.ALL)

    def get_photo(self, wdid):
        elogger.enter(f'^^ get_photo {wdid}')
        query = f"SELECT photo FROM people WHERE wdentity='{wdid}'"
        return self.try_fetch(query, Mdb.ONE)

    def get_emojis(self, entities):
        elogger.enter(f'^^ get_emojis {entities}')
        entity_list = to_tuple_string(entities)
        query = 'SELECT t.people_entity, o.emoji ' \
                'FROM tags t INNER JOIN occupations o ' \
                'ON t.occupation_entity = o.occu_entity ' \
                f'WHERE t.people_entity IN  {entity_list} ' \
                'ORDER BY t._id'
        return self.try_fetch(query, Mdb.ALL)

    def get_tags(self, wdentity):
        elogger.enter(f'^^ get_tags {wdentity}')
        query = 'SELECT t.occupation_entity, o.emoji ' \
                'FROM tags t INNER JOIN occupations o ' \
                'ON t.occupation_entity = o.occu_entity ' \
                f"WHERE t.people_entity='{wdentity}' ORDER BY t._id"
        return self.try_fetch(query, Mdb.ALL)

    def get_flags(self, wdentity):
        query = 'SELECT countries.people_entity, flags.emoji_flag FROM flags ' \
                'JOIN countries ON countries.country_entity = flags.country_entity ' \
                f"WHERE countries.people_entity = '{wdentity}'"
        return self.try_fetch(query, Mdb.ALL)

    def get_entities(self, entities):
        elogger.enter(f'^^ get_entities {entities}')
        query = f"SELECT people_entity from tags WHERE people_entity IN {to_tuple_string(entities)}"
        return self.try_fetch(query, Mdb.ALL)

    def set_entities(self, entities):
        elogger.debug(f'set_entitites {entities}')
        query = "INSERT INTO tags (people_entity, occupation_entity)" \
                f" VALUES {str(entities)[1:-1]} ON CONFLICT DO NOTHING"
        return self.try_commit(query)

    def get_user(self, userid):
        elogger.enter(f'^^ get_user {userid}')
        query = f'SELECT settings FROM users WHERE userid={userid}'
        return self.try_fetch(query, Mdb.ONE)

    def set_user(self, userid, settings):
        elogger.debug(f'set_user {userid}')
        query = "INSERT INTO users (userid, status, settings, notitime) " + \
                f"VALUES ({userid}, '1', '{settings}', '08:00')"
        return self.try_commit(query)

    def set_sets(self, userid, settings):
        elogger.debug(f'set_settings {userid}')
        query = f"UPDATE users SET settings='{settings}' WHERE userid={userid}"
        return self.try_commit(query)

    def ident_user(self, userid, regname, regtime, settings):
        elogger.debug(f'ident_user {userid}')
        query = f"UPDATE users SET regname='{regname}', regtime='{regtime}', " \
                f"identity='{settings}' WHERE userid={userid}"
        return self.try_commit(query)

    def get_notication_requiring(self, whattime):
        elogger.enter(f'^^ get notifyee @ {whattime}')
        query = f"SELECT userid FROM users WHERE status=1 AND notitime='{whattime}'"
        return self.try_fetch(query, Mdb.ALL)

    def set_notifications(self, userid, tumbler):
        elogger.debug(f'set_notification {userid} to {tumbler}')
        query = f"UPDATE users SET status={tumbler} WHERE userid={userid}"
        return self.try_commit(query)

    def set_notitime(self, userid, notitime):
        elogger.debug(f'set_notitime {userid} to {notitime}')
        query = f"UPDATE users SET notitime='{notitime}' WHERE userid={userid}"
        return self.try_commit(query)

    def get_notitime(self, userid):
        elogger.enter(f'^^ get_notitime of {userid}')
        query = f"SELECT notitime from users WHERE userid={userid}"
        return self.try_fetch(query, Mdb.ONE)

    def get_allfav(self, userid):
        elogger.enter(f'^^ get_likees {userid}')
        query = f"SELECT wdid FROM facetable WHERE userid={userid} ORDER by bday ASC"
        return self.try_fetch(query, Mdb.ALL)

    def add_to_fav(self, userid, wdid, bday):
        elogger.debug(f'add_to_fav {userid} {wdid} {bday}')
        query = f"INSERT INTO facetable VALUES ({userid}, '{wdid}', '{bday}')"
        return self.try_commit(query)

    def get_bday(self, wdid):
        elogger.debug(f'^^ get_bday {wdid}')
        query = f"SELECT bdate FROM people WHERE wdentity='{wdid}'"
        return self.try_fetch(query, Mdb.ONE)


class Memdb:

    def __init__(self):
        self.connection = None

    async def create_connection(self):
        if not self.connection:
            self.connection = await aiosqlite.connect(":memory:", check_same_thread=False)
            print('[ memdb connection ok ]')

    async def create(self):
        if not self.connection:
            await self.create_connection()

        await self.connection.execute(f"CREATE TABLE memble (userid TEXT UNIQUE, settings TEXT)")
        await self.connection.commit()

    async def settings(self, userid):
        if not self.connection:
            await self.create_connection()

        data = ''
        try:
            cur = await self.connection.execute(f"SELECT settings FROM memble WHERE userid={userid}")
            data = await cur.fetchone()
        except aiosqlite.OperationalError:
            await self.create()

        if data:
            return data[0]
        else:
            data = await maindb.get_user(userid)
            await self._load_settings(userid, data)
            return data

    async def _load_settings(self, userid, data):
        await self.connection.execute(f"INSERT INTO memble VALUES({userid}, '{data}')")
        await self.connection.commit()

    async def update_settings(self, userid, data):
        await self.connection.execute(f"UPDATE memble SET settings='{data}' WHERE userid={userid}")
        await self.connection.commit()

    async def close(self):
        await self.connection.close()


maindb = Mdb()
memdb = Memdb()
