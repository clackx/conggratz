import settings
from misc import bot, birthday_from_offset
import sender
from messages import re_join
import elogger
import user

""" command section """


@bot.message_handler(commands=["start"])
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} SRV command /start')
    user.start(message.from_user)
    sender.greetz(message.chat.id)
    settings.settings(message.chat.id, 4)


@bot.message_handler(commands=["menu"])
@bot.message_handler(regexp=(re_join('main menu', ['menu', 'меню', '<<< Menu'])))
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} SRV command /menu')
    settings.settings(message.chat.id, 4, 'noedit')


@bot.message_handler(commands=["settings"])
@bot.message_handler(commands=["sets"])
@bot.message_handler(regexp=re_join('config'))
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} SRV command /sets')
    settings.settings(message.chat.id, 0, 'noedit')


@bot.message_handler(commands=["help"])
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} SRV command /help')
    sender.helps(message.chat.id)


@bot.message_handler(commands=["day"])
@bot.message_handler(regexp=re_join('today'))
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} INF TODAY')
    sender.send_gratz_brief(message.chat.id, birthday_from_offset(0), noedit=True)


""" day section """


@bot.message_handler(regexp=re_join('tomorrow'))
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} INF TOMORROW')
    sender.send_gratz_brief(message.chat.id, birthday_from_offset(1))


@bot.message_handler(regexp=re_join('yesterday'))
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} INF YESTERDAY')
    sender.send_gratz_brief(message.chat.id, birthday_from_offset(-1))


@bot.message_handler(regexp=re_join('another day'))
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} INF OTHERDAY')
    sender.send_anotherdaytext(message.chat.id)


@bot.message_handler(regexp='^\d{1,2}[\.|-]\d{1,2}$')
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} INF MONTH.DAY {message.text}')
    sender.parseday(message.chat.id, message.text)


""" settings section """


@bot.message_handler(regexp=re_join('keyboard'))
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} STT KEYBOARD')
    settings.settings(message.chat.id, 1)


@bot.message_handler(regexp='^\d{1,2}$')
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} STT NUMERIC {message.text}')
    sender.delete_message(message.chat.id, message.id)
    settings.settings(message.chat.id, 1, message.text)


@bot.message_handler(regexp='^(inline|regular)$')
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} STT NUMERIC {message.text}')
    settings.settings(message.chat.id, 1, message.text)


@bot.message_handler(regexp=re_join('language'))
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} STT LOCALE')
    settings.settings(message.chat.id, 2)


@bot.message_handler(regexp='^.{2} (RU|BE|UK|KK|EN|DE|ES|FR|IT|ZH|KO|JA)$')
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} STT LOCALE {message.text[3:]}')
    settings.settings(message.chat.id, 2, '*' + message.text[3:])


@bot.message_handler(regexp='^(RU|BE|UK|KK|EN|DE|ES|FR|IT|ZH|KO|JA)$')
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} STT LOCALE {message.text}')
    settings.settings(message.chat.id, 2, message.text)


@bot.message_handler(regexp=re_join('notifications'))
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} STT NOTIFIC')
    settings.settings(message.chat.id, 3)


@bot.message_handler(regexp=re_join('ON'))
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} STT NOTIFIC ON')
    settings.settings(message.chat.id, 3, 1)


@bot.message_handler(regexp=re_join('OFF'))
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} STT NOTIFIC OFF')
    settings.settings(message.chat.id, 3, 0)


""" other actions """


@bot.message_handler(regexp=re_join('my favorites'))
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} SRV MYLIKEES')
    sender.send_likees(message.chat.id)


@bot.message_handler(regexp=re_join('review'))
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} SRV REVIEW')
    settings.settings(message.chat.id, 42, 0)


@bot.message_handler(regexp='^fw|fw>>$')
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} SRV forward FW>>')
    sender.delete_message(message.chat.id, message.id)
    sender.send_gratz_shift(message.chat.id, +1)


@bot.message_handler(commands=["fw"])
def docall(message):
    sender.send_gratz_shift(message.chat.id, +1, noedit=True)


@bot.message_handler(regexp='^rw|<<rw$')
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} SRV backward <<RW')
    sender.delete_message(message.chat.id, message.id)
    sender.send_gratz_shift(message.chat.id, -1)


@bot.message_handler(regexp=re_join('about'))
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} INF ABOUT')
    sender.greetz(message.chat.id)


# all text messages handler
@bot.message_handler(func=lambda message: True, content_types=['text'])
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} INF MESSAGE {message.text}')
    if message.text == chr(12951):
        sender.send_message(message.chat.id, chr(129395))
    else:
        sender.incoming(message.chat.id, message.text)


# inline keyboard buttons handler
@bot.callback_query_handler(func=lambda call: True)
def docall(query):
    elogger.preinfo(f'<< {query.message.chat.id} INF BUTTON {query.data}')
    button = query.data[:4]
    clarify = query.data[5:]
    if button == 'like':
        sender.save_liked(query.message.chat.id, clarify, query.id)
    if button == 'more':
        sender.send_more(query.message.chat.id, clarify, query.id)
    if button == 'info':
        sender.answer_callback_query(query.id)
        if clarify == 'rw':
            sender.send_gratz_shift(query.message.chat.id, -1)
        elif clarify == 'fw':
            sender.send_gratz_shift(query.message.chat.id, +1)
        elif clarify == 'menu':
            settings.settings(query.message.chat.id, 4)
        else:
            sender.send_info(query.message.chat.id, clarify)
    if button == 'sets':
        print('sets:', clarify)
        sender.answer_callback_query(query.id)
        if clarify in ('2', '4', '6', '8', '10'):
            settings.settings(query.message.chat.id, 1, clarify)
        elif clarify == 'keyboard':
            settings.settings(query.message.chat.id, 1)
        elif clarify in ('regular', 'inline'):
            settings.settings(query.message.chat.id, 1, clarify)
        elif clarify == 'config':
            settings.settings(query.message.chat.id, 0)
        elif clarify == 'language':
            settings.settings(query.message.chat.id, 2)
        elif clarify[0] == 'x':
            settings.settings(query.message.chat.id, 2, '*' + clarify[1:])
        elif clarify == 'notifications':
            settings.settings(query.message.chat.id, 3)
        elif clarify == 'main_menu':
            settings.settings(query.message.chat.id, 4)
        elif clarify == 'review':
            settings.settings(query.message.chat.id, 42, 0)
        elif clarify == 'ON':
            settings.settings(query.message.chat.id, 3, 1)
        elif clarify == 'OFF':
            settings.settings(query.message.chat.id, 3, 2)

        elif clarify == 'today':
            sender.send_gratz_brief(query.message.chat.id, birthday_from_offset(0))
        elif clarify == 'tomorrow':
            sender.send_gratz_brief(query.message.chat.id, birthday_from_offset(1))
        elif clarify == 'yesterday':
            sender.send_gratz_brief(query.message.chat.id, birthday_from_offset(-1))
        elif clarify == 'another_day':
            sender.send_anotherdaytext(query.message.chat.id)
        elif clarify == 'my_favorites':
            sender.send_likees(query.message.chat.id)
        elif clarify == 'about':
            sender.greetz(query.message.chat.id)
