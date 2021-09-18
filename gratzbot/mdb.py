import sqlite3
import threading
from config import DBUSER, DBNAME
import elogger
import psycopg2
from psycopg2 import Error

lock = threading.Lock()


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
        try:
            self.connection = psycopg2.connect(user=DBUSER, database=DBNAME,
                                               host="127.0.0.1", port="5432")
            self.cursor = self.connection.cursor()
        except (Exception, Error) as error:
            elogger.error(f'!! postgres error :: {str(error)}')
        finally:
            if self.connection:
                elogger.preinfo('[] PostgreSQL 8:==э connected')

    def try_fetch(self, query, qtype):
        with lock:
            with self.connection:
                try:
                    if qtype == Mdb.ALL:
                        self.cursor.execute(query)
                        data = self.cursor.fetchall()
                    elif qtype == Mdb.ONE:
                        self.cursor.execute(query)
                        data = self.cursor.fetchone()
                        if data:
                            data = data[0]
                except sqlite3.OperationalError as e:
                    elogger.error(f'!! sqlite3 OperationalError :: {str(e)}')
                    return
                except (Exception, Error) as error:
                    elogger.error(f'!! postgres error :: {str(error)}')
                    return
                elogger.exiter(f'[OK] {len(data) if data else 0} elms {len(str(data))} chrs', data)
            return data

    def try_commit(self, query):
        with lock:
            with self.connection:
                try:
                    self.cursor.execute(query)
                    self.connection.commit()
                    return True
                except sqlite3.OperationalError as e:
                    elogger.error(f'!! sqlite3 OperationalError :: {str(e)}')
                    return False
                except sqlite3.IntegrityError as e:
                    elogger.error(f'!! sqlite3 IntegrityError :: {str(e)}')
                    return False
                except (Exception, Error) as error:
                    elogger.error(f'!! postgres error :: {str(error)}')
                    return False

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
            'labels':       f"SELECT occu_entity, descr_cache FROM occupations WHERE occu_entity IN {tuplestr}",
            'descriptions': f"SELECT wdentity, descrs FROM people WHERE wdentity IN {tuplestr}",
            'sitelinks':    f"SELECT wdentity, links FROM people WHERE wdentity IN {tuplestr}"
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
        query = f"INSERT INTO tags (people_entity, occupation_entity) VALUES {str(entities)[1:-1]}"
        return self.try_commit(query)

    def get_user(self, userid):
        elogger.enter(f'^^ get_user {userid}')
        query = f'SELECT settings FROM users WHERE userid={userid}'
        return self.try_fetch(query, Mdb.ONE)

    def set_user(self, userid, settings):
        elogger.debug(f'set_user {userid}')
        query = f"INSERT INTO users (userid, status, settings) VALUES ({userid}, '1', '{settings}')"
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

    def get_notication_requiring(self):
        elogger.enter('get noti')
        query = "SELECT userid FROM users WHERE status=1"
        return self.try_fetch(query, Mdb.ALL)

    def set_notifications(self, userid, tumbler):
        elogger.debug(f'set_noti {userid} {tumbler}')
        query = f"UPDATE users SET status={tumbler} WHERE userid={userid}"
        return self.try_commit(query)

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
        self.connection = sqlite3.connect(":memory:", check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"CREATE TABLE memble (userid TEXT UNIQUE, settings TEXT)")

    def settings(self, userid):
        data = self.cursor.execute(f"SELECT settings FROM memble WHERE userid='{userid}'").fetchone()
        if data:
            return data[0]
        else:
            data = maindb.get_user(userid)
            self._load_settings(userid, data)
            return data

    def _load_settings(self, userid, data):
        self.cursor.execute(f"INSERT INTO memble VALUES('{userid}', '{data}')")
        self.connection.commit()

    def update_settings(self, userid, data):
        self.cursor.execute(f"UPDATE memble SET settings='{data}' WHERE userid='{userid}'")
        self.connection.commit()

    def close(self):
        self.connection.close()

    def what(self):
        data = self.cursor.execute(f"SELECT * from memble").fetchall()
        return data

    def reload(self):
        self.cursor.execute(f"DELETE from memble")
        self.connection.commit()


maindb = Mdb()
memdb = Memdb()
