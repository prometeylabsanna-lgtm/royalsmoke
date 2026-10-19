#!/usr/bin/env python3
"""Fill django.po msgstr from EN/ZH translation dicts and compile messages."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCALE_DIR = ROOT / "locale"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from i18n_en import PLURALS as EN_PLURALS  # noqa: E402
from i18n_en import TRANSLATIONS as EN  # noqa: E402
from i18n_sea import SEA_LANGUAGES, SEA_PLURAL_FORMS, load_language  # noqa: E402
from i18n_zh import PLURALS as ZH_PLURALS  # noqa: E402
from i18n_zh import TRANSLATIONS as ZH  # noqa: E402


@dataclass
class PoEntry:
    comments: list[str] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)
    msgid: str = ""
    msgstr: str = ""
    msgid_plural: str = ""
    msgstr_plural: dict[int, str] = field(default_factory=dict)
    is_header: bool = False
    is_plural: bool = False


def unescape_po(text: str) -> str:
    return text.replace("\\n", "\n").replace('\\"', '"').replace("\\\\", "\\")


def escape_po(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def read_quoted(lines: list[str], start: int) -> tuple[str, int]:
    parts: list[str] = []
    i = start
    while i < len(lines):
        line = lines[i]
        if not line.startswith('"'):
            break
        m = re.match(r'"(.*)"$', line)
        parts.append(m.group(1) if m else line[1:])
        i += 1
    return unescape_po("".join(parts)), i


def format_po_string(text: str, prefix: str) -> list[str]:
    escaped = escape_po(text)
    if "\n" not in text and len(escaped) <= 70:
        return [f'{prefix} "{escaped}"']
    out = [f'{prefix} ""']
    pos = 0
    while pos < len(escaped):
        end = pos + 70
        if end < len(escaped):
            head = escaped[:end]
            # An odd run of trailing backslashes means the cut would split an
            # escape sequence (\n, \", \\). Move it before the backslash.
            if (len(head) - len(head.rstrip("\\"))) % 2:
                end -= 1
        out.append(f'"{escaped[pos:end]}"')
        pos = end
    return out


def parse_po(path: Path) -> list[PoEntry]:
    raw = path.read_text(encoding="utf-8").splitlines()
    entries: list[PoEntry] = []
    i = 0
    while i < len(raw):
        line = raw[i]
        if not line.startswith("#") and not line.startswith("msgid"):
            i += 1
            continue

        entry = PoEntry()
        while i < len(raw) and raw[i].startswith("#"):
            cl = raw[i]
            if cl.startswith("#, "):
                entry.flags = [f.strip() for f in cl[3:].split(",")]
            else:
                entry.comments.append(cl)
            i += 1

        if i >= len(raw) or not raw[i].startswith("msgid"):
            continue

        if raw[i] == 'msgid ""':
            i += 1
            if i < len(raw) and raw[i].startswith('"'):
                entry.msgid, i = read_quoted(raw, i)
            else:
                entry.msgid = ""
                entry.is_header = True
        else:
            m = re.match(r'msgid "(.*)"$', raw[i])
            entry.msgid = unescape_po(m.group(1)) if m else ""
            i += 1

        if i < len(raw) and raw[i].startswith("msgid_plural"):
            m = re.match(r'msgid_plural "(.*)"$', raw[i])
            entry.msgid_plural = unescape_po(m.group(1)) if m else ""
            entry.is_plural = True
            i += 1

        if i < len(raw) and raw[i].startswith("msgstr["):
            while i < len(raw) and raw[i].startswith("msgstr["):
                m = re.match(r'msgstr\[(\d+)\] "(.*)"$', raw[i])
                if m:
                    entry.msgstr_plural[int(m.group(1))] = unescape_po(m.group(2))
                elif raw[i].startswith('msgstr[') and raw[i].endswith('""'):
                    idx_m = re.match(r'msgstr\[(\d+)\] ""', raw[i])
                    if idx_m:
                        idx = int(idx_m.group(1))
                        i += 1
                        val, i = read_quoted(raw, i)
                        entry.msgstr_plural[idx] = val
                    continue
                i += 1
            entries.append(entry)
            continue

        if i < len(raw) and raw[i].startswith("msgstr"):
            if raw[i] == 'msgstr ""':
                i += 1
                if i < len(raw) and raw[i].startswith('"'):
                    entry.msgstr, i = read_quoted(raw, i)
                else:
                    entry.msgstr = ""
            else:
                m = re.match(r'msgstr "(.*)"$', raw[i])
                entry.msgstr = unescape_po(m.group(1)) if m else ""
                i += 1

        if entry.msgid == "" and not entry.is_header:
            entry.is_header = True
        entries.append(entry)
    return entries


def write_po(path: Path, entries: list[PoEntry], *, single_plural: bool = False) -> None:
    lines: list[str] = []
    for entry in entries:
        for c in entry.comments:
            if c.startswith("#|"):
                continue
            lines.append(c)
        flags = [f for f in entry.flags if f != "fuzzy"]
        if flags:
            lines.append("#, " + ", ".join(flags))

        if entry.is_header:
            header = entry.msgstr or entry.msgid
            lines.append('msgid ""')
            lines.append('msgstr ""')
            if header:
                for ln in format_po_string(header, "msgstr")[1:]:
                    lines.append(ln)
            lines.append("")
            continue

        if entry.is_plural:
            lines.extend(format_po_string(entry.msgid, "msgid"))
            lines.extend(format_po_string(entry.msgid_plural, "msgid_plural"))
            indices = [0] if single_plural else sorted(entry.msgstr_plural)
            for idx in indices:
                val = entry.msgstr_plural.get(idx, "")
                lines.extend(format_po_string(val, f"msgstr[{idx}]"))
            lines.append("")
            continue

        lines.extend(format_po_string(entry.msgid, "msgid"))
        lines.extend(format_po_string(entry.msgstr, "msgstr"))
        lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def lookup(msgid: str, mapping: dict[str, str]) -> str | None:
    for key in (msgid, msgid.replace("ʼ", "'"), msgid.replace("'", "ʼ")):
        if key in mapping:
            return mapping[key]
    return None


def patch_header(header: str, lang_code: str, plural_forms: str | None = None) -> str:
    if re.search(r"(?m)^Language:", header):
        header = re.sub(r"(?m)^Language:.*$", f"Language: {lang_code}\\n", header)
    else:
        header = header.rstrip("\n") + f"\nLanguage: {lang_code}\n"
    if plural_forms:
        if re.search(r"(?m)^Plural-Forms:", header):
            header = re.sub(r"(?m)^Plural-Forms:.*$", f"Plural-Forms: {plural_forms}", header)
        else:
            header = header.rstrip("\n") + f"\nPlural-Forms: {plural_forms}\n"
    return header.replace("\n\nMIME", "\nMIME")


def fill_po(
    path: Path,
    mapping: dict[str, str],
    plurals: dict[str, tuple[str, str]],
    lang_code: str,
    *,
    plural_forms: str | None = None,
    single_plural: bool | None = None,
    quiet_missing: bool = False,
) -> tuple[int, int]:
    entries = parse_po(path)
    filled = 0
    missing = 0
    if single_plural is None:
        single_plural = lang_code == "zh_Hans"
    for entry in entries:
        if entry.is_header:
            meta = entry.msgstr or entry.msgid
            entry.msgstr = patch_header(meta, lang_code, plural_forms)
            entry.msgid = ""
            entry.flags = [f for f in entry.flags if f != "fuzzy"]
            continue
        if entry.is_plural:
            pl = plurals.get(entry.msgid)
            if not pl:
                alt = entry.msgid.replace("ʼ", "'")
                pl = plurals.get(alt) or plurals.get(entry.msgid.replace("'", "ʼ"))
            if pl:
                entry.msgstr_plural = {0: pl[0], 1: pl[1]}
                entry.flags = [f for f in entry.flags if f != "fuzzy"]
                filled += 1
            else:
                missing += 1
                if not quiet_missing:
                    print(f"  MISSING plural [{lang_code}]: {entry.msgid!r}", file=sys.stderr)
            continue
        if not entry.msgid:
            continue
        tr = lookup(entry.msgid, mapping)
        if tr:
            entry.msgstr = tr
            entry.flags = [f for f in entry.flags if f != "fuzzy"]
            filled += 1
        else:
            entry.msgstr = ""
            missing += 1
            if not quiet_missing:
                print(f"  MISSING [{lang_code}]: {entry.msgid[:80]!r}", file=sys.stderr)
    write_po(path, entries, single_plural=single_plural)
    return filled, missing


def compile_messages(codes: list[str]) -> None:
    """msgfmt напряму: проєктний .venv не потрібен, а формат плейсхолдерів перевіряється."""
    for code in codes:
        base = LOCALE_DIR / code / "LC_MESSAGES"
        subprocess.run(
            ["msgfmt", "--check-format", "-o", str(base / "django.mo"), str(base / "django.po")],
            check=True,
        )


def build_targets() -> dict[str, dict]:
    """Мова → дані й параметри каталогу. en/zh обовʼязкові; ms/fil/id/vi заповнюються по сторінках."""
    targets: dict[str, dict] = {
        "en": {"mapping": EN, "plurals": EN_PLURALS, "required": True},
        "zh_Hans": {"mapping": ZH, "plurals": ZH_PLURALS, "required": True},
    }
    for code in SEA_LANGUAGES:
        mapping, plurals = load_language(code)
        forms = SEA_PLURAL_FORMS[code]
        targets[code] = {
            "mapping": mapping,
            "plurals": plurals,
            "required": False,
            "plural_forms": forms,
            "single_plural": forms.startswith("nplurals=1"),
        }
    return targets


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lang", action="append", help="locale code (default: all)")
    parser.add_argument("--strict", action="store_true", help="fail on missing strings for ms/fil/id/vi too")
    args = parser.parse_args(argv)

    targets = build_targets()
    codes = args.lang or list(targets)
    unknown = [c for c in codes if c not in targets]
    if unknown:
        print(f"Unknown locale(s): {unknown}", file=sys.stderr)
        return 1
    for code in codes:
        if not (LOCALE_DIR / code / "LC_MESSAGES" / "django.po").exists():
            print(f"Run makemessages -l {code} first.", file=sys.stderr)
            return 1

    results: dict[str, tuple[int, int]] = {}
    for code in codes:
        cfg = targets[code]
        print(f"Filling {code}…")
        results[code] = fill_po(
            LOCALE_DIR / code / "LC_MESSAGES" / "django.po",
            cfg["mapping"],
            cfg["plurals"],
            code,
            plural_forms=cfg.get("plural_forms"),
            single_plural=cfg.get("single_plural"),
            quiet_missing=not cfg["required"] and not args.strict,
        )

    print("Compiling messages…")
    compile_messages(codes)

    failed = False
    for code in codes:
        filled, missing = results[code]
        mo = LOCALE_DIR / code / "LC_MESSAGES" / "django.mo"
        print(f"  {code}: filled={filled}, missing={missing}, mo={'OK' if mo.exists() else 'MISSING'}")
        if missing and (targets[code]["required"] or args.strict):
            failed = True
    return 2 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
