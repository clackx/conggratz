import mdb
import sender
from misc import birthday_from_offset

maindb = mdb.Mdb()

users = maindb.get_notication_requiring()
bday = birthday_from_offset(0)
for user_id, settings in users:
    sender.send_gratz_brief(user_id, bday)
