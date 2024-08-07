import aiohttp
import asyncio
import json
from datetime import datetime
from aiogram import types
from mdb import maindb
import user
import elogger
from misc import get_wc_thumb
from messages import get_translation, get_dayname
from config import admin_id
from aiohttp import client_exceptions


async def please_request(url, params=''):
    """ safe request *url* with *params* """
    elogger.enter(f'>< requesting {url} with {str(params)[:100]}')
    is_request_successful = False
    result = ''
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                result = await resp.json()
        is_request_successful = True
        if 'error' in result:
            is_request_successful = False
        elogger.exiter(f'[OK] {resp.status}', result)
    except aiohttp.client_exceptions.ClientConnectorError as err:
        await elogger.error(f'!! aiohttp ClientConnectorError: {err}')
    return is_request_successful, result


async def request_wiki_info(namelink, locale):
    """ request wikipedia for extracts intro (content before the first section)
    of page *namelink* on *locale* language """
    elogger.debug(f'----- request_wiki_info :: {namelink} @ {locale}')
    url = f"https://{locale}.wikipedia.org/w/api.php?action=query&format=json" \
          f"&prop=extracts&explaintext=1&exintro=1&titles={namelink}"
    is_request_successful, r = await please_request(url)
    if is_request_successful:
        pages = r['query']['pages']
        info = pages[list(pages)[0]]['extract']
        info = info.replace(chr(769), '')  # accent mark remove
        info = '\n\n '.join(info.split('\n'))
        info = info.rstrip()
        return info


async def get_notional_value(data_dict, locale, altale):
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
                    await elogger.datawarn(f'(dict) No data in {data_dict}')
    return key, value


async def get_universal(utypename, wdentities, locale, altale):
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

    unidata = await maindb.get_universal(utypename, wdentities)

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
                await elogger.datawarn(f'{wdentity} has no {key} in {utypename}')
                key, value = await get_notional_value(descr_dict, locale, altale)
                if not value:
                    await elogger.datawarn(f'{wdentity} has no description at all !!')
                    value = '--nodata--'

            result_dict[wdentity] = (key, value)

    elogger.exiter('[OK]', result_dict)
    return result_dict


async def get_tags(wdentity, locale, altale):
    """ get tags from db as list of pairs (entity, emoji code),
    get from universe description labels for all entities,
    compile result *emores* as emoji chars and description """
    elogger.enter(f'----- get_tags {wdentity} @ {locale}')
    await check_tags([wdentity, ])
    emojis_list = await maindb.get_tags(wdentity)
    entity_list = [en[0] for en in emojis_list]
    emoji_list = [em[1] for em in emojis_list]

    desc_dict = await get_universal('labels', entity_list, locale, altale)
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


async def get_info(wdid, locale, altale):
    """ get all stuff (tags, text and keyboard) for person info card """
    data = await get_universal('sitelinks', [wdid], locale, altale)
    key, namelink = data[wdid]
    info = await request_wiki_info(namelink, key)
    tags = await get_tags(wdid, locale, altale)
    text = f'<i>{tags}</i>\n\n{info}'
    if len(text) > 3896:
        text = text[:3896] + '...'
    keyboard = get_inline_keyboard(wdid, namelink, key)
    return text, keyboard


async def get_shift_params(userid, direction):
    """ get user session params for shift operation """
    kb = await user.load_param(userid, 'keyboard')
    step = kb.get('step')
    kbtype = kb.get('type')
    s = await user.load_param(userid, 'session')
    bday = s.get('bday')
    offset = s.get('offset') + direction * int(step)
    is_rested = False
    if offset < 0:
        offset = 0
        is_rested = True
    return bday, offset, is_rested, kbtype


async def get_day_plus(userid, bday, offset):
    """ get user session params to call *get_day_info* """
    elogger.enter(' ++++ MAIN')
    lcl = await user.load_param(userid, 'locale')
    locale = lcl.get('primary')
    altale = lcl.get('altern', 'en')
    keyboard = await user.load_param(userid, 'keyboard')
    count = keyboard.get('entries')
    buttons = keyboard.get('keys')
    kbtype = keyboard.get('type')
    debug = True if userid == admin_id else False
    text, names, entities = await get_day_info(bday, locale, altale, offset, count, debug)
    markup = get_keyboard(names, buttons, entities, kbtype, offset)
    elogger.exiter('[OK] MAIN', text)
    return text, markup, kbtype


