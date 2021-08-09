import requests
import grequests
import json
from datetime import datetime
from telebot import types
from mdb import maindb
import user
import elogger
from misc import get_wc_thumb
from messages import get_translation, get_dayname
from config import admin_id


def please_request(url, params=''):
    """ safe request *url* with *params* """
    elogger.enter(f'>< requesting {url} with {str(params)[:100]}')
    is_request_successful = False
    result = ''
    try:
        r = requests.get(url, params=params, timeout=3)
        r.raise_for_status()
        is_request_successful = True
        result = r.json()
        if 'error' in result:
            is_request_successful = False
        elogger.exiter(f'[OK] {r.status_code}', result)
    except requests.exceptions.HTTPError as e:
        elogger.error(f'!! Http Error: {e}')
    except requests.exceptions.ConnectionError as e:
        elogger.error(f'!! Error Connecting: {e}')
    except requests.exceptions.Timeout as e:
        elogger.error(f'!! Timeout Error: {e}')
    except requests.exceptions.RequestException as e:
        elogger.error(f'!! Oops: {e}')

    return is_request_successful, result


def request_wiki_info(namelink, locale):
    """ request wikipedia for extracts intro (content before the first section)
    of page *namelink* on *locale* language """
    elogger.debug(f'----- request_wiki_info :: {namelink} @ {locale}')
    url = f"https://{locale}.wikipedia.org/w/api.php?action=query&format=json" \
          f"&prop=extracts&explaintext=1&exintro=1&titles={namelink}"
    is_request_successful, r = please_request(url)
    if is_request_successful:
        pages = r['query']['pages']
        info = pages[list(pages)[0]]['extract']
        info = info.replace(chr(769), '')  # accent mark remove
        info = '\n\n '.join(info.split('\n'))
        info = info.rstrip()
        return info


def get_notional_value(data_dict, locale, altale):
    """ Get *locale* key value from cached *data_dict*
    If locale value is empty, get value of default 'en'
    If default value is empty, get first non-empty """
    (key, value) = (locale, None)
    if len(data_dict):
        value = data_dict.get(key)
        if not value:
            key = altale
            value = data_dict.get(key)
            if not value:
                for key in data_dict.keys():
                    value = data_dict[key]
                    if value:
                        break
                if not value:
                    elogger.warn(f'No data in {data_dict}')
    return key, value


def get_universal(utypename, wdentities, locale, altale):
    """ most complicated function (with preloaded db becames pretty simple)
    it returns dictionary of entities with pair: {wdentity: (locale, value)}
    First gets *unidata*, db query with *wdentity* and *descr_cache* pairs,
    then starts assembling *result_dict*
    and *full_dict* containing not pairs but full json with localized descriptions.
    If unidata has no entries for entity, that entity is appended to request list.
    The second part requests entities from wikidata and appends them to full_dict
    Every entity from second part is included in result_dict and db store """
    elogger.enter(f'----- get:{utypename} of {str(wdentities)[:100]}  entities in {locale}')
    full_dict = dict([(i, {}) for i in wdentities])
    result_dict = dict([(i, (None, None)) for i in wdentities])

    unidata = maindb.get_universal(utypename, wdentities)

    for wdentity, descr_cache in unidata:
        if descr_cache:
            descr_dict = json.loads(descr_cache)
            full_dict[wdentity] = descr_dict
            value = ''
            if locale in descr_dict:
                value = descr_dict[locale]

            # preloaded db needs no outer requests
            key = locale
            if not value:
                elogger.warn(f'{wdentity} has no {key} in {utypename}')
                key, value = get_notional_value(descr_dict, locale, altale)
                if not value:
                    elogger.warn(f'{wdentity} has no description at all !!')
                    value = '--nodata--'

            result_dict[wdentity] = (key, value)

    elogger.exiter('[OK]', result_dict)
    return result_dict


