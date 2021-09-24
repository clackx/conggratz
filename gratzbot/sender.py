import aiogram
import datetime
from time import sleep
import getter
from misc import bot, search_entity
from config import admin_id
import user
import elogger
import settings
from messages import get_translation


async def send_gratz_brief(user_id, bday, offset=0, noedit=False):
    """ sends daily briefing for *bday*, starting from *offset*
    all the time *offset* is 0, except calling from send_greets_shift """
    elogger.info(f'<< {user_id} send_greetz {bday} offset {offset}')
    text, markup, kbtype = await getter.get_day_plus(user_id, bday, offset)
    await smartsend(user_id, text, markup, kbtype, noedit)
    await user.update_param(user_id, 'session', {'bday': bday, 'offset': offset})
    elogger.exiter(f'[OK]  [OK]  [OK]', True)


async def send_gratz_shift(user_id, direction, noedit=False):
    """ deletes the previous brief and sends a new one with calculated offset """
    bday, offset, is_rested, kbtype = await getter.get_shift_params(user_id, direction)
    if not is_rested:
        await send_gratz_brief(user_id, bday, offset, noedit)


async def incoming(user_id, incoming_message):
    s = await user.load_param(user_id, 'session')
    state = s.get('state')
    if state == 4:
        await elogger.preinfo(f':: {user_id} RVW {incoming_message}')
        await send_message(user_id, message='GREAT THANX!')
        await user.update_param(user_id, 'session', {'state': 0})
    else:
        await send_info(user_id, incoming_message)


async def send_info(user_id, incoming_message):
    """" sends personality info message in three steps:
    because getter.get_info takes several seconds to request page,
    first it's sends four-dots message and saves this message_id,
    then if wdid is found, message changes to just photolink;
    finally, appends text info from wikipedia in required locale
    After all, wikidata is requested for all notable properties """
    elogger.info(f'<< {user_id} send_info {incoming_message}')
    lcl = await user.load_param(user_id, 'locale')
    locale = lcl.get('primary')
    altale = lcl.get('altern', 'en')
    starttime = datetime.datetime.now()
    message_id = await send_message(user_id, '....')
    if incoming_message[:1] == 'Q':
        wdid = incoming_message
    else:
        wdid = await search_entity(incoming_message)
    stata = ''
    if wdid is None:
        await edit_message(user_id, message_id, get_translation('not found', locale))
    else:
        phlink = await getter.get_photo_link(wdid)
        link = f'<a href="{phlink}">&#8205;</a>'
        await edit_message(user_id, message_id, '....\n' + link)

        text, keyboard = await getter.get_info(wdid, locale, altale)
        endtime = datetime.datetime.now()
        stata = '<code>Spend {}s to request</code>'.format((endtime - starttime).total_seconds())
        s = '\n\n' + stata if user_id == admin_id else ''
        await edit_message(user_id, message_id, text + s + ' ' + link, markup=keyboard)

    elogger.exiter(f'[OK] {user_id} send_info {wdid}', result=stata)


async def send_more(user_id, wdid, query_id):
    lcl = await user.load_param(user_id, 'locale')
    locale = lcl.get('primary')
    altale = lcl.get('altern', 'en')
    props_dict = await getter.find_properties(wdid, locale, altale)
    for prop in props_dict.keys():
        text = f'{props_dict[prop][0].capitalize()}:\n'
        if user_id == admin_id: text = text[:-1] + f' ({prop})\n'
        for value in props_dict[prop][1:]:
            text += f'• {value} \n'
        await send_message(user_id, text)
    if not props_dict:
        await send_message(user_id, 'N/A')
    await answer_callback_query(query_id)


async def save_liked(user_id, wdid, query_id):
    """ informs if a fav entity has been added to db or already exist """
    elogger.info(f'<< {user_id} like {wdid}')
    lcl = await user.load_param(user_id, 'locale')
    locale = lcl.get('primary')
    if await user.add_to_fav(user_id, wdid):
        text = get_translation('added to fav', locale)
    else:
        text = get_translation('already in fav', locale)
    await answer_callback_query(query_id)
    await send_message(user_id, text)
    elogger.exiter('[OK]', text)


async def send_likees(user_id):
    """ shows your favlist """
    elogger.info(f'<< {user_id} likees')
    text = await getter.get_all_fav(user_id)
    await send_message(user_id, text)
    elogger.exiter('[OK]', text)