async def get_day_info(bday, locale, altale, offset, count, debug=False):
    """ get full *bday* info with *count* entries from starting *offset*
     every entry contains name from namelist, tag (emoji + description)
     and short description from desclist """
    elogger.enter(f'----- get_today {bday}, {count} items')
    starttime = datetime.now()
    res_names = []
    res_text = f'{get_dayname(bday, locale)} {get_translation("were born", locale)}:\n\n'
    data = await maindb.get_day_intro(bday, locale, offset, count)
    entities = []
    for entity in data:
        if entity[0]:
            entities += entity
    if entities:
        namelist = await get_universal('sitelinks', entities, locale, altale)
        desclist = await get_universal('descriptions', entities, locale, altale)
        await check_tags(entities)
        data = await maindb.get_emojis(entities)
        tagdixt = {}
        for wde, emojis in data:
            emores = get_emoji_chars(emojis)
            tagdixt.setdefault(wde, '')
            tagdixt[wde] += emores + '•'
        for wdentity in entities:
            if wdentity:
                l_tmp, name = namelist[wdentity]
                l_tmp, desc = desclist[wdentity]
                flag = await get_person_flag(wdentity)
                tag = tagdixt.get(wdentity, chr(8265))
                ftag = get_first_emoji(tag)
                if tag == chr(8265):
                    await elogger.datawarn(f'{wdentity} ({name}) has no tags')
                res_names.append(name)
                res_text += f' {flag}{ftag} : : {name}\n{desc}\n\n'

    if int(count) > len(entities):
        res_text += '      ~~ endofdata ~~'

    endtime = datetime.now()
    stata = "<code>Spend {}s to request</code>".format((endtime - starttime).total_seconds())
    res_text += stata if debug else ''
    elogger.exiter('[OK] all great ', stata)
    return res_text, res_names, entities


def get_button(name, entity='', kbtype='regualr'):
    if kbtype == 'regular':
        button = types.KeyboardButton
        return button(text=name)
    else:
        button = types.InlineKeyboardButton
        return button(text=name, callback_data=f'info_{entity}')


def get_keyboard(names, buttons, entities, kbtype, offset):
    """ build keyboard markup from list of names and 2 nav buttons """
    elogger.debug(f'get_keyboard {str(names)[:100]}')

    is_odd = True if (len(names) % 2) != 0 else False
    is_end = False
    if len(names) < int(buttons):
        buttons = len(names) if not is_odd else len(names) - 1
        is_end = True

    buttons_list = []
    for i in range(0, int(buttons), 2):
        buttons_list.append([
            get_button(names[i], entities[i], kbtype),
            get_button(names[i + 1], entities[i + 1], kbtype)])

    if offset == 0:
        buttons_list.append([
            get_button('<<< Menu', 'menu', kbtype),
            get_button('FW >>>', 'fw', kbtype)])
    else:
        if not is_end:
            buttons_list.append([
                get_button('<<RW', 'rw', kbtype),
                get_button('FW>>', 'fw', kbtype)])
        else:
            if is_odd:
                buttons_list.append([
                    get_button(names[len(names)-1], entities[len(names)-1], kbtype),
                    get_button('<<RW', 'rw', kbtype)])
            else:
                buttons_list.append([get_button('<<RW', 'rw', kbtype)])

    if kbtype == 'regular':
        return types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons_list)
    else:
        return types.InlineKeyboardMarkup(inline_keyboard=buttons_list)


def get_inline_keyboard(wdid, name, locale):
    """ build inline keyboard markup with (so far) 2 buttons, Like and More.. """
    elogger.debug(f'get_inline_keyboard {wdid}')
    name = name.replace(u'\u2019', '%E2%80%99')
    info_btn = types.InlineKeyboardButton(text=u'\U0001F497' + " Like", callback_data=f'like_{wdid}')
    more_btn = types.InlineKeyboardButton(text=u'\U0001F9E0' + " More..", callback_data=f'more_{wdid}')
    wiki_btn = types.InlineKeyboardButton(text=u'\U0001F310' + " Wiki",
                                          url=f'https://{locale}.m.wikipedia.org/wiki/{name}')
    return types.InlineKeyboardMarkup(inline_keyboard=[[info_btn, more_btn, wiki_btn]])


async def get_photo_link(wdid):
    """ query photo entry and generate full wikimedia link """
    elogger.enter(f'----- get_photo_link {wdid}')
    photo = await maindb.get_photo(wdid)
    result = get_wc_thumb(photo)
    elogger.exiter(f'[OK] get_photo_link', result)
    return result


