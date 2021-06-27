from flask import request, jsonify
import pprint
import json
import datetime
import hashlib
from app import app

# from app.forms import LoginForm, UserForm
from app.models import People, Occupations, Tags, Wdentities


def get_day():
    return datetime.datetime.now().strftime('%m.%d')


def get_tags(wdentity, lang):
    # generating tags list
    tags = Tags.query.filter_by(people_entity=wdentity).order_by(Tags._id)
    tags_str = ''
    emoji_list = []
    for tag in tags:
        occu_data = Occupations.query.filter_by(occu_entity=tag.occupation_entity)
        if occu_data.count():
            emoji_list.append(get_emoji_chars(occu_data[0].emoji))
            occu_descr = get_notional_value(occu_data[0].descr_cache, lang)
            occu_descr = occu_descr.replace(' ', '_').replace('/', '_').replace('-', '_')
            tags_str += f'#{occu_descr} '
        else:
            tags_str += f'#UNKNOWN_{tag.occupation_entity[1:]} '

    if not tags_str:
        tags_str = '--notags--'

    return tags_str, emoji_list


def get_describe(wdentity, lang):
    occu_descr = '--nodata--'
    descr_data = Wdentities.query.filter_by(wdentity=wdentity)
    if descr_data.count():
        occu_descr = get_notional_value(descr_data[0].descr_cache, lang)
    return occu_descr


def get_flag(wdentity):
    flag = '?'
    descr_data = Wdentities.query.filter_by(wdentity=wdentity)
    if descr_data.count():
        flag = descr_data[0].flag
    if flag == '?':
        flag = 'U+1F5FA'
    emoji_flag = get_emoji_chars(flag)
    return emoji_flag


def get_wc_thumb(photo, width=420):
    if not photo:
        return "https://conggratz.ru/stati/nophoto2.jpg"
    photo = photo.replace(' ', '_')
    m = hashlib.md5()
    m.update(photo.encode('utf-8'))
    d = m.hexdigest()
    result = 'https://upload.wikimedia.org/wikipedia/commons/thumb/' + \
             f'{d[0]}/{d[0:2]}/{photo}/{str(width)}px-{photo}'
    result = result.replace('"', '%22')
    if result[-3:] != 'jpg':
        result += '.jpg'
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

    data = People.query.filter_by(bdate=bdate). \
        order_by(People.bklinks.desc()).limit(limit).offset(offset)

    list_d = []
    a = 0
    for item in data:
        if item:
            list_d.append(item.__dict__)
        # else:
        #     print('noitem', a)
        # a += 1
    for item in list_d:
        links = json.loads(item['links'])
        name = links['ru']
        del item['_sa_instance_state']
        del item['links']
        del item['bdate']
        photo = get_wc_thumb(item['photo'])
        tags, emoji = get_tags(item['wdentity'], 'ru')
        descr = get_describe(item['wdentity'], 'ru')
        flag = get_flag(item['wdentity'])

        item.update({'tags': tags, 'name': name, 'photo': photo, 'descr': descr, 'emoji': emoji, 'flag': flag})

    # pp = pprint.PrettyPrinter(indent=4)
    # print (pp.pprint(list_d))

    resp = jsonify(list_d)
    # resp.status_code = 200
    return resp
