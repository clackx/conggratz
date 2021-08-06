from flask import request, jsonify
import pprint
import json
import datetime
import hashlib
from app import app

from app.models import People, Occupations, Tags, Presorted, Countries, Flags


def get_day():
    return datetime.datetime.now().strftime('%m.%d')


def get_tags(wdentity, lang):
    # generating tags list
    tags_str = ''
    emoji_list = []
    occu_data = Occupations.query.join(Tags, Occupations.occu_entity == Tags.occupation_entity).filter_by(
        people_entity=wdentity)

    for occu_item in occu_data:
        emoji_list.append(get_emoji_chars(occu_item.emoji))
        occu_descr = get_notional_value(occu_item.descr_cache, lang)
        occu_descr = occu_descr.replace(' ', '_').replace('/', '_').replace('-', '_')
        tags_str += f'#{occu_descr} '

    if not tags_str:
        tags_str = '--notags--'

    emoji = '⁉️'
    if len(emoji_list):
        emoji = emoji_list[0]
        space = emoji.find(' ')
        if space != -1:
            emoji = emoji[:space]
        dash = emoji.find('-')
        if dash != -1:
            emoji = emoji[:dash]

    return [{'icon': emoji, 'tags': tags_str, 'emojis': emoji_list}]


def get_flags_and_countries(wdentity):
    res_emoji_flag = '-'
    res_countries = []
    res_flags = []
    flags = Flags.query.join(Countries, Countries.country_entity == Flags.country_entity).filter(
        Countries.people_entity == wdentity)

    for f in flags:
        res_flags.append(get_wc_thumb(f.svg_flag, width=256, frmt='png'))
        res_countries.append(f.country_name)

        if not res_emoji_flag:
            res_emoji_flag = f.emoji_flag

        if f.emoji_flag[0] == 'U':
            if res_emoji_flag[0] != 'U':
                res_emoji_flag = f.emoji_flag

        if f.emoji_flag[0] == '~':
            if res_emoji_flag[0] == '-':
                res_emoji_flag = f.emoji_flag

    return [{'icon': get_flag_emoji(res_emoji_flag),
             'svg_flags': res_flags, 'countries': res_countries, }]


def get_wc_thumb(photo, width=420, frmt='jpg'):
    if not photo:
        return "https://conggratz.ru/stati/nophoto2.jpg"
    photo = photo.replace(' ', '_')
    m = hashlib.md5()
    m.update(photo.encode('utf-8'))
    d = m.hexdigest()
    result = 'https://upload.wikimedia.org/wikipedia/commons/thumb/' + \
             f'{d[0]}/{d[0:2]}/{photo}/{str(width)}px-{photo}'
    result = result.replace('"', '%22')
    if result[-3:] != frmt:
        result += '.' + frmt
    return result


def get_emoji_chars(emojis):
    """ get emoji chars from unified hex notation """
    emores = ''
    if emojis:
        for emoji in emojis.split():
            emores += chr(int(emoji[2:], 16))
    else:
        emores += chr(128100)
    return emores


def get_flag_emoji(emojis):
    if emojis[0] == '-':
        return get_emoji_chars('U+1F5FA')
    if emojis[0] == '~':
        return get_emoji_chars(emojis[2:]) + '*'
    return get_emoji_chars(emojis)


def get_notional_value(data_str, locale):
    """ Get *locale* key value from cached *data_dict*
    If locale value is empty, get value of default 'en'
    If default value is empty, get first non-empty """
    data_dict = {}
    try:
        data_dict = json.loads(data_str)
    except json.decoder.JSONDecodeError as e:
        print('JSON decode error:', e)

    (key, value) = (locale, '--nodata--')
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
                    value = '-?nodata?-'
    return value


@app.route('/json')
def jsss():
    bdate = request.args.get('bdate', '01.01')
    limit = request.args.get('limit', 3)
    offset = request.args.get('offset', 0)
    lang = request.args.get('lang', 'en')

    data = Presorted.query.filter_by(bday=bdate).limit(limit).offset(offset)
    list_d = []
    for item in data:
        if item:
            list_d.append(item.__dict__)

    newdict = []
    for item in list_d:
        wdentity = item[f'{lang}wde']
        newdict.append({'wde': wdentity})
        person = People.query.filter_by(wdentity=wdentity).first()
        newdict.append({'links': person.links, 'descrs': person.descrs,
                        'photo': get_wc_thumb(person.photo)})
        newdict.append({'occupations': get_tags(wdentity, 'ru')})
        newdict.append({'countries': get_flags_and_countries(wdentity)})

    return jsonify(newdict)
