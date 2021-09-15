import telebot
import requests
import datetime
from time import sleep
import getter
from misc import bot, randpicture, search_entity
from config import admin_id
import user
import elogger
import settings
from messages import get_translation


def send_gratz_brief(chat_id, bday, offset=0, noedit=False):
    """ sends daily briefing for *bday*, starting from *offset*
    all the time *offset* is 0, except calling from send_greets_shift """
    elogger.info(f'<< {chat_id} send_greetz {bday} offset {offset}')
    text, markup, kbtype = getter.get_day_plus(chat_id, bday, offset)
    smartsend(chat_id, text, markup, kbtype, noedit)
    user.update_param(chat_id, 'session', {'bday': bday, 'offset': offset})
    elogger.exiter(f'[OK]  [OK]  [OK]', True)


def send_gratz_shift(chat_id, direction, noedit=False):
    """ deletes the previous brief and sends a new one with calculated offset """
    bday, offset, is_rested, kbtype = getter.get_shift_params(chat_id, direction)
    if not is_rested:
        send_gratz_brief(chat_id, bday, offset, noedit)


def incoming(chat_id, incoming_message):
    state = user.load_param(chat_id, 'session').get('state')
    if state == 4:
        elogger.preinfo(f':: {chat_id} RVW {incoming_message}')
        send_message(chat_id, message='GREAT THANX!')
        user.update_param(chat_id, 'session', {'state': 0})
    else:
        send_info(chat_id, incoming_message)


def send_info(chat_id, incoming_message):
    """" sends personality info message in three steps:
    because getter.get_info takes several seconds to request page,
    first it's sends four-dots message and saves this message_id,
    then if wdid is found, message changes to just photolink;
    finally, appends text info from wikipedia in required locale
    After all, wikidata is requested for all notable properties """
    elogger.info(f'<< {chat_id} send_info {incoming_message}')
    locale = user.load_param(chat_id, 'locale').get('primary')
    altale = user.load_param(chat_id, 'locale').get('altern', 'en')
    starttime = datetime.datetime.now()
    message_id = send_message(chat_id, '....')
    if incoming_message[:1] == 'Q':
        wdid = incoming_message
    else:
        wdid = search_entity(incoming_message)
    stata = ''
    if wdid is None:
        edit_message(chat_id, message_id, get_translation('not found', locale))
    else:
        link = '<a href="{}">&#8205;</a>'.format(getter.get_photo_link(wdid))
        edit_message(chat_id, message_id, '....\n' + link)

        text, keyboard = getter.get_info(wdid, locale, altale)
        endtime = datetime.datetime.now()
        stata = '<code>Spend {}s to request</code>'.format((endtime - starttime).total_seconds())
        s = '\n\n' + stata if chat_id == admin_id else ''
        edit_message(chat_id, message_id, text + s + ' ' + link, markup=keyboard)

    elogger.exiter(f'[OK] {chat_id} send_info {wdid}', result=stata)


def send_more(chat_id, wdid, query_id):
    locale = user.load_param(chat_id, 'locale').get('primary')
    altale = user.load_param(chat_id, 'locale').get('altern', 'en')
    props_dict = getter.find_properties(wdid, locale, altale)
    for prop in props_dict.keys():
        text = f'{props_dict[prop][0].capitalize()}:\n'
        if chat_id == admin_id: text = text[:-1] + f' ({prop})\n'
        for value in props_dict[prop][1:]:
            text += f'• {value} \n'
        send_message(chat_id, text)
    if not props_dict:
        send_message(chat_id, 'N/A')
    answer_callback_query(query_id)


def save_liked(chat_id, wdid, query_id):
    """ informs if a fav entity has been added to db or already exist """
    elogger.info(f'<< {chat_id} like {wdid}')
    locale = user.load_param(chat_id, 'locale').get('primary')
    if user.add_to_fav(chat_id, wdid):
        text = get_translation('added to fav', locale)
    else:
        text = get_translation('already in fav', locale)
    answer_callback_query(query_id)
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
    """ parses dd.mm or mm.dd string to return in mm.dd format then
    calls send_greetz_brief if parsing message to bday is correct """
    tstamp = ''
    try:
        if '.' in message:
            tstamp = datetime.datetime.strptime(message, '%d.%m')
        if '-' in message:
            tstamp = datetime.datetime.strptime(message, '%m-%d')
    except ValueError:
        pass
    bday = tstamp.strftime('%m.%d')
    if bday:
        send_gratz_brief(chat_id, bday)
    else:
        send_message(chat_id, '8===Э')


