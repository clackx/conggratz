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
    tags = Tags.query.filter_by(people_entity=wdentity)
    tags_str = ''
    for tag in tags:
        occu = Occupations.query.filter_by(occu_entity=tag.occupation_entity)
        if occu.count():
            occu = occu[0]
            occu_descr = json.loads(occu[0].descr_cache).get(lang)
            if not occu_descr:
                occu_descr = json.loads(occu.descr_cache).get('en', f'? no en ?')
            occu_descr = occu_descr.replace(' ', '_').replace('/', '_').replace('-', '_')
            tags_str += f'#{occu_descr} '
        else:
            tags_str += f'#UNKNOWN_{tag.occupation_entity[1:]} '

    if not tags_str:
        tags_str = '--notags--'

    return tags_str


def get_describe(wdentity, lang):
    occu_descr = '--nodata--'
    descr_data = Wdentities.query.filter_by(wdentity=wdentity)
    if descr_data.count():
        descr = descr_data[0]
        occu_descr = json.loads(descr_data[0].descr_cache).get(lang)
        if not occu_descr:
            occu_descr = json.loads(descr.descr_cache).get('en', '--NO DATA--')
    return occu_descr


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
        tags = get_tags(item['wdentity'], 'ru')
        descr = get_describe(item['wdentity'], 'ru')

        item.update({'tags': tags, 'name': name, 'photo': photo, 'descr': descr})

    # pp = pprint.PrettyPrinter(indent=4)
    # print (pp.pprint(list_d))

    resp = jsonify(list_d)
    # resp.status_code = 200
    return resp
