from flask import request, jsonify, render_template, send_from_directory, make_response
import os
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
    full_list = []
    occu_data = Occupations.query.join(
        Tags, Occupations.occu_entity == Tags.occupation_entity).filter_by(
        people_entity=wdentity)

    for occu_item in occu_data:
        occu_emoji = get_emoji_chars(occu_item.emoji)
        occu_descr = normalize(occu_item.descr_cache)

        for descr in occu_descr:
            if occu_descr[descr]:
                occu_descr[descr].replace(
                    ' ', '_').replace('/', '_').replace('-', '_')
        emoji_list.append(occu_emoji)
        full_list.append((occu_item.occu_entity, occu_descr, occu_emoji))
        tags_str += f'#{occu_descr[lang]} {get_emoji_chars(occu_item.emoji)} '

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

    return {'icon': emoji, 'tags': tags_str, 'list': full_list}


def get_flags_and_countries(wdentity):
    res_emoji_flag = '-'
    res_countries = []
    res_flags = []
    fc_list = []
    flags = Flags.query.join(
        Countries, Countries.country_entity == Flags.country_entity).filter(
        Countries.people_entity == wdentity)

    for f in flags:
        flag_img = get_wc_thumb(f.svg_flag, width=256, frmt='png')
        res_flags.append(flag_img)
        res_countries.append(f.country_name)
        fc_list.append((f.country_name, flag_img))

        if not res_emoji_flag:
            res_emoji_flag = f.emoji_flag

        if f.emoji_flag[0] == 'U':
            if res_emoji_flag[0] != 'U':
                res_emoji_flag = f.emoji_flag

        if f.emoji_flag[0] == '~':
            if res_emoji_flag[0] == '-':
                res_emoji_flag = f.emoji_flag

    return {'icon': get_flag_emoji(res_emoji_flag), 'fc_list': fc_list,
            'svg_flags': res_flags, 'countries': res_countries, }


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


def normalize(data_str, capitalize=False):
    languages = ('en', 'ru', 'es', 'zh', 'kk', 'be',
                 'uk', 'fr', 'de', 'ko', 'ja', 'it')
    result_dict = {key: '--nodata--' for key in languages}

    data_dict = {}
    try:
        data_dict = json.loads(data_str)
    except json.decoder.JSONDecodeError as e:
        print('JSON decode error:', e)

    if data_dict:
        key_lat = 'en'
        key_cyr = 'ru'

        default_lat = data_dict.get(key_lat)
        default_cyr = data_dict.get(key_cyr)

        if not default_lat:
            key_lat = list(data_dict.keys())[0]
            default_lat = data_dict.get(key_lat)

        if not default_cyr:
            key_cyr = key_lat
            default_cyr = default_lat

        if capitalize:
            default_lat = f'*{default_cyr.capitalize()}'
            default_cyr = f'*{default_cyr.capitalize()}'
        else:
            default_lat = f'*{default_lat} ({key_lat})'
            default_cyr = f'*{default_cyr} ({key_cyr})'

        result_dict = {key: default_lat for key in languages}
        result_dict.update(
            {key: default_cyr for key in ('ru', 'uk', 'be', 'kk')})
        for key in data_dict:
            if data_dict[key]:
                if capitalize:
                    result_dict[key] = data_dict[key].capitalize()
                else:
                    result_dict[key] = data_dict[key]

    return result_dict


@app.route('/json')
def jsss():
    bdate = request.args.get('bdate', '01.01')
    limit = request.args.get('limit', 3)
    offset = request.args.get('offset', 0)
    lang = request.args.get('lang', 'en')

    alldata = Presorted.query.filter_by(bday=bdate).filter(
        getattr(Presorted, f'{lang}wde') != None)
    data = alldata.limit(limit).offset(offset)
    list_d = []
    for item in data:
        if item:
            list_d.append(item.__dict__)

    results = []
    for item in list_d:
        wdentity = item[f'{lang}wde']
        pgvwrank = item[f'{lang}rank']
        person = People.query.filter_by(wdentity=wdentity).first()
        results.append({'wde': wdentity, 'rank': pgvwrank,
                        'links': normalize(person.links),
                        'descrs': normalize(person.descrs, capitalize=True),
                        'photo': get_wc_thumb(person.photo),
                        'occupations': get_tags(wdentity, lang),
                        'countries': get_flags_and_countries(wdentity)})

    response = make_response(jsonify(results))
    response.headers["X-Total-Count"] = alldata.count()
    return response