def helps(chat_id):
    locale = user.load_param(chat_id, 'locale').get('primary')
    if locale != 'ru':
        locale = 'en'
    send_message(chat_id, get_translation('prehelp', locale))
    settings.settings(chat_id, 911, 0)


def smartsend(chat_id, text, markup, kbtype, noedit=False):
    s = user.load_param(chat_id, 'session')
    prev_sets_mess_id = s.get('sets_mess_id')
    prev_message_id = s.get('message_id')
    if kbtype == 'regular' or prev_message_id != prev_sets_mess_id or noedit:
        delete_message(chat_id, prev_sets_mess_id)
        message_id = send_message(chat_id, text, markup=markup)
    else:
        is_successful = edit_message(chat_id, prev_sets_mess_id, text, markup=markup)
        if not is_successful:
            message_id = send_message(chat_id, text, markup=markup)
        else:
            return
    user.update_param(chat_id, 'session', {'sets_mess_id': message_id})


def send_message(chat_id, message, markup=''):
    message_id = ''
    try:
        message_id = bot.send_message(chat_id, message, reply_markup=markup,
                                      parse_mode='html', disable_notification=True).message_id

    except telebot.apihelper.ApiTelegramException as e:
        err_num = e.result_json.get('error_code', 0)
        err_dcr = e.result_json.get('description', '')
        elogger.warn(f'{chat_id} ! TelegrAPI error {err_num} :: {err_dcr}')
        if err_num == 429:
            retry_after = 1
            if err_dcr[:17] == 'Too Many Requests':
                err_param = e.result_json.get('parameters', '')
                if err_param:
                    retry_after = err_param.get('retry_after', 2)
            sleep(retry_after)
            send_message(chat_id, message, markup)
        elif (err_num == 400 and err_dcr == 'Bad Request: chat not found') or \
             (err_num == 403 and err_dcr == 'Forbidden: bot was blocked by the user'):
            elogger.preinfo(f'-- {chat_id} SRV user disabled')
            user.set_notifications(chat_id, 0)
        else:
            print('Error', err_num, err_dcr)
    except requests.exceptions.ConnectionError as e:
        elogger.warn(f'{chat_id} ! REQUESTS: {e}')
    if message_id:
        user.update_param(chat_id, 'session', {'message_id': message_id})
    return message_id


def edit_message(chat_id, message_id, text, markup=''):
    is_successful = False
    try:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text,
                              parse_mode="html", reply_markup=markup)
        is_successful = True
    except telebot.apihelper.ApiTelegramException as e:
        err_num = e.result_json.get('error_code', 0)
        err_dcr = e.result_json.get('description', '')
        if err_dcr[85: 105] == 'are exactly the same':
            err_dcr = err_dcr[:38] + 'every day' + err_dcr[88: 105]
        elogger.warn(f'{chat_id} ! TelegrAPI error {err_num} :: {err_dcr}')
    except requests.exceptions.ConnectionError as e:
        elogger.warn(f'{chat_id} ! REQUESTS: {e}')
    return is_successful


def delete_message(chat_id, message_id):
    if message_id:
        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except telebot.apihelper.ApiTelegramException as e:
            err_num = e.result_json.get('error_code', 0)
            err_dcr = e.result_json.get('description', '')
            elogger.warn(f'{chat_id} ! TelegrAPI error {err_num} :: {err_dcr}')
        except requests.exceptions.ConnectionError as e:
            elogger.warn(f'{chat_id} ! REQUESTS: {e}')


def answer_callback_query(query_id):
    if query_id:
        try:
            bot.answer_callback_query(query_id)
        except telebot.apihelper.ApiTelegramException as e:
            err_num = e.result_json.get('error_code', 0)
            err_dcr = e.result_json.get('description', '')
            elogger.warn(f'{query_id} ! TelegrAPI error {err_num} :: {err_dcr}')
        except requests.exceptions.ConnectionError as e:
            elogger.warn(f'{query_id} ! REQUESTS: {e}')
