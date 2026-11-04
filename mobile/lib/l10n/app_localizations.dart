import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:intl/intl.dart' as intl;

import 'app_localizations_en.dart';
import 'app_localizations_fil.dart';
import 'app_localizations_id.dart';
import 'app_localizations_ms.dart';
import 'app_localizations_uk.dart';
import 'app_localizations_vi.dart';
import 'app_localizations_zh.dart';

// ignore_for_file: type=lint

/// Callers can lookup localized strings with an instance of AppLocalizations
/// returned by `AppLocalizations.of(context)`.
///
/// Applications need to include `AppLocalizations.delegate()` in their app's
/// `localizationDelegates` list, and the locales they support in the app's
/// `supportedLocales` list. For example:
///
/// ```dart
/// import 'l10n/app_localizations.dart';
///
/// return MaterialApp(
///   localizationsDelegates: AppLocalizations.localizationsDelegates,
///   supportedLocales: AppLocalizations.supportedLocales,
///   home: MyApplicationHome(),
/// );
/// ```
///
/// ## Update pubspec.yaml
///
/// Please make sure to update your pubspec.yaml to include the following
/// packages:
///
/// ```yaml
/// dependencies:
///   # Internationalization support.
///   flutter_localizations:
///     sdk: flutter
///   intl: any # Use the pinned version from flutter_localizations
///
///   # Rest of dependencies
/// ```
///
/// ## iOS Applications
///
/// iOS applications define key application metadata, including supported
/// locales, in an Info.plist file that is built into the application bundle.
/// To configure the locales supported by your app, you’ll need to edit this
/// file.
///
/// First, open your project’s ios/Runner.xcworkspace Xcode workspace file.
/// Then, in the Project Navigator, open the Info.plist file under the Runner
/// project’s Runner folder.
///
/// Next, select the Information Property List item, select Add Item from the
/// Editor menu, then select Localizations from the pop-up menu.
///
/// Select and expand the newly-created Localizations item then, for each
/// locale your application supports, add a new item and select the locale
/// you wish to add from the pop-up menu in the Value field. This list should
/// be consistent with the languages listed in the AppLocalizations.supportedLocales
/// property.
abstract class AppLocalizations {
  AppLocalizations(String locale)
    : localeName = intl.Intl.canonicalizedLocale(locale.toString());

  final String localeName;

