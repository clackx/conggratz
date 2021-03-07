import time
import settings
import sender
from config import admin_id
import elogger

elogger.enter('))) NOSERVER (((')

chat_id = admin_id


settings.settings(chat_id, 2, 'EN')
sender.greetz(chat_id)

# set RU locale, first run init user (table users)
settings.settings(chat_id, 2, 'RU')

# show info about ? with only cached tags (table tags)
sender.send_info(chat_id, 'Douglas Adams')

# set EN locale
settings.settings(chat_id, 2, 'RU')
settings.settings(chat_id, 0)
sender.send_info(chat_id, 'CG')

# show info about ? with cached tags and cached occupations on previous request
sender.send_info(chat_id, 'Дуглас Адамс')

# show info without any cache data (at first run)
sender.send_info(chat_id, 'Байнам, Эндрю')

# show persons born Feb, 28
# it cache tags data, occupations and namelinks in chosen language
sender.send_gratz_brief(chat_id, '02.28')

# second run takes about 10-100 times ?? less time to show persons born at Feb, 28
sender.send_gratz_brief(chat_id, '02.28')

sender.send_gratz_shift(chat_id, +1)
time.sleep(2)
sender.send_gratz_shift(chat_id, +1)
time.sleep(2)
sender.send_gratz_shift(chat_id, +1)
time.sleep(2)
# and back
# sender.send_gratz_shift(chat_id, -1)
# sender.send_gratz_shift(chat_id, -1)
# sender.send_gratz_shift(chat_id, -1)
# sender.send_gratz_shift(chat_id, -1)

# SETTINGS

# change ui params
settings.settings(chat_id, 1, '')
# Number of keys (must be even) ??
settings.settings(chat_id, 1, '7')
# Number of entries (can't be less than keys (so it'll be fixed))
settings.settings(chat_id, 1, '3')
# Value of step (must be even and can't be more than keys)
settings.settings(chat_id, 1, '5')

# continue navigate back and forth
sender.send_gratz_shift(chat_id, -1)
time.sleep(2)
sender.send_gratz_shift(chat_id, 1)

# show your settings
settings.settings(chat_id, 0)

# and continue navigate
sender.send_gratz_shift(chat_id, -1)
time.sleep(2)
sender.send_gratz_shift(chat_id, -1)

# toggle everyday notification on/off
settings.settings(chat_id, 3, 1)
settings.settings(chat_id, 3, 0)

# sender.send_info(chat_id, 'Ягр, Яромир')
# sender.send_info(chat_id, 'Aleksey Tolstoy')
# sender.send_info(chat_id, '彭帅')

elogger.exiter(')))', True)
