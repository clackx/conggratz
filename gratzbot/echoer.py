import datetime
from config import DBUSER, DBNAME
import psycopg2


class Evdb:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(user=DBUSER, database=DBNAME,
                                               host="127.0.0.1", port="5432")
            self.cursor = self.connection.cursor()
            print('[ evdb connection ok ]')
        except (Exception, psycopg2.Error) as error:
            print('connection failed with', error)

    def add_to_events(self, tstamp, thuman, evt, usr, txt):
        query = f"INSERT INTO events VALUES (%s, %s, %s, %s, %s)"
        values = (tstamp, thuman, evt, usr, txt)
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
        except (Exception, psycopg2.Error) as error:
            print('insertion failed with', error)


def echo(message):
    tstamp = int(datetime.datetime.now().strftime('%s'))
    thuman = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
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

    evdb.add_to_events(tstamp, thuman, evt, usr, txt)


evdb = Evdb()