  static AppLocalizations of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations)!;
  }

  static const LocalizationsDelegate<AppLocalizations> delegate =
      _AppLocalizationsDelegate();

  /// A list of this localizations delegate along with the default localizations
  /// delegates.
  ///
  /// Returns a list of localizations delegates containing this delegate along with
  /// GlobalMaterialLocalizations.delegate, GlobalCupertinoLocalizations.delegate,
  /// and GlobalWidgetsLocalizations.delegate.
  ///
  /// Additional delegates can be added by appending to this list in
  /// MaterialApp. This list does not have to be used at all if a custom list
  /// of delegates is preferred or required.
  static const List<LocalizationsDelegate<dynamic>> localizationsDelegates =
      <LocalizationsDelegate<dynamic>>[
        delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
      ];

  /// A list of this localizations delegate's supported locales.
  static const List<Locale> supportedLocales = <Locale>[
    Locale('en'),
    Locale('fil'),
    Locale('id'),
    Locale('ms'),
    Locale('uk'),
    Locale('vi'),
    Locale('zh'),
    Locale.fromSubtags(languageCode: 'zh', scriptCode: 'Hans'),
  ];

  /// M001
  ///
  /// In uk, this message translates to:
  /// **'ПЕРСОНАЛЬНИЙ СЕРВІС'**
  String get splashKicker;

  /// M002
  ///
  /// In uk, this message translates to:
  /// **'ROYALSMOKE'**
  String get splashTitle;

  /// M003
  ///
  /// In uk, this message translates to:
  /// **'ВІДКРИТИ'**
  String get splashOpen;

  /// M004
  ///
  /// In uk, this message translates to:
  /// **'Підтвердження віку · 21+'**
  String get ageKicker;

  /// M005
  ///
  /// In uk, this message translates to:
  /// **'Вікове обмеження 21+'**
  String get ageTitle;

  /// M006
  ///
  /// In uk, this message translates to:
  /// **'21+'**
  String get ageBadge;

  /// M007
  ///
  /// In uk, this message translates to:
  /// **'Застосунок RoyalSmoke доступний користувачам віком від 21 року.'**
  String get ageBody;

  /// M008
  ///
  /// In uk, this message translates to:
  /// **'ВИЙТИ'**
  String get ageExit;

  /// M009
  ///
  /// In uk, this message translates to:
  /// **'Мені є 21 рік'**
  String get ageConfirm;

  /// M010
  ///
  /// In uk, this message translates to:
  /// **'Продовжуючи, ви підтверджуєте свій вік і погоджуєтеся з віковою політикою.'**
  String get ageLegal;

  /// M011
  ///
  /// In uk, this message translates to:
  /// **'ПЕРСОНАЛЬНИЙ СЕРВІС'**
  String get homeKicker;

  /// M012
  ///
  /// In uk, this message translates to:
  /// **'ROYALSMOKE'**
  String get homeTitle;

  /// M013
  ///
  /// In uk, this message translates to:
  /// **'Залиште запит у застосунку — менеджер звʼяжеться з вами у зручний спосіб.'**
  String get homeBody;

  /// M015
  ///
  /// In uk, this message translates to:
  /// **'Сервіс'**
  String get houseTab;

  /// M016
  ///
  /// In uk, this message translates to:
  /// **'Про сервіс'**
  String get houseKicker;

  /// M017
  ///
  /// In uk, this message translates to:
  /// **'Сервіс\nRoyalSmoke'**
  String get houseTitle;

  /// M018
  ///
  /// In uk, this message translates to:
  /// **'RoyalSmoke — застосунок для звʼязку з персональним менеджером. Опишіть, чим вам допомогти, вкажіть контакт і зручний час — менеджер отримає запит і звʼяжеться з вами.'**
  String get houseBody;

  /// M019
  ///
  /// In uk, this message translates to:
  /// **'Залишити запит'**
  String get bookVisit;

  /// M020
  ///
  /// In uk, this message translates to:
  /// **'Контакти'**
  String get contacts;

  /// M021
  ///
  /// In uk, this message translates to:
  /// **'01'**
  String get houseBlock1Index;

  /// M022
  ///
  /// In uk, this message translates to:
  /// **'Сервіс'**
  String get houseBlockServiceTitle;

  /// M023
  ///
  /// In uk, this message translates to:
  /// **'Персональний менеджер опрацьовує кожен запит.'**
  String get houseBlockServiceBody;

  /// M024
  ///
  /// In uk, this message translates to:
  /// **'02'**
  String get houseBlock2Index;

  /// M025
  ///
  /// In uk, this message translates to:
  /// **'B2B'**
  String get houseBlockB2bTitle;

  /// M026
  ///
  /// In uk, this message translates to:
  /// **'Окремі запити від компаній і професійних партнерів.'**
  String get houseBlockB2bBody;

  /// M027
  ///
  /// In uk, this message translates to:
  /// **'03'**
  String get houseBlock3Index;

  /// M028
  ///
  /// In uk, this message translates to:
  /// **'Запит'**
  String get visitTitle;

  /// M029
  ///
  /// In uk, this message translates to:
  /// **'Форма в застосунку: тема, контакт і зручний час для звʼязку.'**
  String get houseBlockVisitBody;

  /// M030
  ///
  /// In uk, this message translates to:
  /// **'RoyalSmoke'**
  String get visitKicker;

  /// M031
  ///
  /// In uk, this message translates to:
  /// **'НОВИЙ ЗАПИТ'**
  String get visitNewRequest;

  /// M032
  ///
  /// In uk, this message translates to:
  /// **'Надіслати запит'**
  String get visitSendRequest;

  /// M033
  ///
  /// In uk, this message translates to:
  /// **'ЗАПИТ НАДІСЛАНО'**
  String get visitSuccessTitle;

  /// M034
  ///
  /// In uk, this message translates to:
  /// **'Менеджер звʼяжеться з вами за вказаними контактами.'**
  String get visitSuccessBody;

  /// M035
  ///
  /// In uk, this message translates to:
  /// **'RoyalSmoke · v1.0'**
  String get appVersion;

  /// M036
  ///
  /// In uk, this message translates to:
  /// **'RoyalSmoke — персональний сервіс: залиште запит, і менеджер звʼяжеться з вами. Вікове обмеження 21+.'**
  String get appBlurb;

  /// M037
  ///
  /// In uk, this message translates to:
  /// **''**
  String get contactAddress;

  /// M038
  ///
  /// In uk, this message translates to:
  /// **'+380 00 000 00 00'**
  String get contactPhone;

  /// M039
  ///
  /// In uk, this message translates to:
  /// **'Менеджер на звʼязку: Пн–Нд · 11:00–22:00'**
  String get contactHours;

  /// M090
  ///
  /// In uk, this message translates to:
  /// **'Політика конфіденційності'**
  String get privacyTitle;

  /// M091
  ///
  /// In uk, this message translates to:
  /// **'Ця політика пояснює, які дані обробляє застосунок RoyalSmoke і з якою метою.'**
  String get privacyBody1;

  /// M092
  ///
  /// In uk, this message translates to:
  /// **'Коли ви надсилаєте запит, ми отримуємо дані, які ви вказали у формі (імʼя, контакт для звʼязку, текст запиту, зручний час). Ці дані використовуються лише для того, щоб менеджер міг звʼязатися з вами й відповісти на запит.'**
  String get privacyBody2;

  /// M093
  ///
  /// In uk, this message translates to:
  /// **'Також застосунок зберігає на пристрої налаштування (мова, підтвердження віку) і може передавати технічні журнали для діагностики збоїв.'**
  String get privacyBody3;

  /// M094
  ///
  /// In uk, this message translates to:
  /// **'Ми не створюємо рекламні профілі та не передаємо персональні дані третім сторонам для маркетингу.'**
  String get privacyBody4;

  /// M095
  ///
  /// In uk, this message translates to:
  /// **'Запити щодо доступу до даних або їх видалення надсилайте через розділ «Контакти». Ми відповідаємо в розумні строки відповідно до чинного законодавства України.'**
  String get privacyBody5;

  /// M096
  ///
  /// In uk, this message translates to:
  /// **'Умови'**
  String get termsTitle;

  /// M097
  ///
  /// In uk, this message translates to:
  /// **'Користуючись застосунком RoyalSmoke, ви підтверджуєте, що вам виповнилося 21 рік і що ви ознайомилися з цими умовами.'**
  String get termsBody1;

  /// M098
  ///
  /// In uk, this message translates to:
  /// **'Застосунок дає змогу надіслати запит менеджеру та знайти контакти для звʼязку. Надсилаючи запит, ви погоджуєтеся, що менеджер звʼяжеться з вами за вказаними даними.'**
  String get termsBody2;

  /// M099
  ///
  /// In uk, this message translates to:
  /// **'Вказуйте достовірні контактні дані. За надання неправдивих відомостей, зокрема про вік, доступ до застосунку може бути обмежено.'**
  String get termsBody3;

  /// M100
  ///
  /// In uk, this message translates to:
  /// **'Ми можемо оновлювати тексти та структуру розділів. Продовження користування після оновлення означає згоду з чинною редакцією умов. Питання — через «Контакти».'**
  String get termsBody4;

  /// M101
  ///
  /// In uk, this message translates to:
  /// **''**
  String get termsBody5;

  /// M102
  ///
  /// In uk, this message translates to:
  /// **'Вікова політика'**
  String get agePolicyTitle;

  /// M103
  ///
  /// In uk, this message translates to:
  /// **'Застосунок RoyalSmoke доступний користувачам віком від 21 року.'**
  String get agePolicyBody1;

  /// M104
  ///
  /// In uk, this message translates to:
  /// **'Під час першого запуску застосунок просить підтвердити вік. Без підтвердження основні розділи недоступні. Якщо вам ще немає 21 року — будь ласка, не користуйтеся застосунком.'**
  String get agePolicyBody2;

  /// M105
  ///
  /// In uk, this message translates to:
  /// **'Ми можемо оновлювати формулювання вікової політики, якщо цього вимагають зміни в законодавстві. Актуальна версія завжди доступна в розділі «Ще».'**
  String get agePolicyBody3;

  /// M106
  ///
  /// In uk, this message translates to:
  /// **'Користуючись застосунком, ви підтверджуєте свій вік і згоду з цією політикою. Запитання — через «Контакти».'**
  String get agePolicyBody4;

  /// M107
  ///
  /// In uk, this message translates to:
  /// **''**
  String get agePolicyBody5;

  /// M108
  ///
  /// In uk, this message translates to:
  /// **'Про застосунок'**
  String get aboutTitle;

  /// M109
  ///
  /// In uk, this message translates to:
  /// **'RoyalSmoke — застосунок персонального сервісу.'**
  String get aboutBody1;

  /// M110
  ///
  /// In uk, this message translates to:
  /// **'У застосунку можна надіслати запит менеджеру, переглянути статус «Запит надіслано» та знайти контакти: телефон і години звʼязку.'**
  String get aboutBody2;

  /// M111
  ///
  /// In uk, this message translates to:
  /// **'Вікове обмеження застосунку — 21+.'**
  String get aboutBody3;

  /// M112
  ///
  /// In uk, this message translates to:
  /// **'Щоб залишити запит — відкрийте розділ «Запит». Щоб дізнатися, як працює сервіс, — розділ «Сервіс». Щоб звʼязатися напряму — «Контакти».'**
  String get aboutBody4;

  /// M113
  ///
  /// In uk, this message translates to:
  /// **''**
  String get aboutBody5;

  /// M114
  ///
  /// In uk, this message translates to:
  /// **'RoyalSmoke'**
  String get appName;

  /// M115
  ///
  /// In uk, this message translates to:
  /// **'Застосунок RoyalSmoke доступний користувачам віком від 21 року.'**
  String get ageBodyShort;

  /// M116
  ///
  /// In uk, this message translates to:
  /// **'Імʼя'**
  String get visitNameLabel;

  /// M117
  ///
  /// In uk, this message translates to:
  /// **'Ваше імʼя'**
  String get visitNameHint;

  /// M118
  ///
  /// In uk, this message translates to:
  /// **'Вкажіть імʼя та телефон'**
  String get visitNamePhoneError;

  /// M119
  ///
  /// In uk, this message translates to:
  /// **'Телефон'**
  String get phoneLabel;

  /// M120
  ///
  /// In uk, this message translates to:
  /// **'+380'**
  String get phonePrefix;

  /// M121
  ///
  /// In uk, this message translates to:
  /// **'Зручний час для звʼязку'**
  String get dateLabel;

  /// M122
  ///
  /// In uk, this message translates to:
  /// **'Наприклад, завтра о 18:00'**
  String get dateHint;

  /// M123
  ///
  /// In uk, this message translates to:
  /// **'Час'**
  String get timeLabel;

  /// M124
  ///
  /// In uk, this message translates to:
  /// **'ГГ:ХХ'**
  String get timeHint;

  /// M125
  ///
  /// In uk, this message translates to:
  /// **'Коментар'**
  String get commentLabel;

  /// M126
  ///
  /// In uk, this message translates to:
  /// **'Необовʼязково'**
  String get commentHint;

  /// M135
  ///
  /// In uk, this message translates to:
  /// **'Ще'**
  String get moreTitle;

  /// M136
  ///
  /// In uk, this message translates to:
  /// **'Адреса'**
  String get addressLabel;

  /// M137
  ///
  /// In uk, this message translates to:
  /// **'Прокласти маршрут'**
  String get getDirections;

  /// M138
  ///
  /// In uk, this message translates to:
  /// **'Зателефонувати'**
  String get call;

  /// M139
  ///
  /// In uk, this message translates to:
  /// **'Години'**
  String get hoursLabel;

  /// M141
  ///
  /// In uk, this message translates to:
  /// **'RoyalSmoke — застосунок для звʼязку з персональним менеджером. Опишіть, чим вам допомогти, вкажіть контакт і зручний час — менеджер отримає запит і звʼяжеться з вами.'**
  String get houseBodyShort;

  /// M143
  ///
  /// In uk, this message translates to:
  /// **'Документ'**
  String get documentFallback;

  /// M151
  ///
  /// In uk, this message translates to:
  /// **'RS'**
  String get monogramRs;

  /// M155
  ///
  /// In uk, this message translates to:
  /// **'Головна'**
  String get tabHome;

  /// M157
  ///
  /// In uk, this message translates to:
  /// **'МАПА'**
  String get mapLabel;
}

