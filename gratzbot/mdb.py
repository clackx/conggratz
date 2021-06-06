import sqlite3
import threading
from config import DBNAME
import elogger

lock = threading.Lock()


def to_tuple_string(elements):
    if type(elements) == str:
        return f"('{elements}')"
    else:
        if len(elements) == 1:
            return f"('{elements[0]}')"
        else:
            return str(tuple(map(str, elements)))


class Mdb:
    (ALL, ONE) = (8, 0)

    def __init__(self):
        self.connection = sqlite3.connect(DBNAME, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def try_fetch(self, query, qtype):
        with lock:
            with self.connection:
                try:
                    if qtype == Mdb.ALL:
                        data = self.cursor.execute(query).fetchall()
                    elif qtype == Mdb.ONE:
                        data = self.cursor.execute(query).fetchone()
                        if data:
                            data = data[0]
                except sqlite3.OperationalError as e:
                    elogger.error(f'!! sqlite3 OperationalError :: {str(e)}')
                    return
                elogger.exiter(f'[OK] {len(data) if data else 0} elms {len(str(data))} chrs', data)
            return data

    def try_commit(self, queries):
        with lock:
            with self.connection:
                try:
                    for query in queries:
                        self.cursor.execute(query)
                    self.connection.commit()
                    return True
                except sqlite3.OperationalError as e:
                    elogger.error(f'!! sqlite3 OperationalError :: {str(e)}')
                    return False
                except sqlite3.IntegrityError as e:
                    elogger.warn(f'!! sqlite3 IntegrityError :: {str(e)}')
                    return False

    def get_day_intro(self, bdate, offset, count):
        elogger.enter(f'^^ get_day_intro {bdate}, offset {offset}')
        query = f'SELECT wdentity FROM people WHERE bdate="{bdate}" ORDER BY bklinks DESC LIMIT {offset}, {count}'
        return self.try_fetch(query, Mdb.ALL)

    def get_names(self, bday):
        elogger.enter(f'^^ get_names at {bday}')
        query = f'SELECT links FROM people WHERE bdate="{bday}" LIMIT 0,10'
        return self.try_fetch(query, Mdb.ALL)

    def get_ids_by_name(self, name):
        elogger.enter(f'^^ get_people {name}')
        query = f'SELECT wdentity FROM people WHERE links LIKE "%{name}%"'
        return self.try_fetch(query, Mdb.ALL)

    def get_unequivocal_wdid(self, id_list):
        elogger.enter(f'^^ get_unequivocal_wdid || ids: {len(id_list)}')
        query = f'SELECT wdentity, MAX(bklinks) FROM people WHERE wdentity IN {to_tuple_string(id_list)}'
        return self.try_fetch(query, Mdb.ONE)

    def get_universal(self, utypename, wdentities):
        elogger.enter(f'^^ get: {utypename} {wdentities}')
        tuplestr = to_tuple_string(wdentities)
        query = {
            'labels':       f"SELECT occu_entity, descr_cache FROM occupations WHERE occu_entity IN {tuplestr}",
            'descriptions': f"SELECT wdentity, descr_cache FROM wdentities WHERE wdentity IN {tuplestr}",
            'sitelinks':    f"SELECT wdentity, links FROM people WHERE wdentity IN {tuplestr}"
        }.get(utypename)
        return self.try_fetch(query, Mdb.ALL)

    def set_universal(self, utypename, wdentity, desc_dict):
        elogger.debug(f'set {utypename} {wdentity} :: {desc_dict}')
        desc_dict = desc_dict.replace("'", "''")   # escaping a quote
        queries = {
            'labels': (f"INSERT OR IGNORE INTO occupations VALUES ('{wdentity}', null, null, null) ",
                       f"UPDATE occupations SET descr_cache='{desc_dict}' WHERE occu_entity='{wdentity}'"),
            'descriptions': (f"INSERT OR IGNORE INTO wdentities VALUES ('{wdentity}', null, null) ",
                             f"UPDATE wdentities SET descr_cache='{desc_dict}' WHERE wdentity='{wdentity}'"),
            'sitelinks': (f"UPDATE people SET links='{desc_dict}' WHERE wdentity='{wdentity}'",)
        }.get(utypename)
        return self.try_commit(queries)

    def get_photo(self, wdid):
        elogger.enter(f'^^ get_photo {wdid}')
        query = f'SELECT photo FROM people WHERE wdentity="{wdid}"'
        return self.try_fetch(query, Mdb.ONE)

    def get_emojis(self, entities):
        elogger.enter(f'^^ get_emojis {entities}')
        entity_list = to_tuple_string(entities)
        query = 'SELECT t.people_entity, o.emoji ' \
                'FROM tags t INNER JOIN occupations o ' \
                'ON t.occupation_entity = o.occu_entity ' \
                f'WHERE t.people_entity IN  {entity_list} ' \
                'ORDER BY t.ROWID'
        return self.try_fetch(query, Mdb.ALL)

    def get_tags(self, wdentity):
        elogger.enter(f'^^ get_tags {wdentity}')
        query = 'SELECT t.occupation_entity, o.emoji ' \
                'FROM tags t INNER JOIN occupations o ' \
                'ON t.occupation_entity = o.occu_entity ' \
                f'WHERE t.people_entity="{wdentity}" ORDER BY t.ROWID'
        return self.try_fetch(query, Mdb.ALL)

    def get_entities(self, entities):
        elogger.enter(f'^^ get_entities {entities}')
        query = f"SELECT people_entity from tags WHERE people_entity IN {to_tuple_string(entities)}"
        return self.try_fetch(query, Mdb.ALL)

    def set_entities(self, entities):
        elogger.debug(f'set_entitites {entities}')
        query = (f"INSERT OR IGNORE INTO tags (people_entity, occupation_entity) VALUES {str(entities)[1:-1]}", )
        return self.try_commit(query)

    def get_user(self, userid):
        elogger.enter(f'^^ get_user {userid}')
        query = f'SELECT settings FROM users WHERE userid={userid}'
        return self.try_fetch(query, Mdb.ONE)

    def set_user(self, userid, settings):
        elogger.debug(f'set_user {userid}')
        queries = (f"INSERT OR IGNORE INTO users VALUES ({userid}, '1', '{settings}', '')",
                   f"UPDATE users SET settings='{settings}' WHERE userid={userid}")
        return self.try_commit(queries)

    def ident_user(self, userid, settings):
        elogger.debug(f'ident_user {userid}')
        queries = (f"UPDATE users SET identity='{settings}' WHERE userid={userid}",)
        return self.try_commit(queries)

    def get_notication_requiring(self):
        elogger.enter('get noti')
        query = "SELECT userid FROM users WHERE status=1"
        return self.try_fetch(query, Mdb.ALL)

    def set_notifications(self, userid, tumbler):
        elogger.debug(f'set_noti {userid} {tumbler}')
        query = (f"UPDATE users SET status={tumbler} WHERE userid={userid}", )
        return self.try_commit(query)

    def get_allfav(self, userid):
        elogger.enter(f'^^ get_likees {userid}')
        query = f"SELECT wdid FROM facetable WHERE userid={userid} ORDER BY ROWID"
        return self.try_fetch(query, Mdb.ALL)

    def add_to_fav(self, userid, wdid):
        elogger.debug(f'add to fav {userid} {wdid}')
        query = (f"INSERT INTO facetable VALUES ({userid}, '{wdid}')", )
        return self.try_commit(query)


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
            maindb = Mdb()
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
