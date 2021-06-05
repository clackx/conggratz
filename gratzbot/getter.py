import requests
import json
from datetime import datetime
from telebot import types
import mdb
import user
import elogger
from misc import get_wc_thumb
from messages import get_translation, get_dayname
from config import admin_id

maindb = mdb.Mdb()


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


def requestmany(prop_type, entities, locale):
    """ Can request multiple entities of the same props type in chosen locale:
    'labels' refers name of entity, 'descriptions' treats as short description
    and 'sitelinks' returns wiki page title/name, sometimes similar to 'label' """
    elogger.enter(f'** requestmany {str(entities)} {prop_type} {locale}')
    url = 'https://www.wikidata.org/w/api.php'
    params = {
        'props': prop_type,
        'languages': f'en|ru|{locale}',
        'ids': '|'.join(entities),
        'sitefilter': f'enwiki|ruwiki|{locale}wiki',
        'action': 'wbgetentities',
        'format': 'json'
    }
    is_good, r = please_request(url, params)

    values = []
    if is_good:
        if 'error' in r:
            elogger.warn(f"!! {r['error']['code']} :: {r['error']['info']}")
        else:
            for entity in entities:
                # creating list of dictionaries
                entry = r['entities'][entity][prop_type]

                res_dict = {'en': None, 'ru': None, locale: None}
                for key in (locale, 'en', 'ru'):
                    if prop_type == 'sitelinks':
                        keyname = key + 'wiki'
                        fieldname = 'title'
                    else:
                        keyname = key
                        fieldname = 'value'

                    if keyname in entry:
                        value = entry[keyname][fieldname]
                        res_dict.update({key: value})

                values.append(res_dict)

    elogger.exiter('[OK]', str(values))
    return values


def get_notional_value(data_dict, locale):
    """ Get *locale* key value from cached *data_dict*
    If locale value is empty, get value of default 'en'
    If default value is empty, get first non-empty """
    (key, value) = (locale, None)
    if len(data_dict):
        value = data_dict.get(key)
        if not value:
            key = 'en'
            value = data_dict.get(key)
            if not value:
                for key in data_dict.keys():
                    value = data_dict[key]
                    if value:
                        break
                if not value:
                    elogger.warn(f'No data in {data_dict}')
    return key, value


def get_universal(utypename, wdentities, locale):
    """ most complicated function
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
            if locale in descr_dict:
                # если ключ есть, реквест не нужен
                key = locale
                value = descr_dict[locale]
                if not value:
                    elogger.warn(f'{wdentity} has no {key} in {descr_dict}')
                    key, value = get_notional_value(descr_dict, locale)
                    if not value:
                        elogger.warn(f'{wdentity} has no description at all !!')
                        value = '?? N/A ??'

                result_dict[wdentity] = (key, value)

    entities_to_request = []
    for wdentity in wdentities:
        if result_dict[wdentity] == (None, None):
            entities_to_request.append(wdentity)

    if len(entities_to_request):
        elogger.debug('Need to request: ' + str(entities_to_request))
        rlist = requestmany(utypename, entities_to_request, locale)
        if rlist:
            for i in range(0, len(entities_to_request)):
                wdentity = entities_to_request[i]
                full_dict[wdentity].update(rlist[i])

                new_json = json.dumps(full_dict[wdentity], ensure_ascii=False)
                maindb.set_universal(utypename, wdentity, new_json)

                key, value = get_notional_value(full_dict[wdentity], locale)
                result_dict[wdentity] = (key, value)

    elogger.exiter('[OK]', result_dict)
    return result_dict


def get_tags(wdentity, locale):
    """ get tags from db as list of pairs (entity, emoji code),
    get from universe description labels for all entities,
    compile result *emores* as emoji chars and description """
    elogger.enter(f'----- get_tags {wdentity} @ {locale}')
    check_tags([wdentity, ])
    emojis_list = maindb.get_tags(wdentity)
    entity_list = [en[0] for en in emojis_list]
    emoji_list = [em[1] for em in emojis_list]

    desc_dict = get_universal('labels', entity_list, locale)
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


def get_info(wdid, locale):
    """ get all stuff (tags, text and keyboard) for person info card """
    key, namelink = get_universal('sitelinks', [wdid], locale)[wdid]
    info = request_wiki_info(namelink, key)
    tags = get_tags(wdid, locale)
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
    keyboard = user.load_param(userid, 'keyboard')
    count = keyboard.get('entries')
    buttons = keyboard.get('keys')
    debug = True if userid == admin_id else False
    text, names = get_day_info(bday, locale, offset, count, debug)
    keyboard = get_keyboard(names, buttons)
    elogger.exiter('[OK] MAIN', text)
    return text, keyboard


def get_day_info(bday, locale, offset, count, debug=False):
    """ get full *bday* info with *count* entries from starting *offset*
     every entry contains name from namelist, tag (emoji + description)
     and short description from desclist """
    elogger.enter(f'----- get_today {bday}, {count} items')
    starttime = datetime.now()

    res_text = f'{get_dayname(bday, locale)} {get_translation("were born", locale)}:\n\n'
    data = maindb.get_day_intro(bday, offset, count)
    entities = sum(data, ())
    namelist = get_universal('sitelinks', entities, locale)
    desclist = get_universal('descriptions', entities, locale)

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
        tag = tagdixt.get(wdentity, chr(8265))
        if tag == chr(8265):
            elogger.warn(f'{wdentity} ({name}) has no tags')
        res_names.append(name)
        res_text += f' : : {name} : : {tag[:-1]}\n{desc}\n\n'

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
    wdentities = sum(maindb.get_allfav(userid), ())
    data = get_universal('sitelinks', wdentities, locale)
    result = ''
    for wdid in wdentities:
        result += data[wdid][1] + '\n'
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


def find_properties(wdid, locale):
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
        notable_props = []
        result_dict = {}
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
                    worklist = requestmany('labels', entities[:49], locale)
                    if worklist:
                        values = []
                        for work in worklist:
                            key, value = get_notional_value(work, locale)
                            if value not in values:
                                values.append(value)
                        if len(values):
                            result_dict[prop] = values
                            notable_props.append(prop)

        return notable_props, result_dict
