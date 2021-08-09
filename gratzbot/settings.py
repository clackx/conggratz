from telebot import types
from getter import get_acc_info, get_flag
from messages import get_translation
from sender import send_message
import user


def settings(chat_id, rtype, message=''):
    locale = user.load_param(chat_id, 'locale').get('primary')
    btn_list = 'menu'
    text = '...'

    if rtype == 1:
        if message == '':
            state = 0
        else:
            state = user.load_param(chat_id, 'session').get('state', 0)
        choice = message
        set_str = get_translation('set to', locale)
        btn_list_list = (('2', '4', '6', '8'), ('4', '6', '8', '10'), ('2', '4', '6', '8'))
        if state == 0:
            user.update_param(chat_id, 'session', {'state': 1})
            user.update_param(chat_id, 'keyboard', {'type': 'regular'})
            text = get_translation('number of keys', locale)
            btn_list = (btn_list_list[0],)
        elif state == 1:
            if choice not in btn_list_list[0]:
                choice = '6'
            send_message(chat_id, f'{set_str}: {choice}')
            user.update_param(chat_id, 'session', {'state': 2})
            user.update_param(chat_id, 'keyboard', {'keys': choice})
            text = get_translation('number of entries', locale)
            btn_list = (btn_list_list[1],)
        elif state == 2:
            if choice not in btn_list_list[1]:
                choice = '6'
            keynum = user.load_param(chat_id, 'keyboard').get('keys')
            if int(choice) < int(keynum):
                choice = keynum
            send_message(chat_id, f'{set_str}: {choice}')
            user.update_param(chat_id, 'session', {'state': 3})
            user.update_param(chat_id, 'keyboard', {'entries': choice})
            text = get_translation('value of step', locale)
            btn_list = (btn_list_list[2],)
        elif state == 3:
            if choice not in btn_list_list[2]:
                choice = '4'
            keynum = user.load_param(chat_id, 'keyboard').get('keys', 0)
            if int(choice) > int(keynum):
                choice = keynum
            send_message(chat_id, f'{set_str}: {choice}')
            user.update_param(chat_id, 'session', {'state': 0})
            user.update_param(chat_id, 'keyboard', {'step': choice})
            text = get_translation('OK', locale)
            btn_list = 'menu'

    elif rtype == 2:
        state = user.load_param(chat_id, 'session').get('state', 0)
        btn_list = ((get_flag('RU'), get_flag('FR'), get_flag('UK'), get_flag('ZH')),
                    (get_flag('EN'), get_flag('ES'), get_flag('BE'), get_flag('KO')),
                    (get_flag('DE'), get_flag('IT'), get_flag('KK'), get_flag('JA')))
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
            btn_list = ((get_translation('ON', locale), get_translation('OFF', locale)),)
        elif message == 1:
            text = get_translation('notifications', locale) + ': ' + get_translation('ON', locale)
            user.set_notifications(chat_id, 1)
        else:
            text = get_translation('notifications', locale) + ': ' + get_translation('OFF', locale)
            user.set_notifications(chat_id, 0)

    elif rtype == 4 or rtype == 42:
        text = get_translation('main menu', locale)
        btn_list = ((get_translation('today', locale), get_translation('tomorrow', locale)),
                    (get_translation('yesterday', locale), get_translation('another day', locale)),
                    (get_translation('config', locale), get_translation('about', locale)))
    else:
        text = get_acc_info(chat_id)

    if rtype == 42:
        user.update_param(chat_id, 'session', {'state': 4})
        text = get_translation('grateful', locale)

    if btn_list == 'menu':
        btn_list = ((get_translation('language', locale)+' (Lang)', get_translation('keyboard', locale)),
                    (get_translation('notifications', locale), get_translation('review', locale)),
                    (get_translation('my favorites', locale), get_translation('main menu', locale)))

    if btn_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                           row_width=len(btn_list[0]), one_time_keyboard=True)
        for btn_tuple in btn_list:
            markup.add(*btn_tuple)
        send_message(chat_id, text, markup=markup)
    else:
        send_message(chat_id, text)