async def get_acc_info(userid):
    """ get user settings localized info """
    lcl = await user.load_param(userid, 'locale')
    locale = lcl.get('primary')
    altale = lcl.get('altern', 'en')
    keyb = await user.load_param(userid, 'keyboard')
    tm = await user.load_param(userid, 'time')
    nttm = tm.get('notitime') if tm else '??:??'
    tmzn = tm.get('timezone') if tm else '??'
    spaces = len(get_translation('number of entries', locale)) + 1
    res_str = f"{get_translation('config', locale)}:\n"
    res_str += f"<code>{(get_translation('language', locale) + ':').ljust(spaces)}  " \
               f"{locale}  {get_flag(locale, flagonly=True)}\n"
    res_str += f"╰{(get_translation('language', altale) + ' ALT :').ljust(spaces)} " \
               f"{altale}  {get_flag(altale, flagonly=True)} \n"
    res_str += f"{get_translation('keyboard', locale)}:\n"
    res_str += f"├{(get_translation('type', locale) + ':').ljust(spaces)} {keyb.get('type')} \n"
    res_str += f"├{(get_translation('number of keys', locale) + ':').ljust(spaces)} {keyb.get('keys')} \n"
    res_str += f"├{(get_translation('number of entries', locale) + ':').ljust(spaces)} {keyb.get('entries')} \n"
    res_str += f"╰{(get_translation('value of step', locale) + ':').ljust(spaces)} {keyb.get('step')}\n"
    res_str += f"{(get_translation('notitime', locale)+ ':')}  {nttm} GMT{tmzn}\n</code>"
    return res_str


async def get_all_fav(userid):
    """ get all entries of favorites """
    elogger.enter(f'----- get_all_fav {userid}')
    lcl = await user.load_param(userid, 'locale')
    locale = lcl.get('primary')
    altale = lcl.get('altern', 'en')
    kb = await user.load_param(userid, 'keyboard')
    kbtype = kb.get('type')
    result = ''
    data = await maindb.get_allfav(userid)
    wdentities = [d[0] for d in data]
    if wdentities:
        data = await get_universal('sitelinks', wdentities, locale, altale)
        result = '' if kbtype == 'regular' else get_translation('my favorites', locale) + ':\n'
        for wdid in wdentities:
            result += f'• {data[wdid][1]}\n'
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


async def get_person_flag(wdentity):
    elogger.enter(f'^^ get_person_flag of {wdentity}')
    flags = await maindb.get_flags(wdentity)
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


async def check_tags(entities):
    """ It has been added in final stage and breaks some logic
    Returns nothing, but requests and stores absent tags """
    data = await maindb.get_entities(entities)
    data_list = [d[0] for d in data]
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
            is_good, r = await please_request(url)
            if is_good and r['claims']:
                for entry in r['claims']['P106']:
                    wde = entry['mainsnak']['datavalue']['value']['id']
                    result_values.append((entity, wde))
    if result_values:
        await maindb.set_entities(result_values)


