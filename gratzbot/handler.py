import settings
from misc import bot, birthday_from_offset
import sender
from messages import get_values
import elogger


""" command section """


@bot.message_handler(commands=["start"])
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} SRV command /start')
    sender.greetz(message.chat.id)
    settings.settings(message.chat.id, 4)


@bot.message_handler(commands=["menu"])
@bot.message_handler(regexp=('|'.join(get_values('main menu') + ['menu', 'меню']).replace(' ', '.')))
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} SRV command /menu')
    settings.settings(message.chat.id, 4)


@bot.message_handler(commands=["settings"])
@bot.message_handler(commands=["set"])
@bot.message_handler(regexp='|'.join(get_values('config')))
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} SRV command /set')
    settings.settings(message.chat.id, 0)


@bot.message_handler(commands=["help"])
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} SRV command /help')
    sender.helps(message.chat.id)


@bot.message_handler(commands=["day"])
@bot.message_handler(regexp='|'.join(get_values('today')))
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} INF TODAY')
    sender.send_gratz_brief(message.chat.id, birthday_from_offset(0))


""" day section """


@bot.message_handler(regexp='|'.join(get_values('tomorrow')))
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} INF TOMORROW')
    sender.send_gratz_brief(message.chat.id, birthday_from_offset(1))


@bot.message_handler(regexp='|'.join(get_values('yesterday')))
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} INF YESTERDAY')
    sender.send_gratz_brief(message.chat.id, birthday_from_offset(-1))


@bot.message_handler(regexp='|'.join(get_values('another day')))
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} INF OTHERDAY')
    sender.send_anotherdaytext(message.chat.id)


@bot.message_handler(regexp='\d{1,2}[\.|-]\d{1,2}')
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} INF MONTH.DAY {message.text}')
    sender.parseday(message.chat.id, message.text)


""" settings section """


@bot.message_handler(regexp='|'.join(get_values('keyboard')))
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} STT KEYBOARD')
    settings.settings(message.chat.id, 1)


@bot.message_handler(regexp='\d')
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} STT NUMERIC {message.text}')
    settings.settings(message.chat.id, 1, message.text)


@bot.message_handler(regexp='|'.join(get_values('language')))
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} STT LOCALE')
    settings.settings(message.chat.id, 2)


@bot.message_handler(regexp='^.{2} (RU|BE|UK|KK|EN|DE|ES|FR|ZH|KO|JA)$')
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} STT LOCALE {message.text[3:]}')
    settings.settings(message.chat.id, 2, message.text[3:])


@bot.message_handler(regexp='^(RU|BE|UK|KK|EN|DE|ES|FR|ZH|KO|JA)$')
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} STT LOCALE {message.text}')
    settings.settings(message.chat.id, 2, message.text)


@bot.message_handler(regexp='|'.join(get_values('notifications')))
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} STT NOTIFIC')
    settings.settings(message.chat.id, 3)


#TODO отд. функ
@bot.message_handler(regexp='^('+'|'.join(get_values('ON'))+')$')
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} STT NOTIFIC ON')
    settings.settings(message.chat.id, 3, 1)


@bot.message_handler(regexp='|'.join(get_values('OFF')))
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} STT NOTIFIC OFF')
    settings.settings(message.chat.id, 3, 0)


""" other actions """


@bot.message_handler(regexp=('|'.join(get_values('my favorites')).replace(' ', '.')))
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} SRV MYLIKEES')
    sender.send_likees(message.chat.id)


@bot.message_handler(regexp='|'.join(get_values('review')))
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} SRV REVIEW')
    settings.settings(message.chat.id, 42, 0)


@bot.message_handler(regexp='fw.*')
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} SRV forward FW>>')
    sender.delete_message(message.chat.id, message.id)
    sender.send_gratz_shift(message.chat.id, +1)


@bot.message_handler(regexp='.{0,2}rw')
def docall(message):
    elogger.preinfo(f'<< {message.chat.id} SRV backward <<RW')
    sender.delete_message(message.chat.id, message.id)
    sender.send_gratz_shift(message.chat.id, -1)


@bot.message_handler(regexp='|'.join(get_values('about'))+'$')
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
    wdid = query.data[5:]
    if button == 'like':
        sender.save_liked(query.message.chat.id, wdid, query.id)
