#!/usr/bin/env python3
"""Fill django.po msgstr from EN/ZH translation dicts and compile messages."""
from __future__ import annotations

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
        out.append(f'"{escaped[pos : pos + 70]}"')
        pos += 70
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


def patch_header(header: str, lang_code: str) -> str:
    if re.search(r"(?m)^Language:", header):
        header = re.sub(r"(?m)^Language:.*$", f"Language: {lang_code}\\n", header)
    else:
        header = header.rstrip("\n") + f"\nLanguage: {lang_code}\n"
    return header.replace("\n\nMIME", "\nMIME")


def fill_po(path: Path, mapping: dict[str, str], plurals: dict[str, tuple[str, str]], lang_code: str) -> tuple[int, int]:
    entries = parse_po(path)
    filled = 0
    missing = 0
    for entry in entries:
        if entry.is_header:
            meta = entry.msgstr or entry.msgid
            entry.msgstr = patch_header(meta, lang_code)
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
            missing += 1
            print(f"  MISSING [{lang_code}]: {entry.msgid[:80]!r}", file=sys.stderr)
    write_po(path, entries, single_plural=(lang_code == "zh_Hans"))
    return filled, missing


def compile_messages() -> None:
    subprocess.run(
        [
            str(ROOT / ".venv/bin/python"),
            "manage.py",
            "compilemessages",
            "-l",
            "en",
            "-l",
            "zh_Hans",
            "--ignore=.venv",
        ],
        cwd=ROOT,
        check=True,
    )


def main() -> int:
    en_po = LOCALE_DIR / "en" / "LC_MESSAGES" / "django.po"
    zh_po = LOCALE_DIR / "zh_Hans" / "LC_MESSAGES" / "django.po"
    if not en_po.exists() or not zh_po.exists():
        print("Run makemessages first.", file=sys.stderr)
        return 1

    print("Filling EN…")
    en_filled, en_missing = fill_po(en_po, EN, EN_PLURALS, "en")
    print("Filling zh_Hans…")
    zh_filled, zh_missing = fill_po(zh_po, ZH, ZH_PLURALS, "zh_Hans")

    print("Compiling messages…")
    compile_messages()

    for lang in ("en", "zh_Hans"):
        mo = LOCALE_DIR / lang / "LC_MESSAGES" / "django.mo"
        print(f"  {mo}: {'OK' if mo.exists() else 'MISSING'}")

    print(f"\nEN: filled={en_filled}, missing={en_missing}")
    print(f"zh_Hans: filled={zh_filled}, missing={zh_missing}")
    return 0 if en_missing == 0 and zh_missing == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
