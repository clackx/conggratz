import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class SettingsScreenWidget extends StatefulWidget {
  final SharedPreferences? preferences;

  const SettingsScreenWidget({Key? key, required this.preferences})
      : super(key: key);

  @override
  State<SettingsScreenWidget> createState() =>
      SettingsScreen(preferences: preferences);
}

class SettingsScreen extends State<SettingsScreenWidget> {
  final SharedPreferences? preferences;

  SettingsScreen({required this.preferences});

  @override
  Widget build(BuildContext context) {
    int mainColor = 0;
    int brightness = 0;

    void initializePreferences() async {
      mainColor = preferences?.getInt("color") ?? Colors.green.value;
      brightness = preferences?.getInt("bright") ?? Brightness.light.index;
      setState(() {});
    }

    initializePreferences();

    openColorSettings() async {
      Navigator.of(context)
          .push(MaterialPageRoute<void>(
              builder: (context) =>
                  ColorSettingsScreenWidget(preferences: preferences)))
          .then((_) => initializePreferences());
    }

    return MaterialApp(
        theme: new ThemeData(
            primaryColor: Color(mainColor),
            brightness: Brightness.values[brightness]),
        home: Scaffold(
            appBar: AppBar(
              automaticallyImplyLeading: false,
              title: const Text('Bottom App Bar Demo'),
            ),
            body: ListView(
                padding: const EdgeInsets.only(bottom: 88),
                children: <Widget>[
                  ListTile(
                      leading: Container(
                          padding: EdgeInsets.symmetric(
                              horizontal: 10.0, vertical: 10.0),
                          child: Icon(Icons.account_circle_outlined)),
                      title: Text('Accounting'),
                      subtitle: Text('Log in for store your favorites'),
                      onTap: () => openDialog()),
                  Divider(
                    color: Colors.black,
                  ),
                  ListTile(
                      leading: Container(
                          padding: EdgeInsets.symmetric(
                              horizontal: 10.0, vertical: 10.0),
                          child: Icon(Icons.color_lens_outlined)),
                      title: Text('Theme colors'),
                      subtitle: Text('Choose colors or change theme'),
                      onTap: () => openColorSettings()),
                  Divider(
                    color: Colors.black,
                  ),
                  ListTile(
                      leading: Container(
                          padding: EdgeInsets.symmetric(
                              horizontal: 10.0, vertical: 10.0),
                          child: Icon(Icons.language_outlined)),
                      title: Text('Language'),
                      subtitle: Text('Set logic language and ui language'),
                      onTap: () => openDialog()),
                  Divider(
                    color: Colors.black,
                  ),
                  ListTile(
                      leading: Container(
                          padding: EdgeInsets.symmetric(
                              horizontal: 10.0, vertical: 10.0),
                          child: Icon(Icons.tour_outlined)),
                      title: Text('Help'),
                      subtitle: Text('App tour'),
                      onTap: () => openDialog()),
                  Divider(
                    color: Colors.black,
                  ),
                  ListTile(
                      leading: Container(
                          padding: EdgeInsets.symmetric(
                              horizontal: 10.0, vertical: 10.0),
                          child: Icon(Icons.help_outline_outlined)),
                      title: Text('About'),
                      subtitle: Text('Credits'),
                      onTap: () => openDialog()),
                ])));
  }

  openDialog() {
    showDialog<String>(
        context: context,
        builder: (BuildContext context) => AlertDialog(
                title: const Text('Coming soon..'),
                content: const Text('In future releases'),
                actions: <Widget>[
                  TextButton(
                    onPressed: () => Navigator.pop(context),
                    child: const Text('OK'),
                  )
                ]));
  }
}

class ColorSettingsScreenWidget extends StatefulWidget {
  final SharedPreferences? preferences;

  const ColorSettingsScreenWidget({Key? key, required this.preferences})
      : super(key: key);

  @override
  State<ColorSettingsScreenWidget> createState() =>
      ColorSettingsScreen(preferences: preferences);
}

class ColorSettingsScreen extends State<ColorSettingsScreenWidget> {
  final SharedPreferences? preferences;

  ColorSettingsScreen({required this.preferences});

  bool isDark = false;

  @override
  Widget build(BuildContext context) {
    int mainColor = preferences?.getInt("color") ?? Colors.green.value;
    int brightness = preferences?.getInt("bright") ?? Brightness.light.index;
    isDark = (brightness == 0) ? true : false;

    void onRadioTap(int? value) {
      setState(() => mainColor = value!);
      preferences!.setInt('color', value!);
    }

    void onTumblerTap(bool? value) {
      setState(() => isDark = value!);
      int brightness = isDark ? Brightness.dark.index : Brightness.light.index;
      preferences!.setInt('bright', brightness);
    }

    return MaterialApp(
        theme: new ThemeData(
            primaryColor: Color(mainColor),
            brightness: Brightness.values[brightness]),
        home: Scaffold(
          appBar: AppBar(
            automaticallyImplyLeading: false,
            title: const Text('Bottom App Bar Demo'),
          ),
          body: ListView(
              padding: const EdgeInsets.only(bottom: 88),
              children: <Widget>[
                SwitchListTile(
                  title: const Text('Dark Theme'),
                  value: isDark,
                  onChanged: onTumblerTap,
                ),
                const Padding(
                  padding: EdgeInsets.all(16),
                  child: Text('Main color suchenka'),
                ),
                RadioListTile<int>(
                    title: const Text('Orange'),
                    value: Colors.orange.value,
                    groupValue: mainColor,
                    onChanged: onRadioTap),
                RadioListTile<int>(
                    title: const Text('Green'),
                    value: Colors.green.value,
                    groupValue: mainColor,
                    onChanged: onRadioTap),
                RadioListTile<int>(
                    title: const Text('Violet'),
                    value: Colors.deepPurple.value,
                    groupValue: mainColor,
                    onChanged: onRadioTap),
                RadioListTile<int>(
                    title: const Text('Yellow'),
                    value: Colors.yellow.value,
                    groupValue: mainColor,
                    onChanged: onRadioTap),
                RadioListTile<int>(
                    title: const Text('Red'),
                    value: Colors.red.value,
                    groupValue: mainColor,
                    onChanged: onRadioTap),
              ]),
        ));
  }
}
