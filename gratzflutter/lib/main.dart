import 'dart:async';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'settings.dart';

void main() => runApp(new MyApp());

class MyApp extends StatefulWidget {
  @override
  _AppState createState() => new _AppState();

  static void setLocale(BuildContext context, String locale) {
    _AppState? state = context.findAncestorStateOfType<_AppState>()!;
    state.setState(() {
      state._locale = locale;
    });
  }
}

class _AppState extends State<MyApp> {
  int color = Colors.green.value;
  int brightness = Brightness.light.index;
  String _locale = 'ru';

  @override
  Widget build(BuildContext context) {
    return new MaterialApp(
        locale: Locale(_locale),
        localizationsDelegates: AppLocalizations.localizationsDelegates,
        supportedLocales: AppLocalizations.supportedLocales,
        theme: new ThemeData(
          primaryColor: Color(color),
          brightness: Brightness.values[brightness],
        ),
        home: new MyHomePage());
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  Map<String, List<Map<String, dynamic>>> allItems = {};
  ScrollController _scrollController1 = new ScrollController();
  ScrollController _scrollController2 = new ScrollController();
  ScrollController _scrollController3 = new ScrollController();
  Map<int, bool> isPerformingRequest = {};

  SharedPreferences? preferences;
  int mainColor = Colors.green.value;
  int brightness = Brightness.dark.index;
  bool isDark = false;

  Future<void> initializePreferences() async {
    preferences = await SharedPreferences.getInstance();
  }

  void loadPreferences() async {
    mainColor = preferences?.getInt("color") ?? Colors.green.value;
    brightness = preferences?.getInt("bright") ?? Brightness.light.index;
    isDark = (brightness == 0) ? true : false;
    setState(() {});
  }

  @override
  void initState() {
    super.initState();
    initializePreferences().whenComplete(() {
      loadPreferences();
    });

    hangListener(int tabNum) {
      ScrollController _scrollController = getScrollController(tabNum);
      _scrollController.addListener(() {
        if (_scrollController.position.pixels ==
            _scrollController.position.maxScrollExtent) {
          _getMoreData(tabNum);
        }
      });
    }

    hangListener(0);
    hangListener(1);
    hangListener(2);
  }

  String apptitle = "Cong Gratz календарь";
  DateTime selectedDate = DateTime.now();

  @override
  Widget build(BuildContext context) {
    Image settingsIcon = isDark
        ? Image.asset('graphics/moon.png')
        : Image.asset('graphics/sun.png');
    if (!allItems.containsKey(bdayFromOffset(-1))) _getMoreData(0);
    if (!allItems.containsKey(bdayFromOffset(0))) _getMoreData(1);
    if (!allItems.containsKey(bdayFromOffset(1))) _getMoreData(2);

    ListView listView(int tabNum) {
      String bday = bdayFromOffset(tabNum - 1);
      List<Map<String, dynamic>> items = allItems[bday] ?? [];

      return ListView.builder(
        itemCount: items.length + 1,
        itemBuilder: (context, index) {
          if (index >= items.length) {
            return _buildProgressIndicator();
          } else {
            return Card(
                elevation: 13.0,
                margin: EdgeInsets.symmetric(horizontal: 10.0, vertical: 6.0),
                child: Container(
                    child: ListTile(
                  contentPadding:
                      EdgeInsets.symmetric(horizontal: 20.0, vertical: 10.0),
                  leading: Text(
                      '${items[index]['icon']}\n${items[index]['flag']}',
                      style: TextStyle(fontSize: 24)),
                  title: Text(items[index]['name'][langChosen]),
                  subtitle: Text('${items[index]['info'][langChosen]}'),
                  trailing: _getBklAsset(items[index]['bkls']),
                  onTap: () => openDetailed(items[index]),
                )));
          }
        },
        controller: getScrollController(tabNum),
      );
    }

    return DefaultTabController(
        length: 3,
        initialIndex: 1,
        child: MaterialApp(
            locale: Locale(langChosen),
            theme: new ThemeData(
              primaryColor: Color(mainColor),
              brightness: Brightness.values[brightness],
            ),
            home: Scaffold(
                appBar: AppBar(
                  title: Text(AppLocalizations.of(context)!.main_title),
                  elevation: 15.0,
                  actions: [
                    IconButton(
                        icon: Image.asset('graphics/clndr2.png'),
                        onPressed: () => _selectDate(context)),
                    IconButton(
                        icon: Image.asset('graphics/flag$langNext.png'),
                        onPressed: () => _selectNextLang()),
                    IconButton(
                        icon: settingsIcon, onPressed: () => openSettings()),
                    Image.asset('graphics/blank.png')
                  ],
                  bottom: TabBar(
                    isScrollable: true,
                    labelStyle: TextStyle(fontSize: 26),
                    tabs: <Tab>[
                      Tab(text: dateFromOffsetLocalized(-1)[langChosen]),
                      Tab(text: dateFromOffsetLocalized(0)[langChosen]),
                      Tab(text: dateFromOffsetLocalized(1)[langChosen]),
                    ],
                  ),
                ),
                body: TabBarView(children: <Widget>[
                  listView(0),
                  listView(1),
                  listView(2)
                ]))));
  }

  openDetailed(data) async {
    Navigator.of(context).push(
      MaterialPageRoute<void>(
        builder: (BuildContext context) {
          Widget wikiInfo(title) {
            return FutureBuilder(
              builder: (context, AsyncSnapshot snapshot) {
                switch (snapshot.connectionState) {
                  case ConnectionState.none:
                  case ConnectionState.active:
                  case ConnectionState.waiting:
                    return _buildProgressIndicator();
                  case ConnectionState.done:
                    if (snapshot.hasError) {
                      return Text('Error: ${snapshot.error}');
                    } else {
                      return Padding(
                        padding: EdgeInsets.fromLTRB(20, 20, 20, 20),
                        child: Text(
                          snapshot.data,
                          textAlign: TextAlign.justify,
                          overflow: TextOverflow.fade,
                          style: TextStyle(fontSize: 18),
                        ),
                      );
                    }
                }
              },
              future: getWikiPage(title),
            );
          }

          return Scaffold(
            body: NestedScrollView(
              headerSliverBuilder:
                  (BuildContext context, bool innerBoxIsScrolled) {
                return <Widget>[
                  SliverAppBar(
                      expandedHeight: 500.0,
                      floating: true,
                      pinned: true,
                      flexibleSpace: FlexibleSpaceBar(
                          centerTitle: true,
                          title: Text(data['name'][langChosen],
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 16.0,
                                shadows: [
                                  Shadow(
                                    offset: Offset(2.0, 1.0),
                                    blurRadius: 2.0,
                                    color: Color.fromARGB(125, 125, 125, 125),
                                  )
                                ],
                              )),
                          background: Image.network(
                            data['photo'],
                            fit: BoxFit.cover,
                          ))),
                ];
              },
              body: Center(
                child: wikiInfo(data['name'][langChosen]),
              ),
            ),
          );
        },
      ),
    );
  }