def get_tags(wdentity, locale, altale):
    """ get tags from db as list of pairs (entity, emoji code),
    get from universe description labels for all entities,
    compile result *emores* as emoji chars and description """
    elogger.enter(f'----- get_tags {wdentity} @ {locale}')
    check_tags([wdentity, ])
    emojis_list = maindb.get_tags(wdentity)
    entity_list = [en[0] for en in emojis_list]
    emoji_list = [em[1] for em in emojis_list]

    desc_dict = get_universal('labels', entity_list, locale, altale)
    emores = ''
    for i in range(0, len(entity_list)):
        l_tmp, descr = desc_dict.get(entity_list[i])
        emojis = emoji_list[i]
        emores += f' {descr} '
        emores += get_emoji_chars(emojis)

    elogger.exiter(f'[OK] TAGS of {wdentity}: {len(entity_list)} pcs. ', emores)
    return emores


def get_emoji_chars(emojis):
    """ get emoji chars from unified hex notation """
    emores = ''
    if emojis:
        for emoji in emojis.split():
            emores += chr(int(emoji[2:], 16))
    else:
        emores += chr(128100)
    return emores


def get_first_emoji(emoji_str):
    emoji = '⁉️'
    if len(emoji_str):
        for splitter in ('•', ' ', '-'):
            split_index = emoji_str.find(splitter)
            if split_index != -1:
                emoji_str = emoji_str[:split_index]
        emoji = emoji_str
    return emoji


def get_info(wdid, locale, altale):
    """ get all stuff (tags, text and keyboard) for person info card """
    key, namelink = get_universal('sitelinks', [wdid], locale, altale)[wdid]
    info = request_wiki_info(namelink, key)
    tags = get_tags(wdid, locale, altale)
    text = f'<i>{tags}</i>\n\n{info}'
    if len(text) > 3896:
        text = text[:3896] + '...'
    keyboard = get_inline_keyboard(wdid, namelink, key)
    return text, keyboard


def get_shift_params(userid, direction):
    """ get user session params for shift operation """
    step = user.load_param(userid, 'keyboard').get('step')
    s = user.load_param(userid, 'session')
    bday = s.get('bday')
    offset = s.get('offset') + direction * int(step)
    is_rested = False
    if offset < 0:
        offset = 0
        is_rested = True
    message_id = s.get('message_id')
    return message_id, bday, offset, is_rested


def get_day_plus(userid, bday, offset):
    """ get user session params to call *get_day_info* """
    elogger.enter(' ++++ MAIN')
    locale = user.load_param(userid, 'locale').get('primary')
    altale = user.load_param(userid, 'locale').get('altern', 'en')
    keyboard = user.load_param(userid, 'keyboard')
    count = keyboard.get('entries')
    buttons = keyboard.get('keys')
    debug = True if userid == admin_id else False
    text, names = get_day_info(bday, locale, altale, offset, count, debug)
    keyboard = get_keyboard(names, buttons)
    elogger.exiter('[OK] MAIN', text)
    return text, keyboard


def get_day_info(bday, locale, altale, offset, count, debug=False):
    """ get full *bday* info with *count* entries from starting *offset*
     every entry contains name from namelist, tag (emoji + description)
     and short description from desclist """
    elogger.enter(f'----- get_today {bday}, {count} items')
    starttime = datetime.now()

    res_text = f'{get_dayname(bday, locale)} {get_translation("were born", locale)}:\n\n'
    data = maindb.get_day_intro(bday, locale, offset, count)
    entities = sum(data, ())
    namelist = get_universal('sitelinks', entities, locale, altale)
    desclist = get_universal('descriptions', entities, locale, altale)

    check_tags(entities)
    data = maindb.get_emojis(entities)
    tagdixt = {}
    for wde, emojis in data:
        emores = get_emoji_chars(emojis)
        tagdixt.setdefault(wde, '')
        tagdixt[wde] += emores + '•'

    res_names = []
    for wdentity in entities:
        l_tmp, name = namelist[wdentity]
        l_tmp, desc = desclist[wdentity]
        flag = get_person_flag(wdentity)
        tag = tagdixt.get(wdentity, chr(8265))
        ftag = get_first_emoji(tag)
        if tag == chr(8265):
            elogger.warn(f'{wdentity} ({name}) has no tags')
        res_names.append(name)
        res_text += f' {flag}{ftag} : : {name}\n{desc}\n\n'

    endtime = datetime.now()
    stata = "<code>Spend {}s to request</code>".format((endtime - starttime).total_seconds())
    res_text += stata if debug else ''
    elogger.exiter('[OK] all great ', stata)
    return res_text, res_names


