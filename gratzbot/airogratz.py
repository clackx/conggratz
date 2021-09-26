import aiogram
import asyncio
import datetime
import ssl
import config
from misc import bot, dp, birthday_from_offset
import handler
from mdb import maindb
from sender import send_gratz_brief


async def on_startup(dp):
    await bot.set_webhook(config.WEBHOOK_URL)


async def on_shutdown(dp):
    await bot.delete_webhook()


async def periodic():
    prev = -1
    while True:
        await asyncio.sleep(20)
        now = datetime.datetime.utcnow().strftime("%H:%M")
        if now != prev:
            prev = now
            users = [d[0] for d in await maindb.get_notication_requiring(now)]
            for userid in users:
                print(f'{now} UTC :: briefing user {userid}')
                await send_gratz_brief(userid, birthday_from_offset(0))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(periodic())
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(config.WEBHOOK_SSL_CERT, config.WEBHOOK_SSL_PRIV)
    aiogram.executor.start_webhook(
        dispatcher=dp,
        webhook_path=config.WEBHOOK_URL_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=False,
        host=config.WEBHOOK_LISTEN,
        port=config.WEBHOOK_PORT,
        ssl_context=context
    )
