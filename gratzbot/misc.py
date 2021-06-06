import telebot
import datetime
import hashlib
import random
import re
import config
import mdb

maindb = mdb.Mdb()
bot = telebot.TeleBot(config.API_TOKEN)


def get_wc_thumb(photo, width=420):
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


def search_entity(search_str):
    """ finds one most relevant result of name search
    if request of *search_str* returns nothing, it splits into words,
    then it's queries every word and finds entity in every queries
    result list of entities goes to *get_unequivocal_wdid* """
    ids = sum(maindb.get_ids_by_name(search_str), ())
    if ids:
        if len(ids) == 1:
            wdid = ids[0]
        else:
            wdid = maindb.get_unequivocal_wdid(ids)
    else:
        search_str = re.sub("[(\[].*?[)\]]", "", search_str)  # remove all in brackets
        search_str = re.sub(r"[-()\]\[\"'#/@;:<>{}`+=~|.!?,$]", " ", search_str)  # remove symbols
        prev_list = []
        for word in search_str.split():
            ids = sum(maindb.get_ids_by_name(word.capitalize()), ())
            if len(ids) == 0:
                continue
            if not prev_list:  # first run
                prev_list = ids
            else:
                res_list = []
                for _id in ids:
                    if _id in prev_list:
                        res_list.append(_id)
                prev_list = res_list

        if prev_list:
            wdid = maindb.get_unequivocal_wdid(prev_list)
        else:
            wdid = None

    return wdid


def birthday_from_offset(offset):
    """" returns mm.dd string with day offset relative day today """
    result_stamp = int(datetime.datetime.now().strftime('%s')) + 60 * 60 * 24 * offset
    result = datetime.datetime.fromtimestamp(result_stamp).strftime('%m.%d')
    return result


def parseday(message):
    """ parses dd.mm or mm.dd string to return in mm.dd format """
    try:
        if '.' in message:
            tstamp = datetime.datetime.strptime(message, '%d.%m')
        if '-' in message:
            tstamp = datetime.datetime.strptime(message, '%m-%d')
    except ValueError:
        return False
    return tstamp.strftime('%m.%d')