def get_keyboard(names, buttons):
    """ build keyboard markup from list of names and 2 nav buttons """
    elogger.debug(f'get_keyboard {str(names)[:100]}')
    button = types.KeyboardButton
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for i in range(0, int(buttons), 2):
        markup.add(button(text=names[i]), button(text=names[i + 1]))
    markup.add(button(text="<<RW"), button(text="FW>>"))
    return markup


def get_inline_keyboard(wdid, name, locale):
    """ build inline keyboard markup with (so far) 2 buttons, Like and More.. """
    elogger.debug(f'get_inline_keyboard {wdid}')
    name = name.replace(u'\u2019', '%E2%80%99')
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    info_btn = types.InlineKeyboardButton(text=u'\U0001F497' + " Like", callback_data=f'like_{wdid}')
    more_btn = types.InlineKeyboardButton(text=u'\U0001F9E0' + " More..",
                                          url=f'https://{locale}.m.wikipedia.org/wiki/{name}')
    keyboard.row(info_btn, more_btn)
    return keyboard


def get_photo_link(wdid):
    """ query photo entry and generate full wikimedia link """
    elogger.enter(f'----- get_photo_link {wdid}')
    photo = maindb.get_photo(wdid)
    result = get_wc_thumb(photo)
    elogger.exiter(f'[OK] get_photo_link', result)
    return result


def get_acc_info(userid):
    """ get user settings localized info """
    locale = user.load_param(userid, 'locale').get('primary')
    keyb = user.load_param(userid, 'keyboard')
    spaces = len(get_translation('number of entries', locale)) + 1
    res_str = f"{get_translation('config', locale)}:\n"
    res_str += f"<code>{(get_translation('language', locale) + ':').ljust(spaces)}  " \
               f"{locale}  {get_flag(locale, flagonly=True)}\n"
    res_str += f"{get_translation('keyboard', locale)}:\n"
    res_str += f"├{(get_translation('type', locale) + ':').ljust(spaces)} {keyb.get('type')} \n"
    res_str += f"├{(get_translation('number of keys', locale) + ':').ljust(spaces)} {keyb.get('keys')} \n"
    res_str += f"├{(get_translation('number of entries', locale) + ':').ljust(spaces)} {keyb.get('entries')} \n"
    res_str += f"╰{(get_translation('value of step', locale) + ':').ljust(spaces)} {keyb.get('step')}\n</code>"
    return res_str


def get_all_fav(userid):
    """ get all entries of favorites """
    elogger.enter(f'----- get_all_fav {userid}')
    locale = user.load_param(userid, 'locale').get('primary')
    altale = user.load_param(userid, 'locale').get('altern', 'en')
    wdentities = sum(maindb.get_allfav(userid), ())
    data = get_universal('sitelinks', wdentities, locale, altale)
    result = ''
    for wdid in wdentities:
        result += f'{data[wdid][1]}\n'
    if not result:
        result = 'N/A'
    elogger.exiter(f'[OK]', result)
    return result


def get_flag(country, flagonly=False):
    """ get country flag emoji """
    emojis = get_translation('flags', country.upper())
    emores = get_emoji_chars(emojis)
    if flagonly or country == 'CG':
        return emores
    return f'{emores} {country}'


def get_person_flag(wdentity):
    flags = maindb.get_flags(wdentity)
    if not flags:
        return get_emoji_chars('U+1F5FA')
    else:
        res_emoji_flag = '-'
        for tmp_wde, emoji_flag in flags:
            if not res_emoji_flag:
                res_emoji_flag = emoji_flag

            if emoji_flag[0] == 'U':
                if res_emoji_flag[0] != 'U':
                    res_emoji_flag = emoji_flag

            if emoji_flag[0] == '~':
                if res_emoji_flag[0] == '-':
                    res_emoji_flag = emoji_flag

        if res_emoji_flag[0] == '-':
            return get_emoji_chars('U+1F5FA')
        if res_emoji_flag[0] == '~':
            return get_emoji_chars(res_emoji_flag[2:]) + '*'

        return get_emoji_chars(res_emoji_flag)


