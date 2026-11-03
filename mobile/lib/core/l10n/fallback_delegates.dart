import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

/// Filipino входить у Material і Cupertino з Flutter 3.35.
/// Якщо SDK його не знає, підставляємо англійські системні рядки, щоб застосунок не падав.
class FilMaterialFallbackDelegate extends LocalizationsDelegate<MaterialLocalizations> {
  const FilMaterialFallbackDelegate();

  @override
  bool isSupported(Locale locale) {
    return locale.languageCode == 'fil' &&
        !GlobalMaterialLocalizations.delegate.isSupported(locale);
  }

  @override
  Future<MaterialLocalizations> load(Locale locale) {
    return GlobalMaterialLocalizations.delegate.load(const Locale('en'));
  }

  @override
  bool shouldReload(FilMaterialFallbackDelegate old) => false;
}

class FilCupertinoFallbackDelegate extends LocalizationsDelegate<CupertinoLocalizations> {
  const FilCupertinoFallbackDelegate();

  @override
  bool isSupported(Locale locale) {
    return locale.languageCode == 'fil' &&
        !GlobalCupertinoLocalizations.delegate.isSupported(locale);
  }

  @override
  Future<CupertinoLocalizations> load(Locale locale) {
    return GlobalCupertinoLocalizations.delegate.load(const Locale('en'));
  }

  @override
  bool shouldReload(FilCupertinoFallbackDelegate old) => false;
}

class FilWidgetsFallbackDelegate extends LocalizationsDelegate<WidgetsLocalizations> {
  const FilWidgetsFallbackDelegate();

  @override
  bool isSupported(Locale locale) {
    return locale.languageCode == 'fil' &&
        !GlobalWidgetsLocalizations.delegate.isSupported(locale);
  }

  @override
  Future<WidgetsLocalizations> load(Locale locale) {
    return GlobalWidgetsLocalizations.delegate.load(const Locale('en'));
  }

  @override
  bool shouldReload(FilWidgetsFallbackDelegate old) => false;
}