class _AppLocalizationsDelegate
    extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();

  @override
  Future<AppLocalizations> load(Locale locale) {
    return SynchronousFuture<AppLocalizations>(lookupAppLocalizations(locale));
  }

  @override
  bool isSupported(Locale locale) => <String>[
    'en',
    'fil',
    'id',
    'ms',
    'uk',
    'vi',
    'zh',
  ].contains(locale.languageCode);

  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}

AppLocalizations lookupAppLocalizations(Locale locale) {
  // Lookup logic when language+script codes are specified.
  switch (locale.languageCode) {
    case 'zh':
      {
        switch (locale.scriptCode) {
          case 'Hans':
            return AppLocalizationsZhHans();
        }
        break;
      }
  }

  // Lookup logic when only language code is specified.
  switch (locale.languageCode) {
    case 'en':
      return AppLocalizationsEn();
    case 'fil':
      return AppLocalizationsFil();
    case 'id':
      return AppLocalizationsId();
    case 'ms':
      return AppLocalizationsMs();
    case 'uk':
      return AppLocalizationsUk();
    case 'vi':
      return AppLocalizationsVi();
    case 'zh':
      return AppLocalizationsZh();
  }

  throw FlutterError(
    'AppLocalizations.delegate failed to load unsupported locale "$locale". This is likely '
    'an issue with the localizations generation tool. Please file an issue '
    'on GitHub with a reproducible sample app and the gen-l10n configuration '
    'that was used.',
  );
}
