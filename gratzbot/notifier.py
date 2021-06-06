from time import sleep
import mdb
import sender
from misc import birthday_from_offset
from config import admin_id

maindb = mdb.Mdb()

users = sum(maindb.get_notication_requiring(), ())
bday = birthday_from_offset(0)

text = ''
# text = 'Мда, в этот день совсем немного очень известных людей родилось.\n' \
#        'Поэтому я решил выкатить интересную фичу раньше времени. Возможно, она недопеклась.\n' \
#        'Чтобы её увидеть, нужно просто нажать на кнопку с чьим-то именем. Хорошего дня!'

if users:
    for user_id in users:
        sender.send_gratz_brief(user_id, bday)
        sleep(30)
        if user_id == admin_id:
            sender.send_gratz_shift(user_id, +1)
            sleep(2)
            sender.send_gratz_shift(user_id, +1)
            sleep(2)
            sender.send_gratz_shift(user_id, +1)
            sleep(2)
        if text:
            sender.send_message(user_id, text)
