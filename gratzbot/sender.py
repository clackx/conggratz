import telebot
import requests
import datetime
import getter
from misc import bot, randpicture
import misc
import user
import elogger
from messages import get_translation


def send_gratz_brief(chat_id, bday, offset=0):
    """ sends daily briefing for *bday*, starting from *offset*
    all the time *offset* is 0, except calling from send_greets_shift """
    elogger.info(f'<< {chat_id} send_greetz {bday} offset {offset}')
    text, keyboard = getter.get_day_plus(chat_id, bday, offset)
    message_id = send_message(chat_id, text, markup=keyboard)
    user.update_param(chat_id, 'session', {'message_id': message_id, 'bday': bday, 'offset': offset})
    elogger.exiter(f'[OK]  [OK]  [OK]', True)


def send_gratz_shift(chat_id, direction):
    """ deletes the previous brief and sends a new one with calculated offset """
    prev_message_id, bday, offset, is_rested = getter.get_shift_params(chat_id, direction)
    if not is_rested:
        delete_message(chat_id, prev_message_id)
        send_gratz_brief(chat_id, bday, offset)


def send_info(chat_id, incoming_message):
    """" sends personality info message in three steps:
    because getter.get_info takes several seconds to request page,
    first it's sends four-dots message and saves this message_id,
    then if wdid is found, message changes to just photolink;
    finally, appends text info from wikipedia in required locale
    After all, wikidata is requested for all notable properties """
    elogger.info(f'<< {chat_id} send_info {incoming_message}')
    locale = user.load_param(chat_id, 'locale').get('primary')
    starttime = datetime.datetime.now()
    message_id = send_message(chat_id, '....')
    wdid = misc.search_entity(incoming_message)
    if wdid is None:
        edit_message(chat_id, message_id, get_translation('not found', locale))
    else:
        link = '<a href="{}">&#8205;</a>'.format(getter.get_photo_link(wdid))
        edit_message(chat_id, message_id, '....\n' + link)

        text, keyboard = getter.get_info(wdid, locale)
        edit_message(chat_id, message_id, text + ' ' + link, markup=keyboard)

        # coming soon
        # props, props_dict = getter.find_properties(wdid, locale)
        # for prop in props_dict:
        #     text = f'{props_dict[prop][0].capitalize()}:  ({prop})\n'
        #     for value in props_dict[prop][1:]:
        #         text += f'• {value} \n'
        #     # придётся избавиться от этой красоты
        #     send(chat_id, text)
    endtime = datetime.datetime.now()
    elogger.exiter(f'[OK] {chat_id} send_info {wdid}',
                   'Spend {}s to request'.format((endtime - starttime).total_seconds()))


def save_liked(chat_id, wdid):
    """ informs if a fav entity has been added to db or already exist """
    elogger.info(f'<< {chat_id} like {wdid}')
    locale = user.load_param(chat_id, 'locale').get('primary')
    if user.add_to_fav(chat_id, wdid):
        text = get_translation('added to fav', locale)
    else:
        text = get_translation('already in fav', locale)
    send_message(chat_id, text)
    elogger.exiter('[OK]', text)


def send_likees(chat_id):
    """ shows your favlist """
    elogger.info(f'<< {chat_id} likees')
    text = getter.get_all_fav(chat_id)
    send_message(chat_id, text)
    elogger.exiter('[OK]', text)


def send_anotherdaytext(chat_id):
    """ just sends localized text """
    locale = user.load_param(chat_id, 'locale').get('primary')
    res_str = get_translation('edf', locale) + ' дд.мм / mm-dd'
    send_message(chat_id, res_str)


def parseday(chat_id, message):
    """ calls send_greetz_brief if parsing message to bday is correct """
    bday = misc.parseday(message)
    if bday:
        send_gratz_brief(chat_id, bday)
    else:
        send_message(chat_id, '8===Э')


def greetz(chat_id):
    locale = user.load_param(chat_id, 'locale').get('primary')
    text = get_translation('greetz', locale)
    link = '<a href="{}">&#8205;</a>'.format(randpicture('greetz'))
    send_message(chat_id, f'{text} {link}')


def send_message(chat_id, message, markup=''):
    message_id = ''
    try:
        message_id = bot.send_message(chat_id, message, reply_markup=markup,
                                      parse_mode='html', disable_notification=True).message_id
    except telebot.apihelper.ApiTelegramException as e:
        elogger.warn(f'! TELE API: {e}')
    except requests.exceptions.ConnectionError as e:
        elogger.warn(f'! REQUESTS: {e}')
    return message_id


def edit_message(chat_id, message_id, text, markup=''):
    try:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text,
                              parse_mode="html", reply_markup=markup)
    except telebot.apihelper.ApiTelegramException as e:
        elogger.warn(f'! TELE API: {e}')
    except requests.exceptions.ConnectionError as e:
        elogger.warn(f'! REQUESTS: {e}')


def delete_message(chat_id, message_id):
    try:
        bot.delete_message(chat_id=chat_id, message_id=message_id)
    except telebot.apihelper.ApiTelegramException as e:
        elogger.warn(f'! TELE API: {e}')
    except requests.exceptions.ConnectionError as e:
        elogger.warn(f'! REQUESTS: {e}')
