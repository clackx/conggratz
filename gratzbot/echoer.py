import datetime
import sqlite3
from config import abspth

connection = sqlite3.connect(abspth+'/logvrotate.sqlite', check_same_thread=False)
cursor = connection.cursor()


def echo(message):
    timenow = int(datetime.datetime.now().strftime('%s'))
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

    try:
        connection.execute(f'INSERT INTO events VALUES ({timenow}, "{evt}", "{usr}", "{txt}")')
        connection.commit()
    except sqlite3.ProgrammingError as e:
        print(e)
    except sqlite3.OperationalError as e:
        print(e)