  Widget _buildProgressIndicator() {
    return new Padding(
      padding: const EdgeInsets.all(8.0),
      child: new Center(
        child: new CircularProgressIndicator(color: Colors.green),
      ),
    );
  }

  int msFromOffset(int offset) {
    return selectedDate.millisecondsSinceEpoch + 1000 * 60 * 60 * 24 * offset;
  }

  String bdayFromOffset(int offset) {
    return DateFormat('MM.dd')
        .format(DateTime.fromMillisecondsSinceEpoch(msFromOffset(offset)));
  }

  Map<String, String> dateFromOffsetLocalized(int offset) {
    Map<String, String> dateLocalized = {};
    for (String lang in languages) {
      dateLocalized[lang] = DateFormat('d MMMM', getLocale(lang))
          .format(DateTime.fromMillisecondsSinceEpoch(msFromOffset(offset)));
    }
    return dateLocalized;
  }

  ScrollController getScrollController(int tabNum) {
    ScrollController _scrollController = _scrollController1;
    if (tabNum == 1) _scrollController = _scrollController2;
    if (tabNum == 2) _scrollController = _scrollController3;
    return _scrollController;
  }

  bool getPerformingRequestStatus(int tabNum) {
    bool result = false;
    if (!isPerformingRequest.containsKey(tabNum)) {
      isPerformingRequest[tabNum] = false;
    } else
      result = isPerformingRequest[tabNum]!;
    return result;
  }

