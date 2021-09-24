import json
import elogger
from mdb import maindb, memdb
import datetime
from re import sub


async def _get_settings(user_id):
    data = await memdb.settings(user_id)
    if not data:
        settings = _init_user(user_id)
    else:
        settings = json.loads(data)
    return settings


async def _set_settings(user_id, settings):
    await memdb.update_settings(user_id, json.dumps(settings))
    await maindb.set_sets(user_id, json.dumps(settings))


async def _init_user(user_id, locale='ru', altale='en', day='04.01'):
    settings = {'locale': {'primary': locale, 'altern': altale},
                'keyboard': {'keys': 4, 'entries': 6, 'step': 4, 'type': 'inline'},
                'session': {'message_id': 1, 'offset': 0, 'state': 0, 'bday': day}}
    await maindb.set_user(user_id, json.dumps(settings))
    await _set_settings(user_id, settings)
    return settings


async def start(from_user):
    user_id = from_user.id
    if not await memdb.settings(user_id):
        uname = from_user.username
        locale = from_user.language_code if from_user.language_code else '--'
        fname = from_user.first_name if from_user.first_name else ''
        lname = from_user.last_name if from_user.last_name else ''
        flname = f'{fname} {lname}'.lstrip().rstrip()
        flname = sub(r"[-()\]\[\"'#/@;:<>{}`+=~|.!?,$]", "_", flname)
        regname = flname
        regname += f' ({uname})' if uname else ' (nousername)'
        nowtime = datetime.datetime.now()
        regtime = nowtime.strftime("%d.%m.%Y %H:%M:%S")
        ident_dict = {'locale': locale, 'uname': uname, 'flname': flname, 'regtime': int(nowtime.strftime('%s'))}

        locales_list = ['en', 'ru', 'be', 'uk', 'kk', 'de', 'fr', 'es', 'it', 'zh', 'ko', 'ja']
        if locale not in locales_list:
            locale = 'ru'
        if locale in ['be', 'uk', 'kk']:
            altale = 'ru'
        else:
            altale = 'en'

        await _init_user(user_id, locale, altale, nowtime.strftime('%m.%d'))
        await maindb.ident_user(user_id, regname, regtime, json.dumps(ident_dict, ensure_ascii=False))
        await elogger.preinfo(f'__ {from_user.id} GRTZ JOIN US AS @{uname} :: {flname}, {locale}')
    else:
        await set_notifications(user_id, 1)


async def load_param(userid, param):
    settings = await _get_settings(userid)
    return settings.get(param)


async def update_param(userid, param, data_dict):
    elogger.debug(f'update {userid} param {param}, set {data_dict}')
    settings = await _get_settings(userid)
    settings[param].update(data_dict)
    await _set_settings(userid, settings)


async def set_notifications(user_id, tumbler):
    await maindb.set_notifications(user_id, tumbler)


async def add_to_fav(userid, wdid):
    elogger.enter(f'{userid} adding to fav {wdid}')
    data = await maindb.get_allfav(userid)
    wdids = [d[0] for d in data]
    result = False
    if wdid not in wdids:
        elogger.enter(f'{userid} gettin bday of {wdid}')
        bday = await maindb.get_bday(wdid)
        result = await maindb.add_to_fav(userid, wdid, bday)
    elogger.exiter(f'[OK]', result)
    return result
