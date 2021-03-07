import json
import elogger
import mdb

maindb = mdb.Mdb()
memdb = mdb.Memdb()


def _get_settings(user_id):
    data = memdb.settings(user_id)
    if not data:
        settings = _init_user(user_id)
    else:
        settings = json.loads(data)
    return settings


def _set_settings(user_id, settings):
    memdb.update_settings(user_id, json.dumps(settings))
    maindb.set_user(user_id, json.dumps(settings))


def _init_user(user_id):
    settings = {'locale': {'primary': 'ru'},
                'keyboard': {'keys': 4, 'entries': 8, 'step': 4, 'type': 'regular'},
                'session': {'message_id': 1}}
    _set_settings(user_id, settings)
    return settings


def load_param(userid, param):
    settings = _get_settings(userid)
    return settings.get(param)


def update_param(userid, param, data_dict):
    elogger.debug(f'update {userid} param {param}, set {data_dict}')
    settings = _get_settings(userid)
    settings[param].update(data_dict)
    _set_settings(userid, settings)


def set_notifications(user_id, tumbler):
    maindb.set_notifications(user_id, tumbler)


def add_to_fav(userid, wdid):
    return maindb.add_to_fav(userid, wdid)
