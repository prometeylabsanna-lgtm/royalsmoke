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
  /// **'ЛАУНЖ'**
  String get splashKicker;

  /// M002
  ///
  /// In uk, this message translates to:
  /// **'ROYAL SMOKE'**
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
  /// **'Лише для повнолітніх'**
  String get ageTitle;

  /// M006
  ///
  /// In uk, this message translates to:
  /// **'21+'**
  String get ageBadge;

  /// M007
  ///
  /// In uk, this message translates to:
  /// **'Застосунок є інформаційним довідником. Вміст призначений виключно для осіб, яким виповнилося 21 рік.'**
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
  /// **'ЛАУНЖ'**
  String get homeKicker;

  /// M012
  ///
  /// In uk, this message translates to:
  /// **'ROYAL\nSMOKE'**
  String get homeTitle;

  /// M013
  ///
  /// In uk, this message translates to:
  /// **'Довідник лаунжу та партнерів'**
  String get homeBody;

  /// M015
  ///
  /// In uk, this message translates to:
  /// **'Лаунж'**
  String get houseTab;

  /// M016
  ///
  /// In uk, this message translates to:
  /// **'Про лаунж'**
  String get houseKicker;

  /// M017
  ///
  /// In uk, this message translates to:
  /// **'Лаунж\nRoyal Smoke'**
  String get houseTitle;

  /// M018
  ///
  /// In uk, this message translates to:
  /// **'Royal Smoke — дім, що представляє в Україні родинні традиції з багаторічною історією. Тут можна дізнатися про походження і познайомитися з колекцією під час візиту.'**
  String get houseBody;

  /// M019
  ///
  /// In uk, this message translates to:
  /// **'Забронювати візит'**
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
  /// **'Консультації щодо історії та зберігання.'**
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
  /// **'Співпраця із закладами та професійними партнерами.'**
  String get houseBlockB2bBody;

  /// M027
  ///
  /// In uk, this message translates to:
  /// **'03'**
  String get houseBlock3Index;

  /// M028
  ///
  /// In uk, this message translates to:
  /// **'Візит'**
  String get visitTitle;

  /// M029
  ///
  /// In uk, this message translates to:
  /// **'Знайомство з домом за попереднім записом.'**
  String get houseBlockVisitBody;

  /// M030
  ///
  /// In uk, this message translates to:
  /// **'Лаунж Royal Smoke'**
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
  /// **'Ми звʼяжемося з вами, щоб підтвердити дату та час візиту.'**
  String get visitSuccessBody;

  /// M035
  ///
  /// In uk, this message translates to:
  /// **'Royal Smoke · v1.0'**
  String get appVersion;

  /// M036
  ///
  /// In uk, this message translates to:
  /// **'Royal Smoke — інформаційний довідник лаунжу. Застосунок призначений для осіб 21+.'**
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
  /// **'Пн–Нд · 11:00–22:00'**
  String get contactHours;

  /// M090
  ///
  /// In uk, this message translates to:
  /// **'Політика конфіденційності'**
  String get privacyTitle;

  /// M091
  ///
  /// In uk, this message translates to:
  /// **'Ця політика пояснює, які дані може обробляти застосунок Royal Smoke і з якою метою.'**
  String get privacyBody1;

  /// M092
  ///
  /// In uk, this message translates to:
  /// **'Royal Smoke — інформаційний довідник лаунжу. Ми збираємо лише мінімальні технічні дані, потрібні для стабільної роботи сервісу: наприклад, локально збережені дані на вашому пристрої, базові відомості про сесію та технічні журнали для діагностики збоїв.'**
  String get privacyBody2;

  /// M093
  ///
  /// In uk, this message translates to:
  /// **'Ми не створюємо рекламні профілі користувачів і не передаємо персональні дані третім сторонам для маркетингу.'**
  String get privacyBody3;

  /// M094
  ///
  /// In uk, this message translates to:
  /// **'Вміст довідника призначений виключно для повнолітніх (21+). Доступ можливий лише після підтвердження віку. Якщо ви не згодні з цими умовами — припиніть користування застосунком.'**
  String get privacyBody4;

  /// M095
  ///
  /// In uk, this message translates to:
  /// **'Запити щодо даних, доступу чи видалення інформації на пристрої можна надіслати через розділ «Контакти». Ми відповідаємо в розумні строки та в межах вимог чинного законодавства України.'**
  String get privacyBody5;

  /// M096
  ///
  /// In uk, this message translates to:
  /// **'Умови'**
  String get termsTitle;

  /// M097
  ///
  /// In uk, this message translates to:
  /// **'Користуючись застосунком Royal Smoke, ви підтверджуєте, що вам виповнилося 21 рік і що ви ознайомилися з цими умовами.'**
  String get termsBody1;

  /// M098
  ///
  /// In uk, this message translates to:
  /// **'Довідник надається з інформаційною метою: опис партнерів, історії дому, лінійок і контактів. Матеріали допомагають зорієнтуватися у світі партнерів і атмосфері простору.'**
  String get termsBody2;

  /// M099
  ///
  /// In uk, this message translates to:
  /// **'Будь-які рішення щодо відвідування дому чи ознайомлення з матеріалами приймаєте ви самостійно, з урахуванням вікових обмежень і правил закладу.'**
  String get termsBody3;

  /// M100
  ///
  /// In uk, this message translates to:
  /// **'Ми можемо оновлювати тексти, зображення та структуру розділів без попереднього окремого повідомлення. Продовження користування після оновлення означає згоду з чинною редакцією умов.'**
  String get termsBody4;

  /// M101
  ///
  /// In uk, this message translates to:
  /// **'За порушення правил користування або надання неправдивих відомостей про вік доступ до довідника може бути обмежено. Питання щодо умов — через «Контакти».'**
  String get termsBody5;

  /// M102
  ///
  /// In uk, this message translates to:
  /// **'Вікова політика'**
  String get agePolicyTitle;

  /// M103
  ///
  /// In uk, this message translates to:
  /// **'Вміст довідника Royal Smoke призначений виключно для осіб, яким виповнилося 21 рік.'**
  String get agePolicyBody1;

  /// M104
  ///
  /// In uk, this message translates to:
  /// **'Перед входом до основних розділів застосунок запитує підтвердження віку. Це обовʼязкова умова доступу до матеріалів про дім і повʼязаний контент. Якщо вам ще немає 21 року — будь ласка, залиште застосунок.'**
  String get agePolicyBody2;

  /// M105
  ///
  /// In uk, this message translates to:
  /// **'Усі сторінки мають довідковий характер і слугують для ознайомлення з партнерами дому та його простором.'**
  String get agePolicyBody3;

  /// M106
  ///
  /// In uk, this message translates to:
  /// **'Ми залишаємо за собою право оновлювати формулювання вікової політики, якщо цього вимагають зміни в законодавстві чи внутрішні стандарти дому. Актуальна версія завжди доступна в розділі «Ще».'**
  String get agePolicyBody4;

  /// M107
  ///
  /// In uk, this message translates to:
  /// **'Використовуючи застосунок, ви підтверджуєте свій вік і згоду з цією політикою. Запитання — через «Контакти».'**
  String get agePolicyBody5;

  /// M108
  ///
  /// In uk, this message translates to:
  /// **'Про застосунок'**
  String get aboutTitle;

  /// M109
  ///
  /// In uk, this message translates to:
  /// **'Royal Smoke — лаунж і цифровий довідник його світу.'**
  String get aboutBody1;

  /// M110
  ///
  /// In uk, this message translates to:
  /// **'Тут зібрано партнерів дому, короткі історії мануфактур, характер лінійок і контакти простору. Мета застосунку — допомогти спокійно зорієнтуватися: хто поруч із домом, чим вирізняється кожен партнер і як до нас звернутися.'**
  String get aboutBody2;

  /// M111
  ///
  /// In uk, this message translates to:
  /// **'Довідник створено для дорослої аудиторії 21+; він розповідає про культуру, походження та атмосферу простору, який ми підтримуємо.'**
  String get aboutBody3;

  /// M112
  ///
  /// In uk, this message translates to:
  /// **'Якщо шукаєте адресу, години роботи чи маршрут — відкрийте «Контакти». Якщо цікавлять партнери — розділ «Лаунж». А щоб зрозуміти сам простір дому — зазирніть у «Лаунж».'**
  String get aboutBody4;

  /// M113
  ///
  /// In uk, this message translates to:
  /// **'Дякуємо, що обираєте Royal Smoke як місце для знайомства.'**
  String get aboutBody5;

  /// M114
  ///
  /// In uk, this message translates to:
  /// **'Royal Smoke'**
  String get appName;

  /// M115
  ///
  /// In uk, this message translates to:
  /// **'Застосунок є інформаційним довідником.'**
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
  /// **'Дата'**
  String get dateLabel;

  /// M122
  ///
  /// In uk, this message translates to:
  /// **'ДД.ММ.РРРР'**
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
  /// **'Royal Smoke — дім, що представляє в Україні родинні традиції з багаторічною історією.'**
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
