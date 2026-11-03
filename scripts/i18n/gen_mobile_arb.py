"""Генерує ARB мобільного застосунку з таблиць M001–M159. Не редагувати ARB вручну."""

from __future__ import annotations

import json
from pathlib import Path

from mobile_tables import ROOT, load_phrases

ARB_DIR = ROOT / 'mobile' / 'lib' / 'l10n'

# Стабільні camelCase-ключі. Опис @key містить M-ID.
KEYS: dict[str, str] = {
    'M001': 'splashKicker',
    'M002': 'splashTitle',
    'M003': 'splashOpen',
    'M004': 'ageKicker',
    'M005': 'ageTitle',
    'M006': 'ageBadge',
    'M007': 'ageBody',
    'M008': 'ageExit',
    'M009': 'ageConfirm',
    'M010': 'ageLegal',
    'M011': 'homeKicker',
    'M012': 'homeTitle',
    'M013': 'homeBody',
    'M014': 'brands',
    'M015': 'houseTab',
    'M016': 'houseKicker',
    'M017': 'houseTitle',
    'M018': 'houseBody',
    'M019': 'bookVisit',
    'M020': 'contacts',
    'M021': 'houseBlock1Index',
    'M022': 'houseBlockServiceTitle',
    'M023': 'houseBlockServiceBody',
    'M024': 'houseBlock2Index',
    'M025': 'houseBlockB2bTitle',
    'M026': 'houseBlockB2bBody',
    'M027': 'houseBlock3Index',
    'M028': 'visitTitle',
    'M029': 'houseBlockVisitBody',
    'M030': 'visitKicker',
    'M031': 'visitNewRequest',
    'M032': 'visitSendRequest',
    'M033': 'visitSuccessTitle',
    'M034': 'visitSuccessBody',
    'M035': 'appVersion',
    'M036': 'appBlurb',
    'M037': 'contactAddress',
    'M038': 'contactPhone',
    'M039': 'contactHours',
    'M040': 'brandAjName',
    'M041': 'brandAjShort',
    'M042': 'countryNicaragua',
    'M043': 'brandAjHeritage',
    'M044': 'factOrigin',
    'M045': 'factOriginEsteli',
    'M046': 'factFounded',
    'M047': 'factFoundedAj',
    'M048': 'factFamily',
    'M049': 'factFamilyAj',
    'M050': 'factLineCharacter',
    'M051': 'factLineCharacterAj',
    'M052': 'lineAjNewWorld',
    'M053': 'lineAjBellasArtes',
    'M054': 'lineAjEnclave',
    'M055': 'lineAjSanLotano',
    'M056': 'brandOlivaName',
    'M057': 'brandOlivaMono',
    'M058': 'brandOlivaHeritage',
    'M059': 'factTradition',
    'M060': 'factTraditionOliva',
    'M061': 'factProduction',
    'M062': 'factProductionOliva',
    'M063': 'factLineCharacterOliva',
    'M064': 'lineOlivaSerieV',
    'M065': 'lineOlivaSerieG',
    'M066': 'lineOlivaMasterBlends',
    'M067': 'lineOlivaSerieO',
    'M068': 'brandPerdomoName',
    'M069': 'brandPerdomoMono',
    'M070': 'brandPerdomoHeritage',
    'M071': 'factFoundedPerdomo',
    'M072': 'factFounder',
    'M073': 'factFounderPerdomo',
    'M074': 'factFeature',
    'M075': 'factFeaturePerdomo',
    'M076': 'linePerdomoReserve',
    'M077': 'linePerdomoHabano',
    'M078': 'linePerdomoLot23',
    'M079': 'brandTurrentName',
    'M080': 'brandTurrentMono',
    'M081': 'countryMexico',
    'M082': 'brandTurrentHeritage',
    'M083': 'factOriginTurrent',
    'M084': 'factFamilyTurrent',
    'M085': 'factLineCharacterTurrent',
    'M086': 'lineTurrent1942',
    'M087': 'lineTurrent1880',
    'M088': 'lineTurrentOrigin',
    'M089': 'lineTurrent1901',
    'M090': 'privacyTitle',
    'M091': 'privacyBody1',
    'M092': 'privacyBody2',
    'M093': 'privacyBody3',
    'M094': 'privacyBody4',
    'M095': 'privacyBody5',
    'M096': 'termsTitle',
    'M097': 'termsBody1',
    'M098': 'termsBody2',
    'M099': 'termsBody3',
    'M100': 'termsBody4',
    'M101': 'termsBody5',
    'M102': 'agePolicyTitle',
    'M103': 'agePolicyBody1',
    'M104': 'agePolicyBody2',
    'M105': 'agePolicyBody3',
    'M106': 'agePolicyBody4',
    'M107': 'agePolicyBody5',
    'M108': 'aboutTitle',
    'M109': 'aboutBody1',
    'M110': 'aboutBody2',
    'M111': 'aboutBody3',
    'M112': 'aboutBody4',
    'M113': 'aboutBody5',
    'M114': 'appName',
    'M115': 'ageBodyShort',
    'M116': 'visitNameLabel',
    'M117': 'visitNameHint',
    'M118': 'visitNamePhoneError',
    'M119': 'phoneLabel',
    'M120': 'phonePrefix',
    'M121': 'dateLabel',
    'M122': 'dateHint',
    'M123': 'timeLabel',
    'M124': 'timeHint',
    'M125': 'commentLabel',
    'M126': 'commentHint',
    'M127': 'brandNotFound',
    'M128': 'patternRoyal',
    'M129': 'brandsBack',
    'M130': 'factsKicker',
    'M131': 'linesKicker',
    'M132': 'allBrands',
    'M133': 'partnersKicker',
    'M134': 'filterAll',
    'M135': 'moreTitle',
    'M136': 'addressLabel',
    'M137': 'getDirections',
    'M138': 'call',
    'M139': 'hoursLabel',
    'M140': 'partnersSection',
    'M141': 'houseBodyShort',
    'M142': 'savedBrands',
    'M143': 'documentFallback',
    'M144': 'offlineLocalCatalog',
    'M145': 'offlineUpdated',
    'M146': 'offlineKicker',
    'M147': 'offlineTitle',
    'M148': 'offlineSubtitle',
    'M149': 'offlineEmpty',
    'M150': 'savedBadge',
    'M151': 'monogramRs',
    'M152': 'emptySearchTitle',
    'M153': 'emptySearchBody',
    'M154': 'offlineMode',
    'M155': 'tabHome',
    'M156': 'searchBrandHint',
    'M157': 'mapLabel',
    'M158': 'packageDescription',
    'M159': 'webDescription',
}

