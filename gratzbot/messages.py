from datetime import datetime
from babel.dates import format_skeleton

ENGLISH = 'en'
SLOVAK = 'sk'

MESSAGES = {
    'were born':
        {'ru': 'родились',
         'be': 'нарадзіліся',
         'uk': 'народилися',
         'kk': 'дүниеге келді',
         'en': 'were born',
         'de': 'wurden geboren',
         'es': 'nació',
         'fr': 'sont nés',
         'zh': '出生',
         'ko': '일생',
         'ja': '生まれた'
         },
    'language':
        {'ru': 'Язык',
         'be': 'Мова',
         'uk': 'Мова',
         'kk': 'Tіл',
         'de': 'Sprache',
         'es': 'Idioma',
         'fr': 'Langue',
         'zh': '語',
         'ko': '언어',
         'ja': '言語'
         },
    'keyboard':
        {'ru': 'Клавиатура',
         'be': 'Клавіятура',
         'uk': 'Клавіатура',
         'kk': 'Пернетақта',
         'de': 'Tastatur',
         'es': 'Teclado',
         'fr': 'Clavier',
         'zh': '鍵盤',
         'ko': '건반',
         'ja': 'キーボード'
         },
    'config':
        {'ru': 'Конфигурация',
         'be': 'Канфігурацыя',
         'uk': 'Конфігурації',
         'kk': 'Конфигурация',
         'de': 'Aufbau',
         'es': 'Configuración',
         'fr': 'Configuration',
         'zh': '配置',
         'ko': '구성',
         'ja': '構成'
         },
    'notifications':
        {'ru': 'Оповещения',
         'be': 'Апавяшчэння',
         'uk': 'Повідомлення',
         'kk': 'Хабарламалар',
         'de': 'Benachrichtigungen',
         'es': 'Notificaciones',
         'fr': 'Notifications',
         'zh': '通知',
         'ko': '알림',
         'ja': '通知'
         },
    'my favorites':
        {'ru': 'Мои лайки',
         'be': 'Мае любімыя',
         'uk': 'Мої улюблені',
         'kk': 'Менің сүйіктілерім',
         'de': 'Meine Favoriten',
         'es': 'Mis favoritos',
         'fr': 'Mes favoris',
         'zh': '我最喜歡的',
         'ko': '내가 좋아하는 것들',
         'ja': '私のお気に入り'
         },
    'type':
        {'ru': 'Тип',
         'be': 'Тыпу',
         'uk': 'Типу',
         'kk': 'Түрі',
         'de': 'Art',
         'es': 'Escribe',
         'fr': 'Taper',
         'zh': '類型',
         'ko': '유형',
         'ja': 'タイプ'
         },
    'number of keys':
        {'ru': 'Количество кнопок',
         'be': 'Колькасць клавіш',
         'uk': 'Кількість клавіш',
         'kk': 'Кілттер саны',
         'de': 'Anzahl der Schlüssel',
         'es': 'Número de llaves',
         'fr': 'Nombre de clés',
         'zh': '按鍵數',
         'ko': '키 수',
         'ja': 'キーの数'
         },
    'number of entries':
        {'ru': 'Количество записей',
         'be': 'Колькасць запісаў',
         'uk': 'Кількість записів',
         'kk': 'Жазбалар саны',
         'de': 'Anzahl der Einträge',
         'es': 'Número de registros',
         'fr': 'Nombre d''enregistrements',
         'zh': '記錄數',
         'ko': '레코드 수',
         'ja': 'レコード数'
         },
    'value of step':
        {'ru': 'Величина сдвига',
         'be': 'Значэнне зруху',
         'uk': 'Значення зсуву',
         'kk': 'Ауысым сомасы',
         'de': 'Wert der Verschiebung',
         'es': 'Cantidad de turno',
         'fr': 'Montant du décalage',
         'zh': '移位量',
         'ko': '시프트 금액',
         'ja': 'シフト量'
         },
    'P800':
        {'en': 'Notable works',
         'ru': 'Значимые работы',
         'be': 'Выдатныя творы',
         'uk': 'Визначний твори',
         'kk': 'Көрнекті жұмыстар',
         'de': 'Herausragende Werke',
         'es': 'Obras destacadas',
         'fr': 'œuvres remarquables',
         'zh': '主要作品',
         'ko': '대표 작품',
         'ja': '主要作品'
         },
    'set to':
        {'ru': 'Установлено',
         'be': 'Устаноўлена',
         'uk': 'Встановлено',
         'kk': 'Орнатылған',
         'de': 'Einstellen',
         'es': 'Ajustado a',
         'fr': 'Mis à',
         'zh': '设置',
         'ko': '로 설정',
         'ja': 'に設定'
         },
    'added to fav':
        {'ru': 'Добавлено в избранное',
         'be': 'Дададзены ў абранае',
         'uk': 'Додано до вибраного',
         'kk': 'Фавориттерге қосылды',
         'de': 'Zu Favoriten hinzugefügt',
         'es': 'Ya en favoritos',
         'fr': 'Ajouté aux favoris',
         'zh': '添加到收藏夹',
         'ko': '즐겨 찾기에 추가',
         'ja': 'お気に入りに追加'
         },
    'already in fav':
        {'ru': 'Уже в любимчиках',
         'be': 'Ужо ў абраным',
         'uk': 'Вже в обраному',
         'kk': 'Қазірдің өзінде фавориттерде',
         'de': 'Schon in Favoriten',
         'es': 'Añadido a favoritos',
         'fr': 'Déjà dans les favoris',
         'zh': '已经收藏',
         'ko': '이미 즐겨 찾기에',
         'ja': 'すでにお気に入りに'
         },
    'not found':
        {'ru': 'Не найдено',
         'be': 'Не знойдзена',
         'uk': 'Не знайдено',
         'kk': 'Табылмады',
         'de': 'Nicht gefunden',
         'es': 'Extraviado',
         'fr': 'Pas trouvé',
         'zh': '未找到',
         'ko': '찾을 수 없음',
         'ja': '見つかりません'
         },
    'ON':
        {'ru': 'Вкл'},
    'OFF':
        {'ru': 'Выкл'},
    'OK thanks, remember':
        {'ru': 'ОК спасибо, записал',
         'be': 'OK дзякуй, запісаў',
         'uk': 'OK спасибі, записав',
         'kk': 'Жарайды рахмет, деп жазды',
         'de': 'OK, danke, denk dran',
         'es': 'OK gracias, recuerda',
         'fr': 'OK merci, notez-le',
         'zh': '好，谢谢，写下来',
         'ko': '좋아, 적어',
         'ja': 'OKありがとう、書き留めた'
         },
    'yesterday':
        {'ru': 'Вчера',
         'be': 'Учора',
         'uk': 'Вчора',
         'kk': 'Кеше',
         'de': 'Gestern',
         'es': 'Ayer',
         'fr': 'Hier',
         'zh': '昨天',
         'ko': '어제',
         'ja': '昨日'
         },
    'today':
        {'ru': 'Сегодня',
         'be': 'Сёння',
         'uk': 'Сьогодні',
         'kk': 'Бүгін',
         'de': 'Heute',
         'es': 'Hoy dia',
         'fr': 'Aujourd''hui',
         'zh': '今天',
         'ko': '오늘',
         'ja': '今日'
         },
    'tomorrow':
        {'ru': 'Завтра',
         'be': 'Заўтра',
         'uk': 'Завтра',
         'kk': 'Ертең',
         'de': 'Morgen',
         'es': 'Mañana',
         'fr': 'Demain',
         'zh': '明天',
         'ko': '내일',
         'ja': '明日'
         },
    'another day':
        {'ru': 'Другой день',
         'be': 'Другі дзень',
         'uk': 'Інший день',
         'kk': 'Басқа күн',
         'de': 'Ein anderer Tag',
         'es': 'Otro día',
         'fr': 'Un autre jour',
         'zh': '另一天',
         'ko': '다른 날',
         'ja': '別の日'
         },
    'information':
        {'ru': 'Информация',
         'be': 'Iнфармацыя',
         'uk': 'Iнформація',
         'kk': 'Ақпарат',
         'de': 'Information',
         'es': 'Información',
         'fr': 'Informations',
         'zh': '信息',
         'ko': '정보',
         'ja': '情報'
         },
    'main menu':
        {'ru': 'Главное меню',
         'be': 'Галоўнае меню',
         'uk': 'Головне меню',
         'kk': 'Басты мәзір',
         'de': 'Hauptmenü',
         'es': 'Menú principal',
         'fr': 'Menu principal',
         'zh': '主菜单',
         'ko': '메인 메뉴',
         'ja': 'メインメニュー'
         },
    'edf':
        {'en': 'Enter a date in the format',
         'ru': 'Введите дату в формате',
         'be': 'Увядзіце дату ў фармаце',
         'uk': 'Введіть дату в форматі',
         'kk': 'Форматты күнді енгізіңіз',
         'de': 'Geben Sie das Datum im Format ein',
         'es': 'Ingrese la fecha en el formato',
         'fr': 'Entrez la date au format',
         'zh': '以格式输入日期',
         'ko': '형식으로 날짜를 입력하십시오',
         'ja': '形式で日付を入力します'
         },
    'greetz':
        {'en': "Greetz!\n Every day I can tell you about people who have made significant contributions to their field "
               "of activity.\n If you add someone to your favorites, I will notify you on his birthday eve so that you "
               "can remember his work and thank him with your attention.\n Over time, I will learn to carefully "
               "recommend you other people in your circle of interests that you may have forgotten or do not know "
               "about.\n If you find a mistake in translation, oddity in work or something caused your negative "
               "feelings, just mail about it.\n Hope for fruitful cooperation!",
         'ru': "Привет!\n Я могу рассказывать тебе каждый день о людях, которые внесли значительный вклад в свою "
               "область деятельности.\n Если ты добавишь кого-то в избранное, я буду оповещать тебя накануне дня его "
               "рождения, чтобы ты смог вспомнить о его трудах и отблагодарить своим вниманием.\n Со временем я "
               "научусь осторожно советовать тебе других людей твоего круга интересов, о которых ты мог забыть или "
               "не знаешь.\n Если ты нашёл ошибку в переводе, странность в работе или что-то вызвало твои негативные "
               "чувства, просто напиши об этом на почту.\n Надеюсь на плодотворное сотрудничество! "
         },
    'flags':
        {'RU': 'U+1F1F7 U+1F1FA',
         'BE': 'U+1F1E7 U+1F1FE',
         'UK': 'U+1F1FA U+1F1E6',
         'KK': 'U+1F1F0 U+1F1FF',
         'EN': 'U+1F1FA U+1F1F8',
         'DE': 'U+1F1E9 U+1F1EA',
         'ES': 'U+1F1EA U+1F1F8',
         'FR': 'U+1F1EB U+1F1F7',
         'ZH': 'U+1F1E8 U+1F1F3',
         'KO': 'U+1F1F0 U+1F1F7',
         'JA': 'U+1F1EF U+1F1F5',
         'CG': 'U+3297'}
}


def get_translation(message, locale):
    result = ''
    mess_dict = MESSAGES.get(message)
    if mess_dict:
        result = mess_dict.get(locale)
    if result:
        return result
    return message.capitalize()


def get_values(key):
    result = [key, ]
    for value in MESSAGES[key].values():
        result.append(value)
    return result


def get_dayname(bday, locale):
    return format_skeleton('MMMMd', datetime.strptime(bday+'.80', '%m.%d.%y'), locale=locale)
