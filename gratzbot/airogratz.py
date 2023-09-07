import os
import sys
import asyncio
from datetime import datetime
from signal import SIGINT, SIGTERM
from aiohttp import web, ClientSession
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

import config
import handler
from periodic import notify_notifyee, run_async_notifier
from misc import bot, dp, birthday_from_offset, scheduler
from config import WEBHOOK_URL, WEBHOOK_URL_PATH, WEBHOOK_HOST, WEBHOOK_PORT


async def start_longpolling():
    dp.startup.register(delete_webhook)
    await dp.start_polling(bot, skip_updates=False)

async def set_webhook(bot):
    await bot.set_webhook(WEBHOOK_URL + WEBHOOK_URL_PATH)

async def delete_webhook(bot):
    await bot.delete_webhook()

async def start_webhook():
    dp.include_router(handler.router)
    dp.startup.register(set_webhook)
    dp.shutdown.register(delete_webhook)

    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_requests_handler.register(app, path=WEBHOOK_URL_PATH)
    setup_application(app, dp, bot=bot)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, WEBHOOK_HOST, WEBHOOK_PORT)
    await site.start()

    while True:
        await asyncio.sleep(42)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    scheduler.add_job(notify_notifyee, "interval", minutes=1)

    if len(sys.argv) > 1 and (sys.argv[1] == '--polling'):
        print('conggratzbot <><> polling <><> mode started')
        main_task = asyncio.ensure_future(start_longpolling())
        loop.add_signal_handler(SIGINT, main_task.cancel)
        loop.add_signal_handler(SIGTERM, main_task.cancel)
    else:
        print('conggratz aiobot V^V^ webhook V^V^ mode started')
        main_task=start_webhook()

    try:
        loop.run_until_complete(main_task)
    except KeyboardInterrupt:
        print("Nicely shutting down ...")
        os._exit(0)
    finally:
        loop.close()
        os._exit(0)