  _getMoreData(int tabNum) async {
    String bday = bdayFromOffset(tabNum - 1);
    ScrollController _scrollController = getScrollController(tabNum);
    if (!getPerformingRequestStatus(tabNum)) {
      List<Map<String, dynamic>> items = allItems[bday] ?? [];
      setState(() => isPerformingRequest[tabNum] = true);
      List<Map<String, dynamic>> newEntries =
          await dayRequest(bday, items.length, items.length + 15);
      if (newEntries.isEmpty) {
        double edge = 50.0;
        double offsetFromBottom = _scrollController.position.maxScrollExtent -
            _scrollController.position.pixels;
        if (offsetFromBottom < edge) {
          _scrollController.animateTo(
              _scrollController.offset - (edge - offsetFromBottom),
              duration: new Duration(milliseconds: 1300),
              curve: Curves.easeInOutBack);
        }
      }
      setState(() {
        if (allItems.containsKey(bday))
          allItems[bday]!.addAll(newEntries);
        else
          allItems[bday] = newEntries;

        isPerformingRequest[tabNum] = false;
      });
    }
  }

  _selectDate(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
        locale: Locale(langChosen),
        context: context,
        initialDate: selectedDate,
        firstDate: DateTime(2021),
        lastDate: DateTime(2022),
        initialDatePickerMode: DatePickerMode.day);
    if (picked != null && picked != selectedDate)
      setState(() {
        selectedDate = picked;
      });
  }

  final languages = ['ru', 'en', 'zh', 'ru'];
  String langChosen = 'ru';
  String langNext = 'en';

  String getLocale(String lang) {
    final locales = ['ru_RU', 'en_US', 'zh_CN'];
    return locales[languages.indexOf(lang)];
  }

  _selectNextLang() {
    int index = languages.indexOf(langChosen);
    index += 1;
    if (index == 3) index = 0;
    langChosen = languages[index];
    langNext = languages[index + 1];
    MyApp.setLocale(context, langChosen);
    setState(() {});
  }

  _getBklAsset(item) {
    int num = 1;
    if (item > 300)
      num = 7;
    else
      num = (item + 50) ~/ 50;
    return (Image.asset('graphics/bk0$num.png'));
  }

  openSettings() async {
    Navigator.of(context)
        .push(MaterialPageRoute<void>(
            builder: (context) =>
                SettingsScreenWidget(preferences: preferences)))
        .then((_) => loadPreferences());
  }

  Future<List<Map<String, dynamic>>> dayRequest(
      String nowaday, int from, int to) async {
    Uri dataURL = Uri.parse(
        'http://qrcat.ru:8081/json?bdate=$nowaday&limit=15&offset=$from');
    http.Response response = await http.get(dataURL);
    var jsonResponse = jsonDecode(response.body);

    return List.generate(to - from, (index) {
      var item = jsonResponse[index];
      List emoji = item['emoji'];
      String icon = '⁉️';
      if (emoji.length > 0) {
        icon = emoji[0];
        final blankspace = icon.indexOf(' ');
        if (blankspace > 0) {
          icon = icon.substring(0, blankspace);
        }
        final dashinidex = icon.indexOf('-');
        if (dashinidex > 0) {
          icon = icon.substring(0, dashinidex);
        }
      }
      return {
        'name': jsonDecode(item['links']),
        'tags': item['tags'],
        'photo': item['photo'],
        'info': jsonDecode(item['descr']),
        'flag': item['flag'],
        'bkls': item['bklinks'],
        'icon': icon
      };
    });
  }

  Future<String> getWikiPage(String name) async {
    Uri dataURL = Uri.parse(
        'https://$langChosen.wikipedia.org/w/api.php?action=query&format=json'
        '&prop=extracts&explaintext=1&exintro=1&titles=$name');
    http.Response response = await http.get(dataURL);

    var wdjson = jsonDecode(response.body);
    String wdkey = wdjson['query']['pages'].keys.toList()[0].toString();
    String result = wdjson['query']['pages'][wdkey]['extract'];

    return result;
  }
}