@app.route('/stati/<path:filename>')
def sttc(filename):
    basedir = os.path.abspath(os.path.dirname(__file__))
    return send_from_directory(basedir + '/static/', filename)


@app.route('/people')
def day():
    bdate = request.args.get('bdate', get_day())
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    lang = request.args.get('lang', 'ru')

    alldata = Presorted.query.filter_by(bday=bdate)
    counts = alldata.count()
    data = alldata.limit(limit).offset(offset)
    counts_str = f'{offset}-{offset+limit} из {counts}'
    link = f'people?bday={bdate}&lang={lang}&limit={limit}'
    next = offset + limit if offset + limit < counts else offset
    prev = offset - limit if offset - limit >= 0 else 0
    dict = {
        'link_fw': link + f'&offset={next}',
        'link_rw': link + f'&offset={prev}',
        'counts_str': counts_str,
        'lang': lang,
        'bdate': bdate
    }

    list_d = []
    for item in data:
        if item:
            list_d.append(item.__dict__)

    results = []
    for item in list_d:
        wdentity = item[f'{lang}wde']
        pgvwrank = item[f'{lang}rank']
        person = People.query.filter_by(wdentity=wdentity).first()
        results.append({'wde': wdentity, 'rank': pgvwrank,
                        'links': normalize(person.links)[lang],
                        'descrs': normalize(person.descrs, capitalize=True),
                        'photo': get_wc_thumb(person.photo),
                        'occupations': get_tags(wdentity, lang),
                        'countries': get_flags_and_countries(wdentity)})

    return render_template('people.html', data=results, dict=dict)


@app.route('/entity/<wdentity>')
def wde(wdentity):
    lang = request.args.get('lang', 'ru')

    p = People.query.filter_by(wdentity=wdentity)[0]

    descrs = {'en': None, 'ru': None}
    descrs.update(json.loads(p.descrs))
    data = {'name': p.name,
            'wdentity': wdentity,
            'tags': get_tags(wdentity, lang)['tags'],
            'countries': get_flags_and_countries(wdentity),
            'photo': get_wc_thumb(p.photo),
            'descrs': descrs,
            'links': json.loads(p.links),
            }

    dict = {'lang': lang,
            'link': data['links'].get(lang)}

    return render_template('entity.html', data=data, dict=dict)


@app.route('/tag/<wdentity>')
def tag(wdentity):
    limit = int(request.args.get('limit', 7))
    offset = int(request.args.get('offset', 0))
    lang = request.args.get('lang', 'ru')

    tags = Tags.query.with_entities(Tags.people_entity).filter_by(
        occupation_entity=wdentity)

    persons = People.query.filter(People.wdentity.in_(tags)).order_by(
        People.qrank.desc()).limit(limit).offset(offset)

    counts = tags.count()
    counts_str = f'{offset}-{offset+limit} из {counts}'
    link = f'{wdentity}?lang={lang}&limit={limit}'
    next = offset + limit if offset + limit < counts else offset
    prev = offset - limit if offset - limit >= 0 else 0

    dict = {
        'link_fw': link + f'&offset={next}',
        'link_rw': link + f'&offset={prev}',
        'counts_str': counts_str,
        'lang': lang,
    }

    results = []
    for person in persons:
        wdentity = person.wdentity
        results.append({'wde': person.wdentity, 'rank': person.qrank,
                        'links': normalize(person.links)[lang],
                        'descrs': normalize(person.descrs, capitalize=True),
                        'photo': get_wc_thumb(person.photo),
                        'occupations': get_tags(wdentity, lang),
                        'countries': get_flags_and_countries(wdentity)})

    return render_template('people.html', data=results, dict=dict)
