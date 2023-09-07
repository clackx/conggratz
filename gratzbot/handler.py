from aiogram import F, Router
from aiogram.filters.command import Command

import settings
from misc import dp, birthday_from_offset
import sender
from messages import re_join
import elogger
import user

router = Router()

""" command section """


@dp.message(Command("start"))
@router.message(Command("start"))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} SRV command /start')
    await user.start(message.from_user)
    await sender.helps(message.chat.id)


@dp.message(Command("menu"))
@router.message(Command("menu"))
@dp.message(F.text.regexp((re_join('main menu', ['menu', 'меню', '<<< Menu']))))
@router.message(F.text.regexp((re_join('main menu', ['menu', 'меню', '<<< Menu']))))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} SRV command /menu')
    await settings.settings(message.chat.id, 4, 'noedit')


@dp.message(Command("sets"))
@router.message(Command("sets"))
@dp.message(Command("settings"))
@router.message(Command("settings"))
@dp.message(F.text.regexp(re_join('config')))
@router.message(F.text.regexp(re_join('config')))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} SRV command /sets')
    await settings.settings(message.chat.id, 0, 'noedit')


@dp.message(Command("help"))
@router.message(Command("help"))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} SRV command /help')
    await sender.helps(message.chat.id)


@dp.message(Command("day"))
@router.message(Command("day"))
@dp.message(F.text.regexp(re_join('today', ['brief', 'day'])))
@router.message(F.text.regexp(re_join('today', ['brief', 'day'])))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} INF TODAY')
    await sender.send_gratz_brief(message.chat.id, birthday_from_offset(0), noedit=True)


""" day section """


@dp.message(F.text.regexp(re_join('tomorrow')))
@router.message(F.text.regexp(re_join('tomorrow')))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} INF TOMORROW')
    await sender.send_gratz_brief(message.chat.id, birthday_from_offset(1))


@dp.message(F.text.regexp(re_join('yesterday')))
@router.message(F.text.regexp(re_join('yesterday')))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} INF YESTERDAY')
    await sender.send_gratz_brief(message.chat.id, birthday_from_offset(-1))


@dp.message(F.text.regexp(re_join('another day')))
@router.message(F.text.regexp(re_join('another day')))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} INF OTHERDAY')
    await sender.send_anotherdaytext(message.chat.id)


@dp.message(F.text.regexp('^\d{1,2}[\.|-]\d{1,2}$'))
@router.message(F.text.regexp('^\d{1,2}[\.|-]\d{1,2}$'))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} INF MONTH.DAY {message.text}')
    await sender.parseday(message.chat.id, message.text)


""" settings section """


@dp.message(F.text.regexp(re_join('keyboard')))
@router.message(F.text.regexp(re_join('keyboard')))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} STT KEYBOARD')
    await settings.settings(message.chat.id, 1)


@dp.message(F.text.regexp('^\d{1,2}:\d{1,2}$'))
@router.message(F.text.regexp('^\d{1,2}:\d{1,2}$'))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} STT TIME {message.text}')
    await settings.settings(message.chat.id, 3, message.text)


@dp.message(F.text.regexp('^\d{1,2}$'))
@router.message(F.text.regexp('^\d{1,2}$'))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} STT NUMERIC {message.text}')
    await sender.delete_message(message.chat.id, message.message_id)
    await settings.settings(message.chat.id, 1, message.text)


@dp.message(F.text.regexp('^(inline|regular)$'))
@router.message(F.text.regexp('^(inline|regular)$'))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} STT NUMERIC {message.text}')
    await settings.settings(message.chat.id, 1, message.text)


@dp.message(Command("lang"))
@router.message(Command("lang"))
@dp.message(F.text.regexp(re_join('language')))
@router.message(F.text.regexp(re_join('language')))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} STT LOCALE')
    await settings.settings(message.chat.id, 2)


@dp.message(F.text.regexp('^.{2} (RU|BE|UK|KK|EN|DE|ES|FR|IT|ZH|KO|JA)$'))
@router.message(F.text.regexp('^.{2} (RU|BE|UK|KK|EN|DE|ES|FR|IT|ZH|KO|JA)$'))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} STT LOCALE {message.text[3:]}')
    await settings.settings(message.chat.id, 2, '*' + message.text[3:])


@dp.message(F.text.regexp('(?i)^(RU|BE|UK|KK|EN|DE|ES|FR|IT|ZH|KO|JA)$'))
@router.message(F.text.regexp('(?i)^(RU|BE|UK|KK|EN|DE|ES|FR|IT|ZH|KO|JA)$'))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} STT LOCALE {message.text}')
    await settings.settings(message.chat.id, 2, message.text)


@dp.message(F.text.regexp(re_join('notifications')))
@router.message(F.text.regexp(re_join('notifications')))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} STT NOTIFIC')
    await settings.settings(message.chat.id, 3)


@dp.message(F.text.regexp(re_join('ON')))
@router.message(F.text.regexp(re_join('ON')))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} STT NOTIFIC ON')
    await settings.settings(message.chat.id, 3, 1)


@dp.message(F.text.regexp(re_join('OFF')))
@router.message(F.text.regexp(re_join('OFF')))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} STT NOTIFIC OFF')
    await settings.settings(message.chat.id, 3, 0)


""" other actions """


