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
