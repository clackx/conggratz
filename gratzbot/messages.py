from datetime import datetime
from babel.dates import format_skeleton

MESSAGES = {
    'were born':
        {'ru': 'родились',
         'be': 'нарадзіліся',
         'uk': 'народилися',
         'kk': 'туғандар',
         'en': 'were born',
         'de': 'wurden geboren',
         'es': 'nació',
         'it': 'nacquero',
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
         'it': 'Lingua',
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
         'it': 'Tastiera',
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
         'it': 'Configurazione',
         'en': 'Configuration',
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
         'it': 'Avvisi',
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
         'it': 'I miei preferiti',
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
         'it': 'Tipo',
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
         'it': 'Numero di pulsanti',
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
         'it': 'Numero di record',
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
         'it': 'Importo spostamento',
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
         'it': 'Lavoro significativo',
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
         'it': 'Installato',
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
         'it': 'Aggiunto ai preferiti',
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
         'it': 'Già nei preferiti',
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
         'it': 'Non trovato',
         'zh': '未找到',
         'ko': '찾을 수 없음',
         'ja': '見つかりません'
         },
    'ON':
        {'ru': 'Вкл',
         'it': 'Su',
         },
    'OFF':
        {'ru': 'Выкл',
         'it': 'Spento'
         },
    'OK thanks, remember':
        {'ru': 'ОК спасибо, записал',
         'be': 'OK дзякуй, запісаў',
         'uk': 'OK спасибі, записав',
         'kk': 'Жарайды рахмет, деп жазды',
         'de': 'OK, danke, denk dran',
         'es': 'OK gracias, recuerda',
         'fr': 'OK merci, notez-le',
         'it': 'Ok grazie, scrivilo',
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
         'it': 'Ieri',
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
         'es': 'Hoy',
         'fr': 'Aujourd''hui',
         'it': 'Oggi',
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
         'it': 'Domani',
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
         'it': 'Un altro giorno',
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
         'it': 'Informazione',
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
         'it': 'Menu principale',
         'zh': '主菜单',
         'ko': '메인 메뉴',
         'ja': 'メインメニュー'
         },
    'about':
        {'ru': 'О',
         'be': 'Пра',
         'uk': 'Про',
         'kk': 'Туралы',
         'de': 'Über',
         'es': 'Sobre',
         'fr': 'À propos',
         'it': 'Di',
         'zh': '关于',
         'ko': '약',
         'ja': '約'
         },
    'help':
        {'ru': 'Помощь',
         'be': 'Дапамога',
         'uk': 'Допомога',
         'kk': 'Көмек',
         'de': 'Helfen',
         'es': 'Ayuda',
         'fr': 'Aider',
         'it': 'Aiuto',
         'zh': '帮助',
         'ko': '돕다',
         'ja': 'ヘルプ'
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
         'it': 'Inserisci la data nel formato',
         'zh': '以格式输入日期',
         'ko': '형식으로 날짜를 입력하십시오',
         'ja': '形式で日付を入力します'
         },
    'review':
        {'ru': 'Отзыв',
         'be': 'Агляд',
         'uk': 'Огляд',
         'kk': 'Шолу',
         'de': 'Rezension',
         'es': 'Revisar',
         'fr': 'Revoir',
         'it': 'Recensione',
         'zh': '审查',
         'ko': '리뷰',
         'ja': 'レビュー'
         },
    'grateful':
        {'en': 'I would be grateful for honest feedback',
         'ru': 'Буду благодарен за честный отзыв',
         'be': 'Буду ўдзячны за сумленны агляд',
         'uk': 'Буду вдячний за чесний огляд.',
         'kk': 'Мен шынайы шолуға ризашылығымды білдіремін',
         'de': 'Ich wäre dankbar für ehrliches Feedback',
         'es': 'Agradecería una revisión honesta',
         'fr': 'Je serais reconnaissant pour vos commentaires honnêtes',
         'it': 'Sarei grato per una recensione onesta',
         'zh': '真诚的反馈我将不胜感激',
         'ko': '솔직한 피드백에 감사드립니다',
         'ja': '正直なフィードバックをいただければ幸いです'
         },
    'prehelp': {
        'en': 'CHANGE LANGUAGE /lang \n'
              '🇷🇺 ru  🇺🇸 en  🇪🇸 es  🇩🇪 de  🇮🇹 it  🇫🇷 fr \n🇧🇾 be  🇺🇦 uk  🇰🇿 kk  🇰🇷 ko  🇯🇵 ja  🇨🇳 zh \n'
              ' Если твой язык русский, отправь ru или RU.\n Также язык можно выбрать в настройках /sets.\n'
              ' Главное меню вызывается по команде /menu, помощь /help',
        'ru': 'CHANGE LANGUAGE /lang \n'
              '🇺🇸 en  🇪🇸 es  🇩🇪 de  🇮🇹 it  🇫🇷 fr  🇷🇺 ru \n🇧🇾 be  🇺🇦 uk  🇰🇿 kk  🇯🇵 ja  🇰🇷 ko 🇨🇳 zh \n'
              ' If Russian is not your native language, send en or EN\n Аlso languages can be selected in '
              'the settings /sets.\nThe main menu is called by the command /menu, help by /help'
        },
    'locale':
        {"en": "choose main locale",
         "ru": "выберите основную локаль",
         "be": "выберыце асноўную лакаль",
         "uk": "виберіть основну локаль",
         "kk": "Тілді негізгі таңдаңыз",
         "de": "wählen Sie das primäre Gebietsschema",
         "fr": "choisissez votre langue principale",
         "es": "elija la lingua principale",
         "it": "scegli la lingua primaria",
         "zh": "选择您的主要语言",
         "ko": "기본 언어를 선택하십시오",
         "ja": "あなたの第一言語を選択してください"},
    'altale':
        {"en": "choose alternative locale",
         "ru": "выберите альтернативную локаль",
         "be": "выберыце альтэрнатыўную лакаль",
         "uk": "виберіть альтернативну локаль",
         "kk": "Тілді балама таңдаңыз",
         "de": "wählen Sie ein alternatives Gebietsschema",
         "fr": "choisir la langue alternative",
         "es": "elige la lingua alternativa",
         "it": "scegli la lingua alternativa",
         "zh": "选择替代语言",
         "ko": "대체 언어를 선택",
         "ja": "代替言語を選択してください"},
    'flags':
        {'RU': 'U+1F1F7 U+1F1FA',
         'BE': 'U+1F1E7 U+1F1FE',
         'UK': 'U+1F1FA U+1F1E6',
         'KK': 'U+1F1F0 U+1F1FF',
         'EN': 'U+1F1FA U+1F1F8',
         'DE': 'U+1F1E9 U+1F1EA',
         'ES': 'U+1F1EA U+1F1F8',
         'FR': 'U+1F1EB U+1F1F7',
         'IT': 'U+1F1EE U+1F1F9',
         'ZH': 'U+1F1E8 U+1F1F3',
         'KO': 'U+1F1F0 U+1F1F7',
         'JA': 'U+1F1EF U+1F1F5',
         'CG': 'U+3297'},
    'tour0': {
        'be': 'Прывітанне!\n'
              'Я буду расказваць табе кожны дзень пра людзей, якія ўнеслі значны ўклад у сваю вобласць дзейнасці.\n'
              'Калі табе захочацца павіншаваць кагосьці, ты можаш проста падарыць свой час яго працам:\n'
              'напрыклад, паглядзець фільм з гэтым акцёрам, паслухаць альбом музыканта, прачытаць вершы паэта, пазнаёміцца \u200b\u200bз працамі вучонага.',
        'de': 'Grüß Gott!\n'
              'Ich werde Ihnen jeden Tag von Menschen berichten, die in ihren jeweiligen Bereichen einen wichtigen Beitrag geleistet haben.\n'
              'Wenn Sie jemandem gratulieren möchten, können Sie ihm einfach Ihre Zeit widmen: \n'
              'Sehen Sie sich zum Beispiel einen Film mit diesem Schauspieler an, hören Sie sich das Album eines Musikers an, lesen Sie die Gedichte eines Dichters, machen Sie sich mit den Schriften eines '
              'Wissenschaftlers vertraut.',
        'en': 'Greetz!\n'
              "I'll be telling you every day about people who have made significant contributions to their respective fields.\n"
              'If you would like to congratulate someone, you can simply give your time to their labors: \n'
              "for example, watch a movie with that actor, listen to a musician's album, read a poet's poems, get acquainted with a scientist's writings.",
        'es': '¡Saludos!\n'
              'Cada día os hablaré de personas que han hecho importantes contribuciones en sus respectivos campos.\n'
              'Si quieres felicitar a alguien, puedes simplemente dedicar tu tiempo a su labor: \n'
              'por ejemplo, ver una película con ese actor, escuchar el disco de un músico, leer los poemas de un poeta, conocer los escritos de un científico.',
        'fr': 'Salutations !\n'
              'Chaque jour, je vous parlerai de personnes qui ont apporté une contribution importante à leurs domaines respectifs.\n'
              "Si vous souhaitez féliciter quelqu'un, vous pouvez tout simplement consacrer votre temps à ses travaux : \n"
              "par exemple, regarder un film avec cet acteur, écouter l'album d'un musicien, lire les poèmes d'un poète, prendre connaissance des écrits d'un scientifique.",
        'it': 'Saluti!\n'
              'Ogni giorno vi parlerò di persone che hanno dato contributi significativi nei loro rispettivi campi.\n'
              'Se volete congratularvi con qualcuno, potete semplicemente dedicare il vostro tempo alle sue fatiche: \n'
              "per esempio, guardare un film con quell'attore, ascoltare l'album di un musicista, leggere le poesie di un poeta, conoscere gli scritti di uno scienziato.",
        'ja': 'グリーツ！\n私は毎日、それぞれの分野で大きな貢献をした人々についてお伝えしていきます。\n'
              'もし、あなたが誰かを祝福したいのであれば、その人の活動にあなたの時間を割けばいいのです。\n'
              '例えば、その俳優の映画を見たり、ミュージシャンのアルバムを聴いたり、詩人の詩を読んだり、科学者の著作に触れたりしてみてください。',
        'kk': 'Сәлем!\n'
              'Мен сізге өз саласына елеулі үлес қосқан адамдар туралы күн сайын айтып беремін.\n'
              'Егер сіз біреуді құттықтағыңыз келсе, оның жұмысына уақытыңызды бөле аласыз:\n'
              'мысалы, осы актермен фильм көріңіз, музыканттың альбомын тыңдаңыз, өлең оқыңыз, ғалымның еңбектерімен танысыңыз.',
        'ko': '안녕하세요!\n저는 매일 각자의 분야에서 상당한 공헌을 한 사람들에 대해 이야기할 것입니다.\n'
              '누군가를 축하하고 싶다면 간단히 그들의 노력에 시간을 할애할 수 있습니다.\n'
              '예를 들어, 그 배우와 함께 영화를 보고, 음악가의 앨범을 듣고, 시인의 시를 읽고, 과학자의 글을 알게 됩니다.',
        'ru': 'Привет!\n'
              'Я буду рассказывать тебе каждый день о людях, которые внесли значительный вклад в свою область деятельности.\n'
              'Если тебе захочется поздравить кого-то, ты можешь просто подарить своё время его трудам: \n'
              'например, посмотреть фильм с этим актёром, послушать альбом музыканта, прочитать стихи поэта, познакомиться с трудами учёного',
        'uk': 'Вітання!\n'
              'Я буду розповідати тобі кожен день про людей, які внесли значний вклад в свою область діяльності.\n'
              'Якщо тобі захочеться привітати когось, ти можеш просто подарувати свій час його працям:\n'
              'наприклад, подивитися фільм з цим актором, послухати альбом музиканта, прочитати вірші поета, познайомитися з працями вченого.',
        'zh': '问候!\n我每天都会向你们介绍那些在各自领域做出重大贡献的人。\n如果你想祝贺某人，你可以简单地把你的时间交给他们的劳动。\n'
              '例如，看一部有该演员的电影，听一张音乐家的专辑，读一首诗人的诗，了解一位科学家的著作。'
        },
    'tour1': {
        'be': 'Такім чынам, кожны дзень я дасылаю табе зводку (brief) пра людзей, якія сёння нарадзіліся.\n'
              'Остортирован спіс па колькасці наведванняў соответсвует старонкі на вікіпедыі.\n'
              'Спіс выводзіцца невялікімі порцыямі, рухацца па ім наперад і назад можна соответсвует клавішамі.',
        'de': 'Jeden Tag sende ich Ihnen also eine (brief) Zusammenfassung der Personen, die heute geboren wurden.\n'
              'Die Liste ist nach der Anzahl der Besuche auf der entsprechenden Seite von Wikipedia geordnet.\n'
              'Die Liste wird in kleinen Stapeln angezeigt, und Sie können mit den entsprechenden Tasten vor- und zurückblättern.',
        'en': 'So, every day I send you a summary (brief) of the people who were born today.\n'
              'The list is ordered by the number of visits to the corresponding page on wikipedia.\n'
              'The list is shown in small batches, and you can move forward and backward with the corresponding keys.',
        'es': 'Así, cada día te envío un resumen (brief) de las personas que han nacido hoy.\n'
              'La lista está ordenada por el número de visitas a la página correspondiente en la wikipedia.\n'
              'La lista se muestra en pequeñas tandas, y puedes avanzar y retroceder con las teclas correspondientes.',
        'fr': "Ainsi, chaque jour, je vous envoie un résumé (brief) des personnes qui sont nées aujourd'hui.\n"
              'La liste est classée en fonction du nombre de visites de la page correspondante sur wikipedia.\n'
              'La liste est affichée par petits lots, et vous pouvez avancer et reculer avec les touches correspondantes.',
        'it': 'Così, ogni giorno vi mando un riassunto (brief) delle persone che sono nate oggi.\n'
              "L'elenco è ordinato in base al numero di visite alla pagina corrispondente su wikipedia.\n"
              'La lista viene mostrata in piccoli lotti, e puoi andare avanti e indietro con i tasti corrispondenti.',
        'ja': 'というわけで、毎日、今日生まれた人たちのサマリー（brief）をお送りします。\n'
              'リストは、wikipediaの対応するページへのアクセス数が多い順に並んでいます。\n'
              'リストは少しずつ表示され、対応するキーで前に進んだり、後ろに戻ったりすることができます。',
        'kk': 'Сондықтан мен сізге күн сайын бүгін туылған адамдар туралы қысқаша (brief) жіберемін.\n'
              'Тізім википедияның сәйкес бетіне кіру саны бойынша сұрыпталған.\n'
              'Тізім кішкене бөліктерде көрсетіледі; сәйкес пернелермен алға және артқа жылжуға болады.',
        'ko': '그래서 나는 매일 당신에게 오늘 태어난 사람들의 요약(brief)을 보냅니다.\n'
              '목록은 위키피디아의 해당 페이지를 방문한 횟수에 따라 정렬됩니다.\n'
              '목록은 작은 배치로 표시되며 해당 키를 사용하여 앞뒤로 이동할 수 있습니다.',
        'ru': 'Итак, каждый день я присылаю тебе сводку (brief) о людях, которые сегодня родились.\n'
              'Остортирован список по количеству посещений соответсвующей страницы на википедии.\n'
              'Список выводится небольшими порциями, двигаться по нему вперёд и назад можно соответсвующими клавишами.',
        'uk': 'Отже, кожен день я надсилаю тобі зведення (brief) про людей, які сьогодні народилися.\n'
              'Остортірован список за кількістю відвідувань відповідної сторінки на вікіпедії.\n'
              'Список виводиться невеликими порціями, рухатися по ньому вперед і назад можна відповідними клавішами.',
        'zh': '因此，每天我都会给你发送一份今天出生的人的摘要（brief）。\n'
              '列表是按照维基百科上相应页面的访问量排序的。\n列表分小批显示，你可以用相应的键向前和向后移动。'
        },
    'tour2': {
        'be': 'Па націску на кнопку з імем адкрываецца картка персаналіі.\n'
              'Гэта фота, некалькі абзацаў з вікіпедыі (часта даволі вычарпальных),\n'
              'а таксама некалькі кнопак: Дадаць у абранае (LIKE), паглядзець дэталі (MORE ..) і адкрыць старонку на вікіпедыі (WIKI)\n'
              'Дэталі запытваюцца з сайта wikidata і ўяўляюць сабой падрабязнасці ў многіх катэгорыях.\n'
              'Калі ты дадасі кагосьці ў выбранае, я магу апавясціць цябе напярэдадні дня яго нараджэння, нагадаць табе, калі захочаш.',
        'de': 'Wenn man auf den Namen klickt, öffnet sich die Karte der Person.\n'
              'Dort gibt es ein Foto, ein paar Absätze aus der Wikipedia (oft recht ausführlich),\n'
              'und einige Schaltflächen: zu den Favoriten hinzufügen (LIKE), Details ansehen (MORE...) und die Wikipedia-Seite öffnen (WIKI)\n'
              'Details werden von wikidata angefordert und stellen Informationen in vielen Kategorien dar.\n'
              'Wenn du jemanden zu deinen Favoriten hinzufügst, kann ich dich am Vorabend seines Geburtstags benachrichtigen, um dich daran zu erinnern, wenn du das möchtest.',
        'en': "Clicking on the name button opens the person's card.\n"
              'There is a photo, a few paragraphs from wikipedia (often quite exhaustive),\n'
              'and some buttons: аdd to favorites (LIKE), see details (MORE...) and open the wikipedia page (WIKI)\n'
              'Details are requested from wikidata and represent information in many categories.\n'
              'If you add someone to your favorites, I can notify you on the eve of their birthday, to remind you if you want.',
        'es': 'Al pulsar el botón del nombre se abre la ficha de la persona.\n'
              'Hay una foto, algunos párrafos de la wikipedia (a menudo bastante exhaustivos)\n'
              'y algunos botones: аdd to favorites (LIKE), see details (MORE...) and open the wikipedia page (WIKI)\n'
              'Los detalles se solicitan a wikidata y representan información en muchas categorías.\n'
              'Si añades a alguien a tus favoritos, puedo avisarte en la víspera de su cumpleaños, para recordártelo si quieres.',
        'fr': 'En cliquant sur le bouton du nom, on ouvre la fiche de la personne.\n'
              'On y trouve une photo, quelques paragraphes de wikipedia (souvent assez exhaustifs),\n'
              'et quelques boutons : аdd aux favoris (LIKE), voir les détails (MORE...) et ouvrir la page wikipedia (WIKI)\n'
              'Les détails sont demandés aux wikidata et représentent des informations dans de nombreuses catégories.\n'
              "Si vous ajoutez quelqu'un à vos favoris, je peux vous avertir la veille de son anniversaire, pour vous le rappeler si vous le souhaitez.",
        'it': 'Cliccando sul tasto del nome si apre la scheda della persona.\n'
              "C'è una foto, alcuni paragrafi di wikipedia (spesso abbastanza esaustivi),\n"
              'e alcuni pulsanti: аggiungi ai preferiti (LIKE), vedi dettagli (MORE...) e apri la pagina di wikipedia (WIKI)\n'
              'I dettagli sono richiesti da wikidata e rappresentano informazioni in molte categorie.\n'
              'Se aggiungi qualcuno ai tuoi preferiti, posso avvisarti alla vigilia del suo compleanno, per ricordartelo se vuoi.',
        'ja': '名前のボタンをクリックすると、その人のカードが開きます。\n'
              'そこには、写真、wikipediaからのいくつかの段落（しばしばかなり網羅的）があります。\n'
              'そしていくつかのボタンがあります：お気に入りに追加（LIKE）、詳細を見る（MORE...）、ウィキペディアのページを開く（WIKI）。\n'
              '詳細はウィキデータから要求され、多くのカテゴリの情報を表しています。\n'
              '誰かをお気に入りに追加すると、その人の誕生日の前夜に通知して、必要に応じて思い出させることができますね。',
        'kk': 'Аты жазылған түймені басу арқылы адамның картасы ашылады.\n'
              'Бұл фотосурет, Википедиядан бірнеше абзац (көбінесе толық),\n'
              'сонымен қатар бірнеше түймелер: Таңдаулыларға қосу (ҰНАУ), мәліметтерді қарау (КӨБІРЕК ..) және Уикипедияда (WIKI) бетті ашу\n'
              'Мәліметтер wikidata сайтынан сұралады және көптеген санаттағы мәліметтерді көрсетеді.\n'
              'Егер сіз біреуді сүйіктілер тізіміне қоссаңыз, мен сізге оның туған күні қарсаңында хабарлай аламын, қаласаңыз, еске саламын.',
        'ko': '이름 버튼을 클릭하면 그 사람의 카드가 열립니다.\n'
              '사진이 있습니다. Wikipedia의 몇 단락(종종 완전함)이 있습니다.\n'
              '및 일부 버튼: 즐겨찾기에 추가(LIKE), 세부정보 보기(MORE...) 및 Wikipedia 페이지 열기(WIKI)\n'
              '자세한 내용은 wikidata에서 요청되며 많은 범주의 정보를 나타냅니다.\n'
              '당신이 당신의 즐겨찾기에 누군가를 추가한다면, 당신이 원한다면 당신을 생각나게 하기 위해 내가 그들의 생일 전날에 당신에게 알려줄 수 있습니다.',
        'ru': 'По нажатию на кнопку с именем открывается карточка персоналии.\n'
              'Это фото, несколько абзацев с википедии (часто довольно исчерпывающих),\n'
              'а также несколько кнопок: Добавить в избранное (LIKE), посмотреть детали (MORE..) и открыть страницу на википедии (WIKI)\n'
              'Детали запрашиваются с сайта wikidata и представляют собой подробности во многих категориях.\n'
              'Если ты добавишь кого-то в избранное, я могу оповестить тебя накануне дня его рождения, напомнить тебе, если захочешь.',
        'uk': "При натисканні на кнопку з ім'ям відкривається картка персоналії.\n"
              'Це фото, кілька абзаців з вікіпедії (часто досить вичерпних),\n'
              'а також кілька кнопок: Додати в обране (LIKE), подивитися деталі (MORE ..) і відкрити сторінку на вікіпедії (WIKI)\n'
              'Деталі запитуються з сайту wikidata і являють собою подробиці у багатьох категоріях.\n'
              'Якщо ти додаси когось в обране, я можу сповістити тебе напередодні дня його народження, нагадати тобі, якщо захочеш.',
        'zh': '点击名字按钮可以打开这个人的卡片。\n这里有一张照片，几段来自维基百科的内容（通常很详尽）。\n'
              '还有一些按钮：添加到收藏夹（LIKE），查看详情（MORE...）和打开维基百科页面（WIKI）。\n'
              '详细内容是从wikidata请求的，代表了许多类别的信息。\n'
              '如果你把某人加入你的收藏夹，我可以在他们的生日前夕通知你，如果你愿意的话，提醒你。'
        },
    'tour3': {
        'be': 'Зараз распавяду табе пра налады.\n'
              'Па-першае, можна выбраць адзін з 12 моў.\n'
              'Налада ўплывае не толькі на мову інтэрфейсу, але і на зводку па людзях, якая будзе адрознівацца для кожнай моўнай групы.\n'
              'Альтэрнатыўны мова выкарыстоўваецца ў тым выпадку, калі для абранага мовы няма перакладу апісання або перакладу тэгаў.',
        'de': 'Jetzt möchte ich Ihnen etwas über die Einstellungen erzählen. \n'
              'Zunächst können Sie eine von 12 Sprachen wählen.\n'
              'Diese Einstellung wirkt sich nicht nur auf die Sprache der Benutzeroberfläche aus, sondern auch auf die Zusammenfassung der Personen, die für jede Sprachgruppe unterschiedlich ist.\n'
              'Die alternative Sprache wird verwendet, wenn es für die gewählte Sprache keine Übersetzung der Beschreibung oder des Tags gibt.',
        'en': 'Now let me tell you about the settings. \n'
              'First, you can choose one of 12 languages.\n'
              'The setting affects not only the interface language, but also the people summary, which will be different for each language group.\n'
              'The alternative language is used when there is no description translation or tag translation for the selected language.',
        'es': 'Ahora déjame hablarte de los ajustes. \n'
              'En primer lugar, puedes elegir uno de los 12 idiomas.\n'
              'La configuración no sólo afecta al idioma de la interfaz, sino también al resumen de personas, que será diferente para cada grupo de idiomas.\n'
              'El idioma alternativo se utiliza cuando no hay traducción de la descripción o de la etiqueta para el idioma seleccionado.',
        'fr': 'Maintenant, laissez-moi vous parler des paramètres. \n'
              "Tout d'abord, vous pouvez choisir l'une des 12 langues.\n"
              "Ce réglage affecte non seulement la langue de l'interface, mais aussi le résumé des personnes, qui sera différent pour chaque groupe linguistique.\n"
              "La langue alternative est utilisée lorsqu'il n'y a pas de traduction de la description ou de la balise pour la langue sélectionnée.",
        'it': 'Ora lascia che ti parli delle impostazioni. \n'
              'In primo luogo, è possibile scegliere una delle 12 lingue.\n'
              "L'impostazione riguarda non solo la lingua dell'interfaccia, ma anche il riassunto delle persone, che sarà diverso per ogni gruppo linguistico.\n"
              "La lingua alternativa viene utilizzata quando non c'è una traduzione della descrizione o dei tag per la lingua selezionata.",
        'ja': 'では、設定について説明します。\nまず、12種類の言語から1つを選ぶことができます。\n'
              'この設定は、インターフェイスの言語だけでなく、人々のサマリーにも影響しますが、これは言語グループごとに異なります。\n'
              '代替言語は、選択した言語に説明文の翻訳やタグの翻訳がない場合に使用されます。',
        'kk': 'Енді мен сізге параметрлер туралы айтып беремін.\n'
              'Біріншіден, таңдау үшін 12 тіл бар.\n'
              'Параметр интерфейс тіліне ғана емес, сонымен қатар әр тіл тобы үшін әр түрлі болатын адамдардың жиынтығына әсер етеді.\n'
              'Таңдалған тілге сипаттама аудармасы немесе тег аудармасы болмаған кезде балама тіл қолданылады.',
        'ko': '이제 설정에 대해 알려드리겠습니다.\n먼저 12개 언어 중 하나를 선택할 수 있습니다.\n'
              '이 설정은 인터페이스 언어뿐만 아니라 각 언어 그룹마다 다른 사람 요약에도 영향을 미칩니다.\n'
              '선택한 언어에 대한 설명 번역 또는 태그 번역이 없을 때 대체 언어가 사용됩니다.',
        'ru': 'Теперь расскажу тебе о настройках. \n'
              'Во-первых, можно выбрать один из 12 языков.\n'
              'Настройка влияет не только на язык интерфейса, но и на сводку по людям (brief), которая будет отличаться для каждой языковой группы.\n'
              'Альтернативный язык используется в том случае, когда для выбранного языка нет перевода описания или перевода тегов.',
        'uk': 'Тепер розповім тобі про налаштування.\n'
              'По-перше, можна вибрати один з 12 мов.\n'
              'Налаштування впливає не тільки на мову інтерфейсу, але і на зведення по людям, яка буде відрізнятися для кожної мовної групи.\n'
              'Альтернативний мова використовується в тому випадку, коли для вибраної мови нема переводу опису або перекладу тегів.',
        'zh': '现在让我告诉你有关设置。\n首先，你可以从12种语言中选择一种。\n'
              '该设置不仅影响到界面语言，而且还影响到人物摘要，每个语言组都会有所不同。\n'
              '当所选语言没有描述翻译或标签翻译时，将使用替代语言。'
        },
    'tour4': {
        'be': 'Па-другое, ты можаш выбраць два тыпу клавіятуры: звычайную (regular), калі кнопкі размешчаны пад полем уводу,\n'
              'і убудавальную або падрадковых (inline), калі кнопкі малююць пад паведамленнем.\n'
              'Не ўсім падабаецца знешні выгляд звычайнай клавіятуры, але многія знаходзяць яе больш зручнай.\n'
              'Зрэшты, для цябе можа быць усё з дакладнасцю да наадварот. Эксперыментуй.',
        'de': 'Zweitens können Sie zwei Arten von Tastaturen wählen: eine normale (regular), wenn sich die Schaltflächen unter dem Eingabefeld befinden,\n'
              'und eine eingebettete (inline), bei der die Schaltflächen unter der Nachricht angezeigt werden.\n'
              'Nicht jeder mag das Aussehen der regulären Tastatur, aber viele Leute finden sie bequemer.\n'
              'Für Sie kann es aber auch genau das Gegenteil sein. Experimentieren Sie.',
        'en': 'Secondly, you can choose two types of keyboard: regular (regular), when the buttons are under the input field,\n'
              'and an inline (inline), where the buttons are rendered under the message.\n'
              'Not everyone likes the look of the regular keyboard, but many people find it more convenient.\n'
              'However, for you it can be exactly the opposite. Experiment.',
        'es': 'En segundo lugar, puede elegir dos tipos de teclado: normal (regular), cuando los botones están debajo del campo de entrada\n'
              'y uno incrustado (inline), en el que los botones aparecen debajo del mensaje.\n'
              'No a todo el mundo le gusta el aspecto del teclado normal, pero a mucha gente le resulta más cómodo.\n'
              'Sin embargo, para ti puede ser exactamente lo contrario. Experimenta.',
        'fr': 'Ensuite, vous pouvez choisir deux types de clavier: un clavier normal (regular), lorsque les boutons se trouvent sous le champ de saisie,\n'
              'et un clavier intégré (inline), où les boutons sont rendus sous le message.\n'
              "Tout le monde n'aime pas l'aspect du clavier ordinaire, mais beaucoup de gens le trouvent plus pratique.\n"
              'Cependant, pour vous, cela peut être exactement le contraire. Expérimentez.',
        'it': 'In secondo luogo, puoi scegliere due tipi di tastiera: regolare (regular), quando i pulsanti sono sotto il campo di inserimento,\n'
              'e una incorporata (inline), dove i pulsanti sono resi sotto il messaggio.\n'
              "Non a tutti piace l'aspetto della tastiera regolare, ma molte persone la trovano più conveniente.\n"
              'Tuttavia, per voi può essere esattamente il contrario. Sperimentate.',
        'ja': '次に、ボタンが入力フィールドの下にあるレギュラー（regular）'
              'と、ボタンがメッセージの下にレンダリングされる埋め込み（inline）の2種類のキーボードを選ぶことができます。\n'
              'すべての人がレギュラーキーボードの見た目を好むわけではありませんが、多くの人がレギュラーキーボードの方が便利だと感じています。\n'
              'しかし、あなたにとっては全く逆の場合もあります。実験です。',
        'kk': 'Екіншіден, сіз пернетақтаның екі түрін таңдай аласыз: тұрақты (тұрақты), батырмалар енгізу өрісінің астында орналасқан кезде,\n'
              'және хабарламаның астында түймелер көрсетілгенде кірістірілген немесе кірістірілген.\n'
              'Кәдімгі пернетақтаның көрінісі бәріне ұнамайды, бірақ көпшілігі оны ыңғайлы деп санайды.\n'
              'Алайда, сіз үшін бәрі керісінше болуы мүмкін. Эксперимент.',
        'ko': '두 번째로, 버튼이 입력 필드 아래에 있는 일반(regular) '
              '키보드와 메시지 아래에 버튼이 렌더링되는 임베디드(inline)의 두 가지 유형의 키보드를 선택할 수 있습니다.\n'
              '모든 사람이 일반 키보드의 모양을 좋아하는 것은 아니지만 많은 사람들이 더 편리하다고 생각합니다.\n'
              '그러나 당신에게는 정확히 그 반대일 수 있습니다. 실험.',
        'ru': 'Во-вторых, ты можешь выбрать два типа клавиатуры: обычную (regular), когда кнопки расположены под полем ввода,\n'
              'и встраиваемую или подстрочную (inline), когда кнопки отрисовываются под сообщением.\n'
              'Не всем нравится внешний вид обычной клавиатуры, но многие находят её более удобной. \n'
              'Впрочем, для тебя может быть всё с точностью до наоброт. Экспериментируй.',
        'uk': 'По-друге, ти можеш вибрати два типи клавіатури: звичайну (regular), коли кнопки розташовані під полем введення,\n'
              'і вбудовується або підрядковим (inline), коли кнопки отрісовиваємих під повідомленням.\n'
              'Не всім подобається зовнішній вигляд звичайної клавіатури, але багато хто знаходить її більш зручною.\n'
              'Втім, для тебе може бути все з точністю до наоброт. Експериментуй.',
        'zh': '其次，你可以选择两种类型的键盘：常规（regular），当按钮在输入栏下时。\n'
              '和嵌入式键盘（inline），在这种情况下，按钮被呈现在信息下面。\n'
              '不是每个人都喜欢普通键盘的外观，但许多人认为它更方便。\n然而，对你来说，它可能正好相反。实验。'
        },
    'tour5': {
        'be': 'Далей можна наладзіць колькасць гэтых самых кнопак (1), колькасць радкоў у порцыі (2) і велічыню зруху (3),\n'
              'г.зн. колькасць радкоў, на якое перамесціцца наступную выснову. Звычайна ўсталёўваецца роўным колькасці кнопак клавіятуры.\n'
              'Колькасць радкоў (2) падладжваецца такім чынам, каб увесь спіс змяшчаўся на экране.\n'
              'У залежнасці ад памеру шрыфта і дазволу вашага прылады гэтая лічба можа моцна змяняцца.',
        'de': 'Dann können Sie die Anzahl dieser Schaltflächen unter der Zusammenfassung (1), die Anzahl der Zeilen im Stapel (2) und den Umfang der Verschiebung (3) einstellen, \n'
              'd. h. die Anzahl der Zeilen, um die die nächste Ausgabe verschoben wird. Normalerweise wird sie gleich der Anzahl der Tastaturtasten gesetzt.\n'
              'Die Anzahl der Zeilen (2) wird so eingestellt, dass die gesamte Liste auf den Bildschirm passt.\n'
              'Je nach Schriftgröße und Auflösung Ihres Geräts kann diese Zahl stark variieren.',
        'en': 'Then you can adjust the number of these buttons under the summary (1), the number of lines in the batch (2), and the amount of shift (3), \n'
              'i.e. the number of lines by which the next output will be shifted. Usually it is set equal to the number of keyboard buttons.\n'
              'The number of lines (2) is adjusted so that the whole list fits on the screen.\n'
              'Depending on the font size and resolution of your device, this number can vary quite a bit.',
        'es': 'Entonces puede ajustar el número de estos botones bajo el resumen (1), el número de líneas en el lote (2) y la cantidad de desplazamiento (3), \n'
              'es decir, el número de líneas en que se desplazará la siguiente salida. Normalmente se establece igual al número de botones del teclado.\n'
              'El número de líneas (2) se ajusta para que toda la lista quepa en la pantalla.\n'
              'Dependiendo del tamaño de la fuente y la resolución de su dispositivo, este número puede variar bastante.',
        'fr': 'Ensuite, vous pouvez ajuster le nombre de ces boutons sous le résumé (1), le nombre de lignes dans le lot (2), et la quantité de décalage (3), \n'
              "c'est-à-dire le nombre de lignes dont la prochaine sortie sera décalée. Habituellement, ce nombre est égal au nombre de boutons du clavier.\n"
              "Le nombre de lignes (2) est ajusté de manière à ce que la liste entière tienne sur l'écran.\n"
              'En fonction de la taille de la police et de la résolution de votre appareil, ce nombre peut varier assez fortement.',
        'it': 'Poi puoi regolare il numero di questi pulsanti sotto il sommario (1), il numero di linee nel gruppo (2), e la quantità di spostamento (3), \n'
              "cioè il numero di linee di cui sarà spostata l'uscita successiva. Di solito è impostato uguale al numero di pulsanti della tastiera.\n"
              "Il numero di linee (2) è regolato in modo che l'intera lista si adatti allo schermo.\n"
              'A seconda della dimensione del carattere e della risoluzione del tuo dispositivo, questo numero può variare abbastanza.',
        'ja': 'そして、要約の下にあるこれらのボタンの数（1）、バッチの行数（2）、シフト量（3）を調整します。\n'
              'つまり、次の出力がシフトされる行数です。通常は、キーボードボタンの数と同じに設定されています。\n'
              '行数(2)は、リスト全体が画面に収まるように調整します。\nデバイスのフォントサイズや解像度によって、この数はかなり変わります。',
        'kk': 'Әрі қарай, сіз сол түймелердің санын (1), бөліктегі жолдардың санын (2) және ығысу мөлшерін (3),\n'
              'яғни келесі шығарылым жылжытылатын жолдар саны. Әдетте пернетақта түймелерінің санына тең болады.\n'
              'Жолдар саны (2) бүкіл тізім экранға сәйкес келетін етіп реттеледі.\n'
              'Құрылғының қаріп өлшемі мен ажыратымдылығына байланысты бұл көрсеткіш айтарлықтай өзгеруі мүмкін.',
        'ko': '그런 다음 요약(1) 아래에 있는 이러한 버튼의 수, 배치의 라인 수(2), 이동량(3)을 조정할 수 있습니다.\n'
              '즉, 다음 출력이 이동할 줄의 수입니다. 일반적으로 키보드 버튼의 수와 동일하게 설정됩니다.\n'
              '전체 목록이 화면에 맞도록 줄 수(2)가 조정됩니다.\n장치의 글꼴 크기와 해상도에 따라 이 숫자는 상당히 다를 수 있습니다.',
        'ru': 'Далее можно настроить количество этих самых кнопок (1), количество строчек в порции (2) и величину сдвига (3), \n'
              'т.е. количество строчек, на которое сместится следующий вывод. Обычно устанавливается равным количеству кнопок клавиатуры.\n'
              'Количество строчек (2) подстраивается таким образом, чтобы весь список помещался на экране.\n'
              'В зависимости от размера шрифта и разрешения вашего устройства эта цифра может сильно меняться.',
        'uk': 'Далі можна налаштувати кількість цих самих кнопок (1), кількість рядків в порції (2) і величину зсуву (3),\n'
              'тобто кількість рядків, на яке зміститься наступний висновок. Зазвичай встановлюється рівною кількості кнопок клавіатури.\n'
              'Кількість рядків (2) підлаштовується таким чином, щоб весь список містився на екрані.\n'
              'Залежно від розміру шрифту і дозволу вашого пристрою ця цифра може сильно змінюватися.',
        'zh': '然后你可以调整摘要下的这些按钮的数量（1），批次中的行数（2），以及移位量（3）。\n'
              '也就是下一个输出将被移位的行数。通常情况下，它被设定为等于键盘按钮的数量。\n'
              '行数（2）的调整是为了使整个列表适合在屏幕上显示。\n根据你的设备的字体大小和分辨率，这个数字可以有很大的变化。'
        },
    'tour6': {
        'be': 'І апошняе, што варта распавесці пра налады, гэта раздзел абвестак.\n'
              'Тут можна наладзіць час штодзённых абвестак, для чаго неабходна таксама пазначыць гадзінны пояс.\n'
              'Тут жа наладжваецца неабходнасць _отдельных_ напамінкаў аб днях нараджэння людзей, якіх ты дадаў у абранае.\n'
              'Можна зусім адключыць паведамлення ад бота, каб ён не дасылаў штодзённую зводку, гэта раўнасільна камандзе STOP.\n'
              'Дарэчы, усе паведамлення ад бота прыходзяць у ціхім рэжыме.',
        'de': 'Der letzte erwähnenswerte Punkt in den Einstellungen ist der Bereich Benachrichtigungen.\n'
              'Hier können Sie den Zeitpunkt der täglichen Benachrichtigungen einstellen, wofür Sie auch die Zeitzone angeben müssen.\n'
              'Hier können Sie auch einstellen, dass Sie _individuelle_ Erinnerungen an die Geburtstage von Personen erhalten möchten, die Sie zu Ihren Favoriten hinzugefügt haben.\n'
              'Sie können die Bot-Benachrichtigungen komplett abschalten, damit ich keine tägliche Zusammenfassung senden muss, was einem STOP-Befehl entspricht.\n'
              'Übrigens, alle Bot-Benachrichtigungen werden im Stumm-Modus gesendet.',
        'en': 'The last thing worth mentioning about the settings is the notifications section.\n'
              'Here you can set the time of daily notifications, for which you must also specify the time zone.\n'
              "Here you can also set up the need for _individual_ reminders about the birthdays of people you've added to your favorites.\n"
              "You can turn off bot notifications completely, so that I don't have to send a daily summary, which is the equivalent of a STOP command.\n"
              'By the way, all bot notifications come in silent mode.',
        'es': 'La última cosa que vale la pena mencionar sobre los ajustes es la sección de notificaciones.\n'
              'Aquí puedes establecer la hora de las notificaciones diarias, para lo cual también debes especificar la zona horaria.\n'
              'Aquí también puedes configurar la necesidad de recordatorios _individuales_ sobre los cumpleaños de las personas que has añadido a tus favoritos.\n'
              'Puedes desactivar por completo las notificaciones del bot, para que no tenga que enviar un resumen diario, lo que equivale a un comando STOP.\n'
              'Por cierto, todas las notificaciones del bot vienen en modo silencioso.',
        'fr': "La dernière chose qui mérite d'être mentionnée à propos des paramètres est la section des notifications.\n"
              "Vous pouvez y définir l'heure des notifications quotidiennes, pour lesquelles vous devez également spécifier le fuseau horaire.\n"
              'Vous pouvez également définir la nécessité de recevoir des rappels _individuels_ pour les anniversaires des personnes que vous avez ajoutées à vos favoris.\n'
              "Vous pouvez désactiver complètement les notifications du robot, afin que je n'aie pas à envoyer un résumé quotidien, qui est l'équivalent d'une commande STOP.\n"
              "D'ailleurs, toutes les notifications des robots sont en mode silencieux.",
        'it': "L'ultima cosa che vale la pena menzionare sulle impostazioni è la sezione delle notifiche.\n"
              "Qui è possibile impostare l'orario delle notifiche giornaliere, per le quali è necessario specificare anche il fuso orario.\n"
              'Qui puoi anche impostare la necessità di promemoria _individuali_ sui compleanni delle persone che hai aggiunto ai tuoi preferiti.\n'
              "È possibile disattivare completamente le notifiche del bot, in modo da non dover inviare un riassunto giornaliero, che è l'equivalente di un comando STOP.\n"
              'A proposito, tutte le notifiche bot sono in modalità silenziosa.',
        'ja': '設定について最後に言及する価値があるのは、通知のセクションです。\n'
              'ここでは、毎日の通知の時間を設定でき、そのためにはタイムゾーンを指定する必要があります。\n'
              'また、お気に入りに登録した人の誕生日を、個別に通知するかどうかも設定できます。\n'
              'ボット通知を完全にオフにすることもできるので、STOPコマンドに相当するデイリーサマリーを送信する必要はありません。\n'
              'ちなみに、ボットの通知はすべてサイレントモードで行われます。',
        'kk': 'Параметрлер туралы айтуға тұрарлық соңғы нәрсе - хабарламалар бөлімі.\n'
              'Мұнда сіз күнделікті ескертулердің уақытын орната аласыз, ол үшін уақыт белдеуін де көрсету қажет.\n'
              'Мұнда сіз таңдаулыларға қосқан адамдардың туған күндері туралы _ бөлек_ еске салғыштардың қажеттілігін теңшей аласыз.\n'
              'Сіз боттан күнделікті хабарлама жібермеуі үшін хабарландыруларды толығымен өшіре аласыз, бұл STOP командасына тең.\n'
              'Айтпақшы, барлық бот хабарландырулары тыныш режимде келеді.',
        'ko': '설정에 대해 언급할 가치가 있는 마지막 사항은 알림 섹션입니다.\n'
              '여기에서 시간대도 지정해야 하는 일일 알림 시간을 설정할 수 있습니다.\n'
              '여기에서 즐겨찾기에 추가한 사람들의 생일에 대한 _개별_ 알림의 필요성을 설정할 수도 있습니다.\n'
              '봇 알림을 완전히 끌 수 있으므로 STOP 명령에 해당하는 일일 요약을 보낼 필요가 없습니다.\n'
              '그건 그렇고, 모든 봇 알림은 자동 모드로 제공됩니다.',
        'ru': 'И последнее, что стоит рассказать о настройках, это раздел оповещений.\n'
              'Здесь можно настроить время ежедневных оповещений, для чего необходимо также указать часовой пояс.\n'
              'Здесь же настраивается необходимость _отдельных_ напоминаний о днях рождениях людей, которых ты добавил в избранное.\n'
              'Можно совсем отключить уведомления от бота, чтобы он не присылал ежедневную сводку, это равносильно команде STOP.\n'
              'Кстати, все уведомления от бота приходят в тихом режиме.',
        'uk': 'І останнє, що варто розповісти про налаштування, це розділ сповіщень.\n'
              'Тут можна налаштувати час щоденних повідомлень, для чого необхідно також вказати часовий пояс.\n'
              'Тут же налаштовується необхідність _отдельних_ нагадувань про дні народження людей, яких ти додав в обране.\n'
              'Можна зовсім відключити повідомлення від бота, щоб він не надсилав щоденну зведення, це рівносильно команді STOP.\n'
              'До речі, всі повідомлення від бота приходять в тихому режимі.',
        'zh': '关于设置，最后值得一提的是通知部分。\n在这里你可以设置每日通知的时间，为此你还必须指定时区。\n'
              '在这里，你还可以设置是否需要对你添加到收藏夹的人的生日进行_个别提醒。\n'
              '你可以完全关闭机器人通知，这样我就不必发送每日摘要，这相当于一个STOP命令。\n'
              '顺便说一下，所有的机器人通知都是以无声模式进行的。'
        },
    'tour7': {
        'be': 'Многія каманды можна проста ўводзіць у поле ўводу, каб не пераходзіць у меню.\n'
              "Так, напрыклад, каб змяніць лакаль, дастаткова проста адправіць паведамленне з тэкстам 'ru' ці 'en' ці 'es' і г.д.\n"
              'Каб перайсці ў меню, можна адправіць слова "меню" на любой мове ці выбраць каманду / menu\n'
              'Налады адкрываюцца словам config ці камандай / sets.\n'
              'Можна ўводзіць словы "ўчора", "сёння", "заўтра" або набіраць дату ў фармаце дд.мм.\n'
              'Каб гартаць наперад-назад можна адправіць паведамленні fw або rw, ну або выкарыстаць адпаведныя кнопкі.',
        'de': 'Viele Befehle können einfach in das Eingabefeld eingegeben werden, ohne das Menü aufzurufen.\n'
              'Wenn Sie beispielsweise das Gebietsschema ändern möchten, senden Sie einfach eine Nachricht mit dem Text "en" oder "es" oder "ru" usw.\n'
              'Um das Menü aufzurufen, können Sie das Wort "menu" in einer beliebigen Sprache senden oder den Befehl /menu wählen\n'
              'Die Einstellungen werden mit dem Wort "config" oder dem Befehl /sets geöffnet.\n'
              'Sie können die Wörter "gestern", "heute", "morgen" oder das Datum im Format tt.mm eingeben.\n'
              'Um vorwärts und rückwärts zu blättern, können Sie fw- oder rw-Nachrichten senden oder die entsprechenden Schaltflächen verwenden.',
        'en': 'Many commands can simply be entered in the input field without going to the menu.\n'
              "So, for example, to change the locale, just send a message with the text 'en' or 'es' or 'ru', etc.\n"
              'To go to the menu, you can send the word "menu" in any language or select the command /menu\n'
              'The settings are opened with the word "config" or the command /sets.\n'
              "You can enter the words 'yesterday', 'today', 'tomorrow' or type the date in dd.mm format.\n"
              'To browse forward and backward you can send fw or rw messages, or use the corresponding buttons.',
        'es': 'Muchos comandos se pueden introducir simplemente en el campo de entrada sin ir al menú.\n'
              'Así, por ejemplo, para cambiar la configuración regional, basta con enviar un mensaje con el texto "en" o "es" o "ru", etc.\n'
              'Para ir al menú, puedes enviar la palabra "menú" en cualquier idioma o seleccionar el comando /menú\n'
              'Los ajustes se abren con la palabra "config" o el comando /sets.\n'
              'Puedes introducir las palabras "ayer", "hoy", "mañana" o escribir la fecha en formato mm-dd.\n'
              'Para navegar hacia adelante y hacia atrás puedes enviar mensajes fw o rw, o utilizar los botones correspondientes.',
        'fr': 'De nombreuses commandes peuvent être saisies simplement dans le champ de saisie sans passer par le menu.\n'
              'Par exemple, pour changer de langue, il suffit d\'envoyer un message contenant le texte "en" ou "es" ou "ru", etc.\n'
              'Pour accéder au menu, vous pouvez envoyer le mot "menu" dans n\'importe quelle langue ou sélectionner la commande /menu.\n'
              'Les paramètres sont ouverts avec le mot "config" ou la commande /sets.\n'
              'Vous pouvez saisir les mots "hier", "aujourd\'hui", "demain" ou taper la date au format jj.mm.\n'
              'Pour naviguer en avant et en arrière, vous pouvez envoyer des messages fw ou rw, ou utiliser les boutons correspondants.',
        'it': 'Molti comandi possono essere semplicemente inseriti nel campo di input senza andare nel menu.\n'
              "Così, per esempio, per cambiare il locale, basta inviare un messaggio con il testo 'en' o 'es' o 'ru', ecc.\n"
              'Per andare al menu, puoi inviare la parola "menu" in qualsiasi lingua o selezionare il comando /menu\n'
              'Le impostazioni si aprono con la parola "config" o con il comando /sets.\n'
              'Si possono inserire le parole "ieri", "oggi", "domani" o digitare la data nel formato gg.mm.\n'
              'Per navigare avanti e indietro puoi inviare messaggi fw o rw, o usare i pulsanti corrispondenti.',
        'ja': '多くのコマンドは、メニューに行かなくても入力欄に入力するだけで済みます。\n'
              '例えば、ロケールを変更するには、「en」や「es」、「ru」などのテキストを入力してメッセージを送信すればよいのです。\n'
              'メニューに移動するには、任意の言語で「menu」という単語を送信するか、「/menu」というコマンドを選択します。\n'
              '設定を開くには、"config "という単語を送るか、/setsというコマンドを選択します。\n'
              '昨日」、「今日」、「明日」という言葉を入力するか、dd.mm形式で日付を入力することができます。\n'
              '前後にブラウズするには、fw または rw メッセージを送信するか、対応するボタンを使用します。',
        'kk': 'Көптеген командаларды енгізу өрісіне мәзірге кірмей -ақ енгізуге болады.\n'
              "Мысалы, тілді өзгерту үшін сізге 'ru' немесе 'en' немесе 'es' т.б мәтіні бар хабарлама жіберу қажет.\n"
              'Мәзірге өту үшін кез келген тілдегі «меню» сөзін жіберуге немесе команданы / мәзірді таңдауға болады\n'
              'Параметрлер config сөзімен немесе / sets командасымен ашылады.\n'
              'Сіз «кеше», «бүгін», «ертең» сөздерін енгізе аласыз немесе күнді dd.mm форматында тере аласыз.\n'
              'Алға -артқа айналдыру үшін fw немесе rw хабарларын жіберуге болады немесе сәйкес түймелерді қолдана аласыз.',
        'ko': '메뉴로 이동하지 않고 많은 명령을 입력 필드에 간단히 입력할 수 있습니다.\n'
              "예를 들어 로케일을 변경하려면 'en' 또는 'es' 또는 'ru' 등의 텍스트가 포함된 메시지를 보내십시오.\n"
              '메뉴로 이동하려면 모든 언어로 "menu"라는 단어를 보내거나 /menu 명령을 선택하십시오.\n'
              '설정은 "config"라는 단어 또는 /sets 명령으로 열립니다.\n'
              "'어제', '오늘', '내일'을 입력하거나 dd.mm 형식으로 날짜를 입력할 수 있습니다.\n"
              '앞으로 및 뒤로 탐색하려면 fw 또는 rw 메시지를 보내거나 해당 버튼을 사용할 수 있습니다.',
        'ru': 'Многие команды можно просто вводить в поле ввода, не переходя в меню.\n'
              "Так, например, чтобы сменить локаль, достаточно просто отправить сообщение с текстом 'ru' или 'en' или 'es' и т.д.\n"
              'Чтобы перейти в меню, можно отправить слово "меню" на любом языке или выбрать команду /menu\n'
              'Настройки открываются словом config или командой /sets.\n'
              'Можно вводить слова "вчера", "сегодня", "завтра" или набирать дату в формате дд.мм.\n'
              'Чтобы листать вперёд-назад можно отправить сообщения fw или rw, ну или использовать соответствующие кнопки.',
        'uk': 'Багато команд можна просто вводити в поле введення, не переходячи в меню.\n'
              "Так, наприклад, щоб змінити локаль, досить просто відправити повідомлення з текстом 'ru' або 'en' або 'es' і т.д.\n"
              'Щоб перейти в меню, можна відправити слово "меню" на будь-якій мові або вибрати команду / menu\n'
              'Налаштування відкриваються словом config або командою / sets.\n'
              'Можна вводити слова "вчора", "сьогодні", "завтра" або набирати дату в форматі дд.мм.\n'
              'Щоб гортати вперед-назад можна відправити повідомлення fw або rw, ну або використовувати відповідні кнопки.',
        'zh': '许多命令可以简单地在输入栏中输入，而不必进入菜单。\n'
              '因此，例如，要改变地区，只需发送一条带有 "en "或 "es "或 "ru "等文字的信息。\n'
              '要进入菜单，你可以用任何语言发送 "menu "这个词或者选择/menu这个命令。\n'
              '用 "config "这个词或/sets这个命令打开设置。\n'
              '你可以输入 "昨天"、"今天"、"明天 "或输入dd.mm格式的日期。\n'
              '要向前和向后浏览，你可以发送fw或rw信息，或使用相应的按钮。'
        },
    'tour8': {
        'be': 'Калі ты знайшоў памылку ў перакладзе, недарэчнасць у працы ці нешта выклікала твае негатыўныя пачуцці,'
              ' проста напішы пра гэта ў Водгук.\nНу што ж, вось, здаецца, і ўсё! Усяго добрага!',
        'de': 'Wenn Sie einen Übersetzungsfehler gefunden haben, etwas Seltsames oder etwas, das Ihnen Unbehagen bereitet hat, '
              'schreiben Sie es einfach in die Rezension.\n'
              "Tja, das war's dann wohl! Habt einen schönen Tag!",
        'en': "If you found a translation mistake, something weird, or something that made you feel uncomfortable, "
              "just write about it to the Review.\n If something remains unclear, you can ask me a question in PM @timeclackx\n"
              " Well, that's about it! Have a nice day!",
        'es': 'Si has encontrado un error de traducción, algo raro, o algo que te ha hecho sentir incómodo, '
              'sólo tienes que escribirlo en la Revisión.\nBueno, ¡eso es todo! ¡Que tengas un buen día!',
        'fr': "Si vous avez trouvé une erreur de traduction, quelque chose de bizarre, ou quelque chose qui vous a mis mal à l'aise, "
              "écrivez simplement à ce sujet dans la revue.\n"
              "Voilà, c'est à peu près tout ! Passez une bonne journée !",
        'it': 'Se hai trovato un errore di traduzione, qualcosa di strano, o qualcosa che ti ha fatto sentire a disagio, '
              'basta scriverlo in Review.\nBene, questo è tutto! Buona giornata!',
        'ja': 'もし、翻訳の間違いや奇妙なこと、不快なことを見つけたら、そのことをレビューに書いてください。\nさて、以上です。それでは、よろしくお願いします。',
        'kk': 'Егер сіз аудармадан қате тапсаңыз, жұмыстағы оғаштық немесе бірдеңе сіздің жағымсыз сезімдеріңізді тудырса, '
              'бұл туралы шолуда жазыңыз.\nЖақсы, бәрі осылай болған сияқты! Іске сәт!',
        'ko': '번역 오류, 이상한 점, 불편한 점을 발견했다면 리뷰에 글을 남겨주세요.\n그게 다야! 좋은 하루 되세요!',
        'ru': 'Если ты нашёл ошибку в переводе, странность в работе или что-то вызвало твои негативные чувства, '
              'просто напиши об этом в Отзыв.\nНу что ж, вот вроде бы и всё! Всего хорошего!',
        'uk': 'Якщо ти знайшов помилку в перекладі, дивина в роботі або щось викликало твої негативні почуття, '
              'просто напиши про це в Відгук.\nНу що ж, ось начебто і все! Всього найкращого!',
        'zh': '如果你发现了一个翻译错误，一些奇怪的东西，或者一些让你感到不舒服的东西，只要把它写到评论里就可以了。\n'
              '好了，就说到这里吧! 祝你有个愉快的一天!'
        },
    'endhelp': {
        'ru': 'Просто оставлю\n это здесь:\nНастройки /sets\nМеню /menu\nПомощь /help\nРазработка \n@timeclackx',
        'en': "I'll just leave\n this here:\nSettings /sets\nMenu /menu\nHelp /help\nDevelopment \n@timeclackx",
        'be': 'Я проста пакіну\n гэта тут:\nНалады /sets\nМеню /меню\nДапамога /help\nРаспрацоўка \n@timeclackx',
        'uk': 'Я просто залишу\n це тут:\nНалаштування /sets\nМеню /menu\nДопомога /help\nРозробка \n@timeclackx',
        'kk': 'Мен оны осында\n қалдырамын:\nПараметрлер /sets\nМәзір /menu\nКөмек /help\nӘзірлеу \n@timeclackx',
        'de': 'Ich lasse es\n einfach hier:\nEinstellungen /sets\nMenü /menu\nHilfe /help\nErarbeitung \n@timeclackx',
        'es': 'Lo dejaré aquí:\nAjustes /sets\nMenú /menu\nAyuda /help\nElaboración\n@timeclackx',
        'fr': 'Je vais juste\n le laisser ici:\nParamètres /sets\nMenu /menu\nAide /help\nDéveloppement \n@timeclackx',
        'it': 'Lo lascio qui:\nImpostazioni /sets\nMenu /menu\nAiuto /help\nSviluppo \n@timeclackx',
        'zh': '我就把它放在这里：\n设置 /sets\n菜单 /menu\n帮助 /help\n发展\n@timeclackx',
        'ko': '그냥 여기에\n두겠습니다.\n설정 /sets\n메뉴 /menu\n도움 /help\n개발\n@timeclackx',
        'ja': 'ここに残しておきます：\n設定 /sets\nメニュー /menu\nヘルプ /help\n開発\n@timeclackx'
        },
}


def get_translation(message, locale):
    result = ''
    mess_dict = MESSAGES.get(message)
    if mess_dict:
        result = mess_dict.get(locale)
    if result:
        if message == 'language':
            return result + ' (Lang)'
        return result
    if mess_dict:
        return message.capitalize()
    else:
        return message


def get_values(key):
    result = [key, ]
    values = MESSAGES.get(key)
    if values:
        for value in values.values():
            if key == 'language':
                result.append(value + ' \(Lang\)')
            else:
                result.append(value)
    return result


def re_join(key, additional=[]):
    values = get_values(key) + additional
    return '^(' + '|'.join(values) + ')$'


def get_dayname(bday, locale):
    return format_skeleton('MMMMd', datetime.strptime(bday + '.80', '%m.%d.%y'), locale=locale)
