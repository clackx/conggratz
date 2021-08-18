import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'main.dart';

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
    final alt = AppLocalizations.of(context)!;
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

    openLocaleSettings() async {
      Navigator.of(context)
          .push(MaterialPageRoute<void>(
              builder: (context) =>
                  LocaleSettingsScreenWidget(preferences: preferences)))
          .then((_) => initializePreferences());
    }

    return MaterialApp(
        theme: new ThemeData(
            primaryColor: Color(mainColor),
            brightness: Brightness.values[brightness]),
        localizationsDelegates: AppLocalizations.localizationsDelegates,
        supportedLocales: AppLocalizations.supportedLocales,
        home: Scaffold(
            appBar: AppBar(
              leading: BackButton(onPressed: () => Navigator.of(context).pop()),
              title: Text(alt.settings_screen_title),
            ),
            body: ListView(
                padding: const EdgeInsets.only(bottom: 88),
                children: <Widget>[
                  ListTile(
                      leading: Container(
                          padding: EdgeInsets.symmetric(
                              horizontal: 10.0, vertical: 10.0),
                          child: Icon(Icons.account_circle_outlined)),
                      title: Text(alt.accounting_setting),
                      subtitle: Text(alt.accounting_subtitle),
                      onTap: () => openDialog()),
                  Divider(
                    color: Colors.black,
                  ),
                  ListTile(
                      leading: Container(
                          padding: EdgeInsets.symmetric(
                              horizontal: 10.0, vertical: 10.0),
                          child: Icon(Icons.color_lens_outlined)),
                      title: Text(alt.theme_setting),
                      subtitle: Text(alt.theme_subtitle),
                      onTap: () => openColorSettings()),
                  Divider(
                    color: Colors.black,
                  ),
                  ListTile(
                      leading: Container(
                          padding: EdgeInsets.symmetric(
                              horizontal: 10.0, vertical: 10.0),
                          child: Icon(Icons.language_outlined)),
                      title: Text(alt.language_setting),
                      subtitle: Text(alt.language_subtitle),
                      onTap: () => openLocaleSettings()),
                  Divider(
                    color: Colors.black,
                  ),
                  ListTile(
                      leading: Container(
                          padding: EdgeInsets.symmetric(
                              horizontal: 10.0, vertical: 10.0),
                          child: Icon(Icons.tour_outlined)),
                      title: Text(alt.helptour),
                      subtitle: Text(alt.helptour_subtitle),
                      onTap: () => openDialog()),
                  Divider(
                    color: Colors.black,
                  ),
                  ListTile(
                      leading: Container(
                          padding: EdgeInsets.symmetric(
                              horizontal: 10.0, vertical: 10.0),
                          child: Icon(Icons.help_outline_outlined)),
                      title: Text(alt.about),
                      subtitle: Text(alt.about_subtitile),
                      onTap: () => aboutDialog()),
                ])));
  }

  openDialog() {
    showDialog<String>(
        context: context,
        builder: (BuildContext context) => AlertDialog(
                title: Text(AppLocalizations.of(context)!.comingsoon),
                content: Text(AppLocalizations.of(context)!.infuture),
                actions: <Widget>[
                  TextButton(
                    onPressed: () => Navigator.pop(context),
                    child: const Text('OK'),
                  )
                ]));
  }

  aboutDialog() {
    showDialog<String>(
        context: context,
        builder: (BuildContext context) => AlertDialog(
            title: Text(AppLocalizations.of(context)!.main_title),
            content: Text('Version 0.1.1'),
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
    final alt = AppLocalizations.of(context)!;

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
        localizationsDelegates: AppLocalizations.localizationsDelegates,
        supportedLocales: AppLocalizations.supportedLocales,
        home: Scaffold(
          appBar: AppBar(
            leading: BackButton(onPressed: () => Navigator.of(context).pop()),
            title: Text(alt.theme_setting),
          ),
          body: ListView(
              padding: const EdgeInsets.only(bottom: 88),
              children: <Widget>[
                SwitchListTile(
                  title: Text(alt.theme_darkmode),
                  value: isDark,
                  onChanged: onTumblerTap,
                ),
                Padding(
                  padding: EdgeInsets.all(16),
                  child:
                      Text(alt.theme_maincolor, style: TextStyle(fontSize: 18)),
                ),
                RadioListTile<int>(
                    title: Text(alt.theme_colororange),
                    value: Colors.orange.value,
                    groupValue: mainColor,
                    onChanged: onRadioTap),
                RadioListTile<int>(
                    title: Text(alt.theme_colorgreen),
                    value: Colors.green.value,
                    groupValue: mainColor,
                    onChanged: onRadioTap),
                RadioListTile<int>(
                    title: Text(alt.theme_colorblue),
                    value: Colors.deepPurple.value,
                    groupValue: mainColor,
                    onChanged: onRadioTap),
                RadioListTile<int>(
                    title: Text(alt.theme_coloryellow),
                    value: Colors.yellow.value,
                    groupValue: mainColor,
                    onChanged: onRadioTap),
                RadioListTile<int>(
                    title: Text(alt.theme_colorred),
                    value: Colors.red.value,
                    groupValue: mainColor,
                    onChanged: onRadioTap),
              ]),
        ));
  }
}

class LocaleSettingsScreenWidget extends StatefulWidget {
  final SharedPreferences? preferences;

  const LocaleSettingsScreenWidget({Key? key, this.preferences})
      : super(key: key);

  @override
  State<LocaleSettingsScreenWidget> createState() =>
      LocaleSettingsScreen(preferences: preferences);
}

class LocaleSettingsScreen extends State<LocaleSettingsScreenWidget> {
  final SharedPreferences? preferences;

  LocaleSettingsScreen({required this.preferences});

  bool isDark = false;

  @override
  Widget build(BuildContext context) {
    String localePref = preferences?.getString("locale") ?? 'en';
    int mainColor = preferences?.getInt("color") ?? Colors.green.value;
    int brightness = preferences?.getInt("bright") ?? Brightness.light.index;
    isDark = (brightness == 0) ? true : false;
    final alt = AppLocalizations.of(context)!;

    void onRadioTap(String? value) {
      setState(() => localePref = value!);
      preferences!.setString('locale', value!);
      preferences!.setBool('islclchngd', true);
      MyApp.setLocale(context, value);
    }

    RadioListTile rlt(locale) {
      var d = {'en': 'English', 'ru': 'Русский', 'zh': '中文'};
      return RadioListTile<String>(
          title: Container(
            height: 42,
            child: Row(children: [
              Text(locale),
              Image.asset('graphics/flag$locale.png', width: 64),
              Text(d[locale] ?? '--'),
            ]),
          ),
          value: locale,
          groupValue: localePref,
          onChanged: onRadioTap);
    }

    return MaterialApp(
        theme: new ThemeData(
            primaryColor: Color(mainColor),
            brightness: Brightness.values[brightness]),
        localizationsDelegates: AppLocalizations.localizationsDelegates,
        supportedLocales: AppLocalizations.supportedLocales,
        home: Scaffold(
          appBar: AppBar(
            leading: BackButton(onPressed: () => Navigator.of(context).pop()),
            title: Text(alt.language_setting),
          ),
          body: ListView(
              padding: const EdgeInsets.only(bottom: 88),
              children: <Widget>[
                Padding(
                  padding: EdgeInsets.all(16),
                  child: Text(alt.language_subtitle,
                      style: TextStyle(fontSize: 18)),
                ),
                rlt('en'),
                rlt('ru'),
                rlt('zh'),
              ]),
        ));
  }
}
