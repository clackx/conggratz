import datetime
import hashlib
import random
import re
import config
from mdb import maindb
from aiogram import Bot, Dispatcher

from apscheduler.schedulers.asyncio import AsyncIOScheduler
scheduler = AsyncIOScheduler()
scheduler.start()
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(apscheduler=scheduler)


def get_wc_thumb(photo, width=800):
    """ generate full wikimedia URL from the filename hash
    https://commons.wikimedia.org/wiki/Commons:FAQ#What_are_the_strangely_named_components_in_file_paths.3F
    code from https://stackoverflow.com/a/64323021/1230965 """
    if photo is None:
        return randpicture('nophoto')
    photo = photo.replace(' ', '_')
    m = hashlib.md5()
    m.update(photo.encode('utf-8'))
    d = m.hexdigest()
    result = f'https://upload.wikimedia.org/wikipedia/commons/thumb/{d[0]}/{d[0:2]}/{photo}/{str(width)}px-{photo}'
    result = result.replace('"', '%22')
    if result[-3:] != 'jpg':
        result += '.jpg'
    return result


def randpicture(rtype):
    if rtype == 'greetz':
        names = ('greetz3.jpg', 'greetz4.jpg', 'greetz1.jpg')
    elif rtype == 'nophoto':
        names = ('nophoto1.jpg', 'nophoto2.jpg', 'nophoto3.jpg')
    link = 'https://conggratz.ru/stati/' + random.choice(names)
    return link


async def search_entity(search_str):
    """ a lot of work taken over by postgres' full-text search """
    search_str = re.sub("[(\[].*?[)\]]", "", search_str)  # remove all in brackets
    search_str = re.sub(r"[-()\]\[\"'#/@;:<>{}`+=~|.!?,$]", " ", search_str)  # remove symbols
    search_str = '&'.join(search_str.strip().split()[:7])
    wdid = await maindb.get_ids_by_name(search_str)
    return wdid


def birthday_from_offset(offset):
    """" returns mm.dd string with day offset relative day today """
    result_stamp = int(datetime.datetime.now().strftime('%s')) + 60 * 60 * 24 * offset
    result = datetime.datetime.fromtimestamp(result_stamp).strftime('%m.%d')
    return result
