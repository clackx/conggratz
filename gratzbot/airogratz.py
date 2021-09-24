import aiogram
import ssl
import config
from misc import bot, dp
import handler


async def on_startup(dp):
    await bot.set_webhook(config.WEBHOOK_URL)


async def on_shutdown(dp):
    await bot.delete_webhook()


if __name__ == '__main__':
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
