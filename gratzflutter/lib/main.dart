import 'dart:async';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'dart:convert';

void main() => runApp(new MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return new MaterialApp(
      theme: new ThemeData(primarySwatch: Colors.green),
      home: new MyHomePage(),
    );
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

  @override
  void initState() {
    super.initState();
    _scrollController.addListener(() {
      if (_scrollController.position.pixels ==
          _scrollController.position.maxScrollExtent) {
        _getMoreData();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    if (items.length == 0) {
      _getMoreData();
    }
    return new Scaffold(
      appBar: AppBar(
        title: Text("Cong Gratz flutter app"),
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
                  title: Text(items[index]['name']),
                  subtitle: Text(items[index]['info']),
                  trailing: Icon(Icons.arrow_forward),
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
                          title: Text(data['name'],
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
                child: wikiInfo(data['name']),
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
}

Future<List<Map<String, dynamic>>> dayRequest(int from, int to) async {
  final now = new DateTime.now();
  String nowaday = DateFormat('MM.dd').format(now);
  Uri dataURL = Uri.parse(
      'http://qrcat.ru:8081/json?bdate=$nowaday&limit=15&offset=$from');
  http.Response response = await http.get(dataURL);
  var jsonResponse = jsonDecode(response.body);

  return List.generate(to - from, (index) {
    return {
      'name': '${jsonResponse[index]['name']}',
      'tags': jsonResponse[index]['tags'],
      'photo': jsonResponse[index]['photo'],
      'info': jsonResponse[index]['descr']
    };
  });
}

Future<String> getWikiPage(String name) async {
  Uri dataURL =
      Uri.parse('https://ru.wikipedia.org/w/api.php?action=query&format=json'
          '&prop=extracts&explaintext=1&exintro=1&titles=$name');
  http.Response response = await http.get(dataURL);

  var wdjson = jsonDecode(response.body);
  String wdkey = wdjson['query']['pages'].keys.toList()[0].toString();
  String result = wdjson['query']['pages'][wdkey]['extract'];

  return result;
}