LOCALE_FILE = {
    'uk': 'app_uk.arb',
    'en': 'app_en.arb',
    'zh-hans': 'app_zh.arb',
    'zh_Hans': 'app_zh_Hans.arb',
    'ms': 'app_ms.arb',
    'fil': 'app_fil.arb',
    'id': 'app_id.arb',
    'vi': 'app_vi.arb',
}


def _locale_tag(code: str) -> str:
    if code == 'zh_Hans':
        return 'zh_Hans'
    if code == 'zh-hans':
        return 'zh'
    return code


def _source_lang(code: str) -> str:
    if code in ('zh-hans', 'zh_Hans'):
        return 'zh-hans'
    return code


def _dump(locale_code: str, phrases: list) -> str:
    lang = _source_lang(locale_code)
    lines = ['{', f'  "@@locale": {json.dumps(_locale_tag(locale_code))},']
    for item in phrases:
        key = KEYS[item.id]
        value = item.text(lang)
        lines.append(f'  {json.dumps(key, ensure_ascii=False)}: {json.dumps(value, ensure_ascii=False)},')
        meta: dict = {'description': item.id}
        if '{date}' in value:
            meta['placeholders'] = {'date': {'type': 'String'}}
        lines.append(f'  {json.dumps("@" + key)}: {json.dumps(meta, ensure_ascii=False)},')
    lines[-1] = lines[-1].rstrip(',')
    lines.append('}')
    lines.append('')
    return '\n'.join(lines)


def main() -> None:
    phrases = load_phrases()
    if set(KEYS) != {item.id for item in phrases}:
        raise SystemExit('KEYS не збігаються з M001–M159')
    if len(set(KEYS.values())) != len(KEYS):
        raise SystemExit('Дублі ключів ARB')
    ARB_DIR.mkdir(parents=True, exist_ok=True)
    for code, filename in LOCALE_FILE.items():
        path = ARB_DIR / filename
        path.write_text(_dump(code, phrases), encoding='utf-8')
        print(path.relative_to(ROOT), 'lines', path.read_text(encoding='utf-8').count('\n'))


if __name__ == '__main__':
    main()
