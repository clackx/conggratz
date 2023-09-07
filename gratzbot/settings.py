import datetime

from aiogram import types
from getter import get_acc_info, get_flag
from messages import get_translation
from sender import send_message, smartsend, send_gratz_brief
from misc import birthday_from_offset
import user


def get_button(name, locale, kbtype='regular'):
    if kbtype == 'regular':
        text = get_translation(name, locale)
        return types.KeyboardButton(text=text)
    else:
        button = types.InlineKeyboardButton
        if name[3:5] in ('RU', 'BE', 'UK', 'KK', 'EN', 'DE', 'ES', 'FR', 'IT', 'ZH', 'KO', 'JA'):
            text = name
            name = 'x' + name[3:5]
        else:
            text = get_translation(name, locale)
        return button(text=text, callback_data=f'sets_{name.replace(" ", "_")}')


async def settings(userid, rtype, message=''):
    lcl = await user.load_param(userid, 'locale')
    locale = lcl.get('primary')
    kb = await user.load_param(userid, 'keyboard')
    kbtype = kb.get('type')
    s = await user.load_param(userid, 'session')
    state = s.get('state', 0)
    btn_list = 'menu'
    text = '...'

    if rtype == 1:
        set_str = get_translation('set to', locale)
        btn_list_list = (('inline', 'regular'), ('2', '4', '6', '8'),
                         ('4', '6', '8', '10'), ('2', '4', '6', '8'), 'menu')
        line_list = ('number of keys', 'number of entries', 'value of step')
        transl_list = [get_translation('keyboard', locale) + '. ' +
                       get_translation('type', locale) + ': ']
        transl_list += [get_translation(line, locale) for line in line_list]

        if message.lower() in ('inline', 'regular'):
            kbtype = message.lower()
            await user.update_param(userid, 'keyboard', {'type': kbtype})
            await send_message(userid, transl_list[0] + kbtype)
            state = 1
        elif message == '':
            state = 0
        else:
            pass
        choice = message

        if state == 0:
            await user.update_param(userid, 'session', {'state': state + 1})
            text = transl_list[state]
            btn_list = (btn_list_list[state],)
        if state == 1:
            await user.update_param(userid, 'session', {'state': state + 1})
            text = transl_list[state]
            btn_list = (btn_list_list[state],)
        elif state == 2:
            if choice not in btn_list_list[state - 1]:
                choice = '6'
            if kbtype != 'inline':
                await send_message(userid, f'{transl_list[state - 1]}: {set_str} {choice}')
            await user.update_param(userid, 'session', {'state': state + 1})
            await user.update_param(userid, 'keyboard', {'keys': int(choice)})
            text = transl_list[2]
            btn_list = (btn_list_list[2],)
        elif state == 3:
            if choice not in btn_list_list[state - 1]:
                choice = '6'
            kb = await user.load_param(userid, 'keyboard')
            keynum = kb.get('keys')
            if int(choice) < int(keynum):
                choice = keynum
            if kbtype != 'inline':
                await send_message(userid, f'{transl_list[state - 1]}: {set_str} {choice}')
            await user.update_param(userid, 'session', {'state': state + 1})
            await user.update_param(userid, 'keyboard', {'entries': int(choice)})
            text = transl_list[state]
            btn_list = (btn_list_list[state],)
        elif state == 4:
            if choice not in btn_list_list[state - 1]:
                choice = '4'
            kb = await user.load_param(userid, 'keyboard')
            keynum = kb.get('keys', 0)
            if int(choice) > int(keynum):
                choice = keynum
            if kbtype != 'inline':
                await send_message(userid, f'{transl_list[state - 1]}: {set_str} {choice}')
            await user.update_param(userid, 'session', {'state': 0})
            await user.update_param(userid, 'keyboard', {'step': int(choice)})
            text = await get_acc_info(userid)
            btn_list = btn_list_list[state]

    elif rtype == 2:
        btn_list = ((get_flag('RU'), get_flag('EN'), get_flag('ES'), get_flag('ZH')),
                    (get_flag('BE'), get_flag('UK'), get_flag('DE'), get_flag('KO')),
                    (get_flag('KK'), get_flag('IT'), get_flag('FR'), get_flag('JA')))
        if message == '':
            text = get_translation('locale', locale).capitalize()
            await user.update_param(userid, 'session', {'state': 0})
        else:
            if message[0] != '*':
                choise = message.lower()
                await user.update_param(userid, 'locale', {'primary': choise})
                await send_message(userid, get_flag(choise, flagonly=True))
                return
            else:
                choise = message[1:].lower()
                if state == 0:
                    await user.update_param(userid, 'locale', {'primary': choise})
                    await user.update_param(userid, 'session', {'state': 1})
                    text = get_translation('altale', locale).capitalize()
                else:
                    await user.update_param(userid, 'locale', {'altern': choise})
                    await user.update_param(userid, 'session', {'state': 0})
                    text = await get_acc_info(userid)
                    btn_list = 'menu'
            await send_message(userid, get_flag(choise, flagonly=True))

    elif rtype == 3:
        btn_list = 'menu'
        if message == '':
            await send_message(userid, get_translation('inp_timezone', locale))
            await user.update_param(userid, 'session', {'state': 0})
            return
        elif message == 1:
            text = get_translation('notifications', locale) + ': ' + get_translation('ON', locale)
            await user.set_notifications(userid, 1)
        elif message == 0:
            text = get_translation('notifications', locale) + ': ' + get_translation('OFF', locale)
            await user.set_notifications(userid, 0)
        else:
            hours, minutes = message.split(':')
            if int(hours) > 23 or int(minutes) > 59:
                await send_message(userid, '8==3')
                return
            else:
                if state == 0:
                    yourutc = int(hours) - int(datetime.datetime.utcnow().strftime('%H'))
                    utcstr = f'{yourutc}' if yourutc < 0 else f'+{yourutc}'
                    text = f'Timezone: UTC{utcstr}'
                    await user.update_param(userid, 'time', {'timezone': utcstr})
                    await user.update_param(userid, 'session', {'state': 1})
                    await send_message(userid, text)
                    await send_message(userid, f"{get_translation('notitime', locale)}:")
                    return
                else:
                    tm = await user.load_param(userid, 'time')
                    tzone = tm.get('timezone', '3') if tm else '3'
                    utchours = (24 + int(hours) - int(tzone)) % 24
                    utcnoti = str(utchours).zfill(2) + ':' + minutes.zfill(2)
                    usrnoti = hours.zfill(2) + ':' + minutes.zfill(2)
                    await user.update_param(userid, 'time', {'notitime': usrnoti})
                    await user.set_notitime(userid, utcnoti)
                    text = f"{get_translation('notitime', locale)}: {usrnoti}"
                    btn_list = (('ON', 'OFF'),)

    elif rtype == 4 or rtype == 42:
        text = ': : ' + get_translation('main menu', locale) + ' : :'
        btn_list = (('today', 'tomorrow'),
                    ('yesterday', 'another day'),
                    ('config', 'help'))
    else:
        text = await get_acc_info(userid)

    if rtype == 42:
        await user.update_param(userid, 'session', {'state': 4})
        text = get_translation('grateful', locale)
        btn_list = ()

    if rtype == 911:
        if message == 0:
            helpstate = 0
        elif message == 8:
            helpstate = 9
        else:
            helpstate = state
        text = get_translation(f'tour{helpstate}', locale).replace('\n', '\n\n\t')
        text += f' <a href="https://conggratz.ru/stati/tour{helpstate}.png">&#8205;</a>'
        btn_list = (('(skip)', 'next'),)
        if helpstate > 8:
            text = get_translation('endhelp', locale)
            await send_message(userid, text)
            await user.update_param(userid, 'session', {'state': 0})
            await send_gratz_brief(userid, birthday_from_offset(0))
            return
        await user.update_param(userid, 'session', {'state': helpstate + 1})

    if btn_list == 'menu':
        btn_list = (('language', 'keyboard'),
                    ('notifications', 'review'),
                    ('my favorites', 'main menu'))
    if btn_list:
        result_list = []
        for btn_pair in btn_list:
            result_list.append([get_button(btn, locale, kbtype=kbtype) for btn in btn_pair])

        if kbtype == 'regular':
            markup = types.ReplyKeyboardMarkup(keyboard=result_list,
                resize_keyboard=True, one_time_keyboard=True)
        else:
            markup = types.InlineKeyboardMarkup(inline_keyboard=result_list)

        noedit = True if message == 'noedit' else False
        await smartsend(userid, text, markup, kbtype, noedit)

    else:
        await send_message(userid, text)