@dp.message(F.text.regexp(re_join('my favorites')))
@router.message(F.text.regexp(re_join('my favorites')))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} SRV MYLIKEES')
    await sender.send_likees(message.chat.id)


@dp.message(F.text.regexp(re_join('review')))
@router.message(F.text.regexp(re_join('review')))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} SRV REVIEW')
    await settings.settings(message.chat.id, 42, 0)


@dp.message(F.text.regexp('^fw|fw>>$'))
@router.message(F.text.regexp('^fw|fw>>$'))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} SRV forward FW>>')
    await sender.delete_message(message.chat.id, message.message_id)
    await sender.send_gratz_shift(message.chat.id, +1)


@dp.message(Command("fw"))
@router.message(Command("fw"))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} SRV command /fw')
    await sender.send_gratz_shift(message.chat.id, +1, noedit=True)


@dp.message(F.text.regexp('^rw|bw|<<rw$'))
@router.message(F.text.regexp('^rw|bw|<<rw$'))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} SRV backward <<RW')
    await sender.delete_message(message.chat.id, message.message_id)
    await sender.send_gratz_shift(message.chat.id, -1)


@dp.message(F.text.regexp(re_join('help')))
@router.message(F.text.regexp(re_join('help')))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} INF HELP')
    await settings.settings(message.chat.id, 911, 0)


@dp.message(F.text.regexp('^next$'))
@router.message(F.text.regexp('^next$'))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} INF TOUR')
    await sender.delete_message(message.chat.id, message.message_id)
    await settings.settings(message.chat.id, 911)


@dp.message(F.text.regexp('^\(skip\)|skip$'))
@router.message(F.text.regexp('^\(skip\)|skip$'))
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} INF SKIP')
    await sender.delete_message(message.chat.id, message.message_id)
    await settings.settings(message.chat.id, 911, 8)


# all text messages handler
@dp.message(F.text)
@router.message(F.text)
async def docall(message):
    await elogger.preinfo(f'<< {message.chat.id} MSG MESSAGE {message.text}')
    if message.text == chr(12951):
        await sender.send_message(message.chat.id, chr(129395))
    else:
        await sender.incoming(message.chat.id, message.text)


# inline keyboard buttons handler
@dp.callback_query()
@router.callback_query()
async def docall(query):
    button = query.data[:4]
    clarify = query.data[5:]
    if button == 'like':
        await elogger.preinfo(f'<< {query.message.chat.id} SRV LIKE {clarify}')
        await sender.save_liked(query.message.chat.id, clarify, query.id)
    if button == 'more':
        await elogger.preinfo(f'<< {query.message.chat.id} SRV MORE {clarify}')
        await sender.send_more(query.message.chat.id, clarify, query.id)
    if button == 'info':
        await elogger.preinfo(f'<< {query.message.chat.id} INF BUTTON {clarify}')
        await sender.answer_callback_query(query.id)
        if clarify == 'rw':
            await sender.send_gratz_shift(query.message.chat.id, -1)
        elif clarify == 'fw':
            await sender.send_gratz_shift(query.message.chat.id, +1)
        elif clarify == 'menu':
            await settings.settings(query.message.chat.id, 4)
        else:
            await sender.send_info(query.message.chat.id, clarify)
    if button == 'sets':
        await elogger.preinfo(f'<< {query.message.chat.id} SRV BUTTON {clarify}')
        await sender.answer_callback_query(query.id)
        if clarify in ('2', '4', '6', '8', '10'):
            await settings.settings(query.message.chat.id, 1, clarify)
        elif clarify == 'keyboard':
            await settings.settings(query.message.chat.id, 1)
        elif clarify in ('regular', 'inline'):
            await settings.settings(query.message.chat.id, 1, clarify)
        elif clarify == 'config':
            await settings.settings(query.message.chat.id, 0)
        elif clarify == 'language':
            await settings.settings(query.message.chat.id, 2)
        elif clarify[0] == 'x':
            await settings.settings(query.message.chat.id, 2, '*' + clarify[1:])
        elif clarify == 'notifications':
            await settings.settings(query.message.chat.id, 3)
        elif clarify == 'main_menu':
            await settings.settings(query.message.chat.id, 4)
        elif clarify == 'review':
            await settings.settings(query.message.chat.id, 42, 0)
        elif clarify == 'ON':
            await settings.settings(query.message.chat.id, 3, 1)
        elif clarify == 'OFF':
            await settings.settings(query.message.chat.id, 3, 2)
        elif clarify == 'help':
            await settings.settings(query.message.chat.id, 911, 0)
        elif clarify == 'next':
            await settings.settings(query.message.chat.id, 911)
        elif clarify == '(skip)':
            await settings.settings(query.message.chat.id, 911, 8)
        elif clarify == 'today':
            await sender.send_gratz_brief(query.message.chat.id, birthday_from_offset(0))
        elif clarify == 'tomorrow':
            await sender.send_gratz_brief(query.message.chat.id, birthday_from_offset(1))
        elif clarify == 'yesterday':
            await sender.send_gratz_brief(query.message.chat.id, birthday_from_offset(-1))
        elif clarify == 'another_day':
            await sender.send_anotherdaytext(query.message.chat.id)
        elif clarify == 'my_favorites':
            await sender.send_likees(query.message.chat.id)
