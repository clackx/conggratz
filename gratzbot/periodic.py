from datetime import datetime
import handler  # to avoid circular import
from asyncio import run, sleep
from sender import send_gratz_brief
from mdb import maindb


async def notify_notifyee():
    now = datetime.utcnow().strftime("%H:%M")
    users = [d[0] for d in await maindb.get_notication_requiring(now)]
    for userid in users:
        print(f'{now} UTC :: briefing user {userid}')
        await send_gratz_brief(userid, birthday_from_offset(0))


def run_async_notifier():
    run(periodic())


async def periodic():
    prev = -1
    while True:
        now = datetime.utcnow().strftime("%H:%M")
        if now != prev:
            prev = now
            await notify_notifyee()

        await sleep(20)


if __name__ == '__main__':
    try:
        run(periodic())
    except KeyboardInterrupt as err:
        pass