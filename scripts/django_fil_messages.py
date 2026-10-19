"""Filipino-переклади вбудованих повідомлень Django, які бачить відвідувач вітрини.

Django не постачає каталог fil, тож без цього вони падають на українську (мову за замовчуванням).
msgid — англійський оригінал Django (скрипт build_django_fil_catalog.py перевіряє, що кожен є
в каталозі Django). Значення: рядок або кортеж (однина, множина) для ngettext.
"""

MESSAGES: dict[str, str | tuple[str, str]] = {
    # --- django.core.validators ------------------------------------------------
    'Enter a valid value.': 'Maglagay ng wastong halaga.',
    'Enter a valid URL.': 'Maglagay ng wastong URL.',
    'Enter a valid integer.': 'Maglagay ng wastong buong bilang.',
    'Enter a valid email address.': 'Maglagay ng wastong email address.',
    'Ensure this value is less than or equal to %(limit_value)s.':
        'Tiyaking hindi hihigit sa %(limit_value)s ang halagang ito.',
    'Ensure this value is greater than or equal to %(limit_value)s.':
        'Tiyaking hindi bababa sa %(limit_value)s ang halagang ito.',
    'Ensure this value has at least %(limit_value)d character (it has %(show_value)d).': (
        'Tiyaking may hindi bababa sa %(limit_value)d karakter ang halagang ito (mayroon itong %(show_value)d).',
        'Tiyaking may hindi bababa sa %(limit_value)d karakter ang halagang ito (mayroon itong %(show_value)d).',
    ),
    'Ensure this value has at most %(limit_value)d character (it has %(show_value)d).': (
        'Tiyaking may hindi hihigit sa %(limit_value)d karakter ang halagang ito (mayroon itong %(show_value)d).',
        'Tiyaking may hindi hihigit sa %(limit_value)d karakter ang halagang ito (mayroon itong %(show_value)d).',
    ),
    'Enter a number.': 'Maglagay ng numero.',
    'Ensure that there are no more than %(max)s digit in total.': (
        'Tiyaking walang hihigit sa %(max)s digit sa kabuuan.',
        'Tiyaking walang hihigit sa %(max)s digit sa kabuuan.',
    ),
    'Ensure that there are no more than %(max)s decimal place.': (
        'Tiyaking walang hihigit sa %(max)s decimal place.',
        'Tiyaking walang hihigit sa %(max)s decimal place.',
    ),
    'Ensure that there are no more than %(max)s digit before the decimal point.': (
        'Tiyaking walang hihigit sa %(max)s digit bago ang decimal point.',
        'Tiyaking walang hihigit sa %(max)s digit bago ang decimal point.',
    ),
    'Null characters are not allowed.': 'Hindi pinapayagan ang mga null character.',
    # --- django.forms ------------------------------------------------------------
    'This field is required.': 'Kailangang punan ang field na ito.',
    'Enter a whole number.': 'Maglagay ng buong bilang.',
    'Enter a valid date.': 'Maglagay ng wastong petsa.',
    'Enter a valid time.': 'Maglagay ng wastong oras.',
    'Enter a valid date/time.': 'Maglagay ng wastong petsa at oras.',
    'Select a valid choice. %(value)s is not one of the available choices.':
        'Pumili ng wastong opsyon. Ang %(value)s ay wala sa mga available na opsyon.',
    'Select a valid choice. That choice is not one of the available choices.':
        'Pumili ng wastong opsyon. Ang napili mo ay wala sa mga available na opsyon.',
    'Enter a list of values.': 'Maglagay ng listahan ng mga halaga.',
    'Enter a complete value.': 'Maglagay ng kumpletong halaga.',
    # --- django.db.models --------------------------------------------------------
    'Value %(value)r is not a valid choice.': 'Ang halagang %(value)r ay hindi wastong opsyon.',
    'This field cannot be null.': 'Hindi maaaring walang laman (null) ang field na ito.',
    'This field cannot be blank.': 'Hindi maaaring blangko ang field na ito.',
    '%(model_name)s with this %(field_label)s already exists.':
        'Mayroon nang %(model_name)s na may ganitong %(field_label)s.',
    # --- widgets -------------------------------------------------------------------
    'Yes': 'Oo',
    'No': 'Hindi',
    'Unknown': 'Hindi alam',
    # --- django.contrib.auth (login, pagpapalit ng password) ----------------------
    'Please enter a correct %(username)s and password. Note that both fields may be case-sensitive.':
        'Maglagay ng tamang %(username)s at password. Tandaan na maaaring case-sensitive ang parehong field.',
    'This account is inactive.': 'Hindi aktibo ang account na ito.',
    'The two password fields didn’t match.': 'Hindi magkapareho ang dalawang password field.',
    'Your old password was entered incorrectly. Please enter it again.':
        'Maling naipasok ang dati mong password. Pakipasok itong muli.',
    'This password is too short. It must contain at least %d character.': (
        'Masyadong maikli ang password na ito. Dapat itong may hindi bababa sa %d karakter.',
        'Masyadong maikli ang password na ito. Dapat itong may hindi bababa sa %d karakter.',
    ),
    'Your password must contain at least %(min_length)d character.': (
        'Dapat may hindi bababa sa %(min_length)d karakter ang iyong password.',
        'Dapat may hindi bababa sa %(min_length)d karakter ang iyong password.',
    ),
    'The password is too similar to the %(verbose_name)s.':
        'Masyadong kahawig ng %(verbose_name)s ang password.',
    'Your password can’t be too similar to your other personal information.':
        'Hindi maaaring masyadong kahawig ng iba mong personal na impormasyon ang iyong password.',
    'This password is too common.': 'Masyadong karaniwan ang password na ito.',
    'Your password can’t be a commonly used password.':
        'Hindi maaaring karaniwang ginagamit na password ang iyong password.',
    'This password is entirely numeric.': 'Puro numero ang password na ito.',
    'Your password can’t be entirely numeric.': 'Hindi maaaring puro numero ang iyong password.',
}
