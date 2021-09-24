import asyncio
import time
import settings
import sender
from config import admin_id
import elogger
import misc
import getter
from mdb import maindb
from echoer import evdb

elogger.enter('))) NOSERVER (((')

userid = admin_id
# userid = 1931265886
userid = 1146011385


async def main():
    await evdb.connect()
    await maindb.connect()

    # print brief to console
    text, _tmp1, _tmp2 = await getter.get_day_plus(userid, '09.09', 0)
    print(text)

    # set EN locale and show 3 first pages of help
    await settings.settings(userid, 2, 'EN')
    await sender.helps(userid)
    time.sleep(3)
    await settings.settings(userid, 911)
    time.sleep(3)
    await settings.settings(userid, 911)

    # send info about person
    await sender.send_info(userid, 'Douglas Adams')
    # and extended info
    await sender.send_more(userid, 'Q42', 0)
    # await sender.send_info(userid, 'Байнам, Эндрю')
    # await sender.send_more(userid, 'Q314822', 0)

    # set FR locale
    await settings.settings(userid, 2, 'FR')
    # ALT locale set to ES
    await settings.settings(userid, 2, '*ES')
    # show settings
    await settings.settings(userid, 0)
    time.sleep(3)

    # show info with new language settings
    await sender.send_info(userid, '彭帅')
    await sender.send_more(userid, 'Q229087', 0)
    # await sender.send_info(userid, 'Aleksey Tolstoy')
    # await sender.send_more(userid, 'Q192279', 0)

    # brief: show persons born at Sept, 11
    await sender.send_gratz_brief(userid, '11.11')
    # await sender.send_gratz_brief(userid, '08.09')

    # navigate forward
    await sender.send_gratz_shift(userid, +1)
    time.sleep(2)
    await sender.send_gratz_shift(userid, +1)
    time.sleep(2)
    await sender.send_gratz_shift(userid, +1)
    time.sleep(2)
    # and back
    # await sender.send_gratz_shift(userid, -1)
    # await sender.send_gratz_shift(userid, -1)
    # await sender.send_gratz_shift(userid, -1)
    # await sender.send_gratz_shift(userid, -1)

    # SETTINGS

    # change ui params
    await settings.settings(userid, 1, '')
    # Number of keys (must be even) ??
    await settings.settings(userid, 1, '7')
    # Number of entries (can't be less than keys (so it'll be fixed))
    await settings.settings(userid, 1, '3')
    # Value of step (must be even and can't be more than keys)
    await settings.settings(userid, 1, '5')

    # continue navigate back and forth
    await sender.send_gratz_shift(userid, -1)
    time.sleep(2)
    await sender.send_gratz_shift(userid, 1)

    await settings.settings(userid, 1, 'regular')
    time.sleep(2)
    await sender.send_gratz_shift(userid, -1)
    time.sleep(2)
    await sender.send_gratz_shift(userid, -1)
    time.sleep(2)

    # show your settings
    await settings.settings(userid, 0)
    time.sleep(3)

    await settings.settings(userid, 1, 'inline')
    time.sleep(2)
    # and continue navigate
    await sender.send_gratz_shift(userid, -1)
    time.sleep(2)
    await sender.send_gratz_shift(userid, -1)

    loop.stop()
    elogger.exiter(')))', True)


loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)
asyncio.run(main())