def check_tags(entities):
    """ It has been added in final stage and breaks some logic
    Returns nothing, but requests and stores absent tags """
    data = maindb.get_entities(entities)
    data_list = sum(data, ())

    result_values = []
    entities_to_request = []
    for entity in entities:
        if entity not in data_list:
            entities_to_request.append(entity)

    if entities_to_request:
        elogger.debug('Need to request: ' + str(entities_to_request))
        for entity in entities_to_request:
            url = f'https://www.wikidata.org/w/api.php?' \
                  f'action=wbgetclaims&format=json&entity={entity}&property=P106'
            is_good, r = please_request(url)
            if is_good and r['claims']:
                for entry in r['claims']['P106']:
                    wde = entry['mainsnak']['datavalue']['value']['id']
                    result_values.append((entity, wde))
    if result_values:
        maindb.set_entities(result_values)


def find_properties(wdid, locale, altale):
    """ future feature """
    ignorelist = ['P19', 'P20', 'P21', 'P22', 'P25', 'P26', 'P27', 'P31', 'P40', 'P53', 'P91',
                  'P102', 'P103', 'P106', 'P119', 'P140', 'P172', 'P184', 'P185', 'P358', 'P451',  # 'P361',
                  'P511', 'P551', 'P552', 'P734', 'P735', 'P802', 'P859', 'P910',
                  'P1038', 'P1283', 'P1303', 'P1340', 'P1343', 'P1412', 'P1424', 'P1884', 'P1889',
                  'P1950', 'P2094', 'P2283', 'P2354', 'P3205', 'P3373', 'P3828',
                  'P5008', 'P6104', 'P6275', 'P6553', 'P6886', 'P7084', 'P7763', 'P8852']

    url = f'https://www.wikidata.org/w/api.php?' \
          f'action=wbgetclaims&format=json&entity={wdid}'
    is_good, r = please_request(url)

    if is_good:
        claims = r['claims']
        props = claims.keys()
        result_dict = {}  # notable properties
        reqs = []  # list of grequests
        propses = []  # ordered list of props
        bigdict = {}  # list of entities passed to grequests
        for prop in props:
            if prop not in ignorelist:
                entities = [prop, ]
                for entry in claims[prop]:
                    if 'datavalue' not in entry['mainsnak']:
                        elogger.warn(f" {prop} no value in {entry['mainsnak']}")
                        continue
                    entry_value = entry['mainsnak']['datavalue']['value']
                    if type(entry_value) == dict:
                        entity = entry_value.get('id', 0)
                        if entity:
                            entities.append(entity)

                if len(entities) > 1:
                    url = f'https://www.wikidata.org/w/api.php?props=labels&languages=en|{locale}|{altale}' \
                          f'&ids={"|".join(entities[:49])}&action=wbgetentities&format=json'
                    reqs.append(grequests.get(url))
                    propses.append(prop)
                    bigdict[prop] = entities[:49]

        if reqs:
            propindx = -1
            for request in grequests.map(reqs):
                if request.status_code == 200:
                    r = request.json()
                    if 'error' in r:
                        elogger.warn(f"!! {r['error']['code']} :: {r['error']['info']}")
                    else:
                        propindx += 1
                        prop = propses[propindx]
                        entities = bigdict[prop]
                        values = []
                        for entity in entities:
                            entry = r['entities'][entity]['labels']
                            loc_dict = {'en': None, 'ru': None, locale: None}
                            for loc in (locale, altale, 'en'):
                                if loc in entry:
                                    value = entry[loc]['value']
                                    loc_dict[loc] = value
                            tmp, value = get_notional_value(loc_dict, locale, altale)
                            if value not in values:
                                values.append(value)

                        if len(values):
                            result_dict[prop] = values
        return result_dict
