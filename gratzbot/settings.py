from telebot import types
from getter import get_acc_info, get_flag
from messages import get_translation
from sender import send_message, smartsend, send_gratz_brief
from misc import birthday_from_offset
import user


def get_button(name, locale, kbtype='regular'):
    if kbtype == 'regular':
        button = types.KeyboardButton
        text = get_translation(name, locale)
        return button(text)
    else:
        button = types.InlineKeyboardButton
        if name[3:5] in ('RU', 'BE', 'UK', 'KK', 'EN', 'DE', 'ES', 'FR', 'IT', 'ZH', 'KO', 'JA'):
            text = name
            name = 'x' + name[3:5]
        else:
            text = get_translation(name, locale)
        return button(text=text, callback_data=f'sets_{name.replace(" ", "_")}')


def settings(chat_id, rtype, message=''):
    locale = user.load_param(chat_id, 'locale').get('primary')
    kbtype = user.load_param(chat_id, 'keyboard').get('type')
    s = user.load_param(chat_id, 'session')
    prev_message_id = s.get('message_id')
    prev_sets_mess_id = s.get('sets_mess_id')

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
            user.update_param(chat_id, 'keyboard', {'type': kbtype})
            send_message(chat_id, transl_list[0] + kbtype)
            state = 1
        elif message == '':
            state = 0
        else:
            state = user.load_param(chat_id, 'session').get('state', 0)
        choice = message

        if state == 0:
            user.update_param(chat_id, 'session', {'state': state + 1})
            text = transl_list[state]
            btn_list = (btn_list_list[state],)
        if state == 1:
            user.update_param(chat_id, 'session', {'state': state + 1})
            text = transl_list[state]
            btn_list = (btn_list_list[state],)
        elif state == 2:
            if choice not in btn_list_list[state - 1]:
                choice = '6'
            if kbtype != 'inline':
                send_message(chat_id, f'{transl_list[state - 1]}: {set_str} {choice}')
            user.update_param(chat_id, 'session', {'state': state + 1})
            user.update_param(chat_id, 'keyboard', {'keys': int(choice)})
            text = transl_list[2]
            btn_list = (btn_list_list[2],)
        elif state == 3:
            if choice not in btn_list_list[state - 1]:
                choice = '6'
            keynum = user.load_param(chat_id, 'keyboard').get('keys')
            if int(choice) < int(keynum):
                choice = keynum
            if kbtype != 'inline':
                send_message(chat_id, f'{transl_list[state - 1]}: {set_str} {choice}')
            user.update_param(chat_id, 'session', {'state': state + 1})
            user.update_param(chat_id, 'keyboard', {'entries': int(choice)})
            text = transl_list[state]
            btn_list = (btn_list_list[state],)
        elif state == 4:
            if choice not in btn_list_list[state - 1]:
                choice = '4'
            keynum = user.load_param(chat_id, 'keyboard').get('keys', 0)
            if int(choice) > int(keynum):
                choice = keynum
            if kbtype != 'inline':
                send_message(chat_id, f'{transl_list[state - 1]}: {set_str} {choice}')
            user.update_param(chat_id, 'session', {'state': 0})
            user.update_param(chat_id, 'keyboard', {'step': int(choice)})
            text = get_acc_info(chat_id)
            btn_list = btn_list_list[state]

    elif rtype == 2:
        state = user.load_param(chat_id, 'session').get('state', 0)
        btn_list = ((get_flag('RU'), get_flag('EN'), get_flag('ES'), get_flag('ZH')),
                    (get_flag('BE'), get_flag('UK'), get_flag('DE'), get_flag('KO')),
                    (get_flag('KK'), get_flag('IT'), get_flag('FR'), get_flag('JA')))
        if message == '':
            text = get_translation('locale', locale).capitalize()
            user.update_param(chat_id, 'session', {'state': 0})
        else:
            if message[0] != '*':
                choise = message.lower()
                user.update_param(chat_id, 'locale', {'primary': choise})
                send_message(chat_id, get_flag(choise, flagonly=True))
                return
            else:
                choise = message[1:].lower()
                if state == 0:
                    user.update_param(chat_id, 'locale', {'primary': choise})
                    user.update_param(chat_id, 'session', {'state': 1})
                    text = get_translation('altale', locale).capitalize()
                else:
                    user.update_param(chat_id, 'locale', {'altern': choise})
                    user.update_param(chat_id, 'session', {'state': 0})
                    text = get_acc_info(chat_id)
                    btn_list = 'menu'
            send_message(chat_id, get_flag(choise, flagonly=True))

    elif rtype == 3:
        btn_list = 'menu'
        if message == '':
            text = get_translation('notifications', locale)
            btn_list = (('ON', 'OFF'),)
        elif message == 1:
            text = get_translation('notifications', locale) + ': ' + get_translation('ON', locale)
            user.set_notifications(chat_id, 1)
        else:
            text = get_translation('notifications', locale) + ': ' + get_translation('OFF', locale)
            user.set_notifications(chat_id, 0)

    elif rtype == 4 or rtype == 42:
        text = ': : ' + get_translation('main menu', locale) + ' : :'
        btn_list = (('today', 'tomorrow'),
                    ('yesterday', 'another day'),
                    ('config', 'help'))
    else:
        text = get_acc_info(chat_id)

    if rtype == 42:
        user.update_param(chat_id, 'session', {'state': 4})
        text = get_translation('grateful', locale)
        btn_list = ()

    if rtype == 911:
        if message == 0:
            helpstate = 0
        elif message == 8:
            helpstate = 9
        else:
            helpstate = user.load_param(chat_id, 'session').get('state', 0)
        text = get_translation(f'tour{helpstate}', locale).replace('\n', '\n\n\t')
        text += f' <a href="https://conggratz.ru/stati/tour{helpstate}.png">&#8205;</a>'
        btn_list = (('(skip)', 'next'),)
        if helpstate > 8:
            text = get_translation('endhelp', locale)
            send_message(chat_id, text)
            user.update_param(chat_id, 'session', {'state': 0})
            send_gratz_brief(chat_id, birthday_from_offset(0))
            return
        user.update_param(chat_id, 'session', {'state': helpstate + 1})

    if btn_list == 'menu':
        btn_list = (('language', 'keyboard'),
                    ('notifications', 'review'),
                    ('my favorites', 'main menu'))
    if btn_list:
        if kbtype == 'regular':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                               row_width=len(btn_list[0]), one_time_keyboard=True)
        else:
            markup = types.InlineKeyboardMarkup(row_width=len(btn_list[0]))

        for btn_tuple in btn_list:
            res = [get_button(btn, locale, kbtype=kbtype) for btn in btn_tuple]
            markup.add(*res)

        noedit = True if message == 'noedit' else False
        smartsend(chat_id, text, markup, kbtype, noedit)

    else:
        send_message(chat_id, text)