async def find_properties(wdid, locale, altale):
    """ get a set of statements from Wikidata and its translation """

    ignorelist = ['P19', 'P20', 'P21', 'P22', 'P25', 'P26', 'P27', 'P31', 'P40', 'P53', 'P91',
                  'P102', 'P103', 'P106', 'P119', 'P140', 'P172', 'P184', 'P185', 'P358', 'P451',  # 'P361',
                  'P511', 'P551', 'P552', 'P734', 'P735', 'P802', 'P859', 'P910',
                  'P1038', 'P1283', 'P1303', 'P1340', 'P1343', 'P1412', 'P1424', 'P1884', 'P1889',
                  'P1950', 'P2094', 'P2283', 'P2354', 'P3205', 'P3373', 'P3828',
                  'P5008', 'P6104', 'P6275', 'P6553', 'P6886', 'P7084', 'P7763', 'P8852']

    url = f'https://www.wikidata.org/w/api.php?' \
          f'action=wbgetclaims&format=json&entity={wdid}'
    is_good, r = await please_request(url)

    if is_good:
        session = aiohttp.ClientSession()
        claims = r['claims']
        props = claims.keys()
        result_dict = {}  # notable properties
        reqs = []  # list of aiohttp requests
        propses = []  # ordered list of props
        bigdict = {}  # list of entities passed to grequests

        """ Social media links """
        idents_res = ''
        idents = {'P2397': ('▶ YT','https://www.youtube.com/channel/'),
                  'P2013': ('🐦 tw', 'https://twitter.com/'),
                  'P2003': ('📷 IG', 'https://www.instagram.com/'),
                  'P3185': ('✌ VK', 'https://vk.com/'),
                  'P2002': ('👤 FB', 'https://www.facebook.com/'),
                  'P2604': ('🎞 KP', 'https://www.kinopoisk.ru/name/'),
                  'P345': ('🗃 IMDB', 'https://www.imdb.com/name/'),
                  'P2949': ('🌲 WikiTree', 'https://www.wikitree.com/wiki/'),
                  }

        for prop in idents:
            if prop in props:
                value = claims[prop][0]['mainsnak']['datavalue']['value']
                result = f"{idents[prop][0]} : : <a href='{idents[prop][1]}{value}'>"
                if prop in ('P2397', 'P2604'):
                    result += '(channel)</a>'
                else:
                    result += f'{value}</a>'
                idents_res += result+'\n'

        sites = {'P856': '🌐 site', 'P1581': '🌐 blog'}
        for prop in sites:
            if prop in props:
                value = claims[prop][0]['mainsnak']['datavalue']['value']
                result = f"{sites[prop]} : : {value}"
                idents_res += result + '\n'

        idents_res += f"WikiData : : <a href='https://www.wikidata.org/wiki/{wdid}'>{wdid}</a>"
        result_dict['Q1'] = [get_translation('external', locale), idents_res]

        """ Other props (statements) """
        photos = {}
        for prop in props:
            if prop not in ignorelist:
                entities = [prop, ]
                for entry in claims[prop]:
                    if 'datavalue' not in entry['mainsnak']:
                        await elogger.datawarn(f"{prop} no value in {entry['mainsnak']}")
                        continue
                    entry_value = entry['mainsnak']['datavalue']['value']
                    datatype = entry['mainsnak']['datatype']

                    if datatype == 'wikibase-item':
                        entity = entry_value.get('id', 0)
                        if entity:
                            entities.append(entity)

                    elif datatype == 'monolingualtext':
                        loc_name = f" {entry_value.get('text')} ({entry_value.get('language')})"
                        result_dict['Q0'] = [get_translation('localname', locale), loc_name]

                    else:
                        if datatype != 'external-id':
                            #print(prop, '::>', entry['mainsnak']['datatype'], entry['mainsnak']['datavalue'], '\n\n')
                            pass

                    if prop == 'P18':
                        jpg = get_wc_thumb(entry_value, width=800)
                        link = f'<a href="{jpg}">&#8205;</a>'
                        idx = str(len(photos.keys()))
                        photos['Foto'+idx] = ['Foto '+idx, link]

                if len(entities) > 1:
                    url = f'https://www.wikidata.org/w/api.php?props=labels&languages=en|ru|{locale}|{altale}' \
                          f'&ids={"|".join(entities[:49])}&action=wbgetentities&format=json'
                    reqs.append(asyncio.ensure_future(session.get(url)))
                    propses.append(prop)
                    bigdict[prop] = entities[:49]

        """ Get translation of prop values based on locale """
        if reqs:
            requests = await asyncio.gather(*reqs)
            propindx = -1
            for request in requests:
                if request.status == 200:
                    r = await request.json(content_type=None)
                    propindx += 1
                    prop = propses[propindx]
                    if 'error' in r:
                        await elogger.datawarn(f"{prop} prop of {wdid} :: {r['error']['code']} : {r['error']['info']}")
                    else:
                        entities = bigdict[prop]
                        values = []
                        for entity in entities:
                            if 'labels' not in r['entities'][entity]:
                                loc_dict = {'en': '(deleted)', 'ru': '(удалено)'}
                            else:
                                entry = r['entities'][entity]['labels']
                                loc_dict = {'en': None, 'ru': None, locale: None}
                                for loc in (locale, altale, 'en', 'ru'):
                                    if loc in entry:
                                        value = entry[loc]['value']
                                        loc_dict[loc] = value
                            tmp, value = await get_notional_value(loc_dict, locale, altale)
                            if value not in values:
                                values.append(value)

                        if len(values):
                            result_dict[prop] = values
        await session.close()

        photos.pop('Foto0', None)
        result_dict.update(photos)

        return result_dict
