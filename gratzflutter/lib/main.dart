import 'dart:async';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:intl/date_symbol_data_local.dart';
import 'package:intl/intl.dart';
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

void main() => runApp(new MyApp());

class MyApp extends StatefulWidget {
  @override
  _AppState createState() => new _AppState();

  static void setTheme(BuildContext context, int newColor, int brightness) {
    _AppState? state = context.findAncestorStateOfType<_AppState>()!;
    state.setState(() {
      state._color = newColor;
      state._brightness = brightness;
    });
  }
}

class _AppState extends State<MyApp> {
  int _color = Colors.green.value;
  int _brightness = Brightness.light.index;

  @override
  Widget build(BuildContext context) {
    return new MaterialApp(
        theme: new ThemeData(
            primaryColor: Color(_color),
            brightness: Brightness.values[_brightness],
        ),
        home: new MyHomePage());
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  var items = [];
  ScrollController _scrollController = new ScrollController();
  bool isPerformingRequest = false;

  SharedPreferences? preferences;
  int mainColor = Colors.green.value;
  int brightness = Brightness.dark.index;

  Future<void> initializePreference() async {
    preferences = await SharedPreferences.getInstance();
    int? savedColor = this.preferences?.getInt("color");
    int? savedBright = this.preferences?.getInt("bright");
    // print ('>>>>'+savedColor.toString()+'//'+savedBright.toString());
    mainColor = savedColor ?? Colors.green.value;
    brightness = savedBright ?? Brightness.light.index;
    this.preferences?.setInt("color", mainColor);
    this.preferences?.setInt("bright", brightness);
    MyApp.setTheme(context, mainColor, brightness);
  }

  @override
  void initState() {
    super.initState();
    initializeDateFormatting('ru_RU');
    initializePreference().whenComplete(() {
      setState(() {});
    });
    _scrollController.addListener(() {
      if (_scrollController.position.pixels ==
          _scrollController.position.maxScrollExtent) {
        _getMoreData();
      }
    });
  }

  String apptitle = "Cong Gratz flutter app";
  String born = " родились";
  DateTime selectedDate = DateTime.now();

  @override
  Widget build(BuildContext context) {
    if (items.length == 0) {
      _getMoreData();
    }
    return new Scaffold(
      appBar: AppBar(
        title: Text(apptitle),
        elevation: 15.0,
        actions: [
          IconButton(
              icon: Icon(Icons.ac_unit), onPressed: () => _changeColor()),
          IconButton(
              icon: Image.asset('graphics/clndr2.png'),
              onPressed: () => _selectDate(context)),
          IconButton(
              icon: Image.asset('graphics/flag$langNext.png'),
              onPressed: () => _selectNextLang()),
          Image.asset('graphics/blank.png')
        ],
      ),
      body: ListView.builder(
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
        controller: _scrollController,
      ),
    );
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

  _getMoreData() async {
    if (!isPerformingRequest) {
      setState(() => isPerformingRequest = true);
      List<Map<String, dynamic>> newEntries =
          await dayRequest(items.length, items.length + 15);
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
        items.addAll(newEntries);
        isPerformingRequest = false;
      });
    }
  }

  _selectDate(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
        context: context,
        initialDate: selectedDate,
        firstDate: DateTime(2021),
        lastDate: DateTime(2022),
        initialDatePickerMode: DatePickerMode.day);
    if (picked != null && picked != selectedDate)
      setState(() {
        selectedDate = picked;
        items = [];
      });
  }

  final languages = ['ru', 'en', 'zh', 'ru'];
  String langChosen = 'ru';
  String langNext = 'en';

  _selectNextLang() {
    int index = languages.indexOf(langChosen);
    index += 1;
    if (index == 3) index = 0;
    langChosen = languages[index];
    langNext = languages[index + 1];
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

  _changeColor() {
    List colors = [
      Colors.green.value,
      Colors.blue.value,
      Colors.yellow.value,
      Colors.orange.value,
      Colors.red.value,
      Colors.green.value
    ];
    int _i = colors.indexOf(mainColor);
    _i += 1;
    mainColor = colors[_i];
    if (_i > 4) brightness = (brightness - 1).abs();

    this.preferences?.setInt("color", mainColor);
    this.preferences?.setInt("bright", brightness);
    setState(() {});
    MyApp.setTheme(context, mainColor, brightness);
  }

  Future<List<Map<String, dynamic>>> dayRequest(int from, int to) async {
    String nowaday = DateFormat('MM.dd').format(selectedDate);
    apptitle = DateFormat('d MMMM', 'ru_RU').format(selectedDate) + born;
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