async def send_anotherdaytext(user_id):
    """ just sends localized text """
    lcl = await user.load_param(user_id, 'locale')
    locale = lcl.get('primary')
    res_str = get_translation('edf', locale) + ' дд.мм / mm-dd'
    await send_message(user_id, res_str)


async def parseday(user_id, message):
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
        await send_gratz_brief(user_id, bday)
    else:
        await send_message(user_id, '8===Э')


async def helps(user_id):
    lcl = await user.load_param(user_id, 'locale')
    locale = lcl.get('primary')
    if locale != 'ru':
        locale = 'en'
    await send_message(user_id, get_translation('prehelp', locale))
    await settings.settings(user_id, 911, 0)


async def smartsend(user_id, text, markup, kbtype, noedit=False):
    s = await user.load_param(user_id, 'session')
    prev_sets_mess_id = s.get('sets_mess_id')
    prev_message_id = s.get('message_id')
    if kbtype == 'regular' or prev_message_id != prev_sets_mess_id or noedit:
        await delete_message(user_id, prev_sets_mess_id)
        message_id = await send_message(user_id, text, markup=markup)
    else:
        is_successful = await edit_message(user_id, prev_sets_mess_id, text, markup=markup)
        if not is_successful:
            message_id = await send_message(user_id, text, markup=markup)
        else:
            return
    await user.update_param(user_id, 'session', {'sets_mess_id': message_id})


async def send_message(user_id, message, markup=''):
    message_id = ''
    try:
        message_obj = await bot.send_message(chat_id=user_id, text=message, reply_markup=markup,
                                             parse_mode='html', disable_notification=True)
        message_id = message_obj.message_id
    except aiogram.exceptions.ChatNotFound as err:
        await elogger.warn(f'{user_id} ! send_message ChatNotFound exception :: {err}')
        await elogger.preinfo(f'-- {user_id} SRV user disabled')
        await user.set_notifications(user_id, 0)
    except aiogram.exceptions.BotBlocked as err:
        await elogger.warn(f'{user_id} ! send_message BotBlocked exception :: {err}')
        await elogger.preinfo(f'-- {user_id} SRV user disabled')
        await user.set_notifications(user_id, 0)
    except aiogram.exceptions.RetryAfter as err:
        await elogger.warn(f'{user_id} ! send_message RetryAfter exception :: {err}')
        retry_after = err.timeout
        sleep(retry_after)
        await send_message(user_id, message, markup)
    except aiogram.exceptions.BadRequest as err:
        await elogger.warn(f'{user_id} ! send_message BadRequest exception :: {err}')
    except aiogram.exceptions.NetworkError as err:
        await elogger.warn(f'{user_id} ! send_message NetworkError exception :: {err}')
    if message_id:
        await user.update_param(user_id, 'session', {'message_id': message_id})
    return message_id


async def edit_message(user_id, message_id, text, markup=''):
    try:
        await bot.edit_message_text(text=text, chat_id=user_id, message_id=message_id,
                                    parse_mode="html", reply_markup=markup)
        return True
    except aiogram.exceptions.MessageNotModified as err:
        err = str(err)
        if err[72: 92] == 'are exactly the same':
            err = err[:25] + 'every day ' + err[72: 92]
        await elogger.warn(f'{user_id} ! edit_message BadRequest exception :: {err}')
        return True
    except aiogram.exceptions.BadRequest as err:
        await elogger.warn(f'{user_id} ! edit_message BadRequest exception :: {err}')
    except aiogram.exceptions.NetworkError as err:
        await elogger.warn(f'{user_id} ! edit_message NetworkError exception :: {err}')
    return False


async def delete_message(user_id, message_id):
    if message_id:
        try:
            await bot.delete_message(chat_id=user_id, message_id=message_id)
        except aiogram.exceptions.BadRequest as err:
            await elogger.warn(f'{user_id} ! delete_message BadRequest exception :: {err}')


async def answer_callback_query(query_id):
    if query_id:
        try:
            await bot.answer_callback_query(query_id)
        except aiogram.exceptions.BadRequest as err:
            await elogger.warn(f'{query_id} ! answer_callback_query BadRequest exception :: {err}')
