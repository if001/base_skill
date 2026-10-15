#!/usr/bin/env python3
"""文書の検査を補助する。標準ライブラリのみを使う。

サブコマンド:
  glossary-to-prh  docs/D2/GLOSSARY.md の「使わない言い換え」列から textlint-rule-prh の辞書を生成する
  table-length     表のセルの文の長さを検査する（textlint の sentence-length は表のセルを検査しないため）

使い方:
  python3 doc_check.py glossary-to-prh [--glossary docs/D2/GLOSSARY.md] [--out .textlint/prh.generated.yml]
  python3 doc_check.py table-length [--max 80] [paths ...]   # 既定は docs/D1 docs/D2

終了コード: 違反または生成時の ERROR があれば 1、それ以外は 0。
"""
from __future__ import annotations

import argparse
import os
import re
import sys

ID_ONLY = re.compile(r"^[\s`*]*((?:C|OV|FR|NFR|AC|UI|ADR|W)(?:-[A-Z]{1,6})?-\d+[\s,、`*]*)+$")


def split_row(line: str) -> list[str]:
    s = line.strip()
    if not (s.startswith("|") and s.endswith("|")):
        return []
    # エスケープされたパイプとコード内のパイプを考慮した簡易分割
    cells, buf, in_code = [], "", False
    for i, ch in enumerate(s[1:-1]):
        if ch == "`":
            in_code = not in_code
        if ch == "|" and not in_code and (i == 0 or s[i] != "\\"):
            cells.append(buf.strip())
            buf = ""
        else:
            buf += ch
    cells.append(buf.strip())
    return cells


def is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells if c)


def read_tables(path: str):
    """(行番号, ヘッダー, セル) を返す。"""
    lines = open(path, encoding="utf-8").read().splitlines()
    header, in_fence = None, False
    for i, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            header = None
            continue
        if in_fence:
            continue
        cells = split_row(line)
        if not cells:
            header = None
            continue
        if header is None:
            header = cells
            continue
        if is_separator(cells):
            continue
        yield i, header, cells


def plain(text: str) -> str:
    text = re.sub(r"`[^`]*`", "", text)          # コード
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # リンク
    text = re.sub(r"https?://\S+", "", text)
    return text.replace("**", "").replace("<br>", "。").strip()


# ---------------------------------------------------------------- glossary-to-prh

def glossary_to_prh(glossary: str, out: str) -> int:
    if not os.path.isfile(glossary):
        print(f"ERROR: 用語集がない: {glossary}")
        return 1
    terms, aliases = [], {}
    for _, header, cells in read_tables(glossary):
        h = [c.replace("*", "") for c in header]
        if "用語" not in h or "使わない言い換え" not in h:
            continue
        term = plain(cells[h.index("用語")]) if len(cells) > h.index("用語") else ""
        if not term:
            continue
        terms.append(term)
        raw = cells[h.index("使わない言い換え")] if len(cells) > h.index("使わない言い換え") else ""
        aliases[term] = [a.strip() for a in re.split(r"[、,，]", plain(raw)) if a.strip() and a.strip() not in {"-", "なし"}]

    errors, warns, rules = 0, [], []
    term_set = set(terms)
    for term in terms:
        pats = []
        for a in aliases.get(term, []):
            if a in term_set:
                print(f"ERROR: 「{a}」は用語として定義されているため、「{term}」の言い換えにできない")
                errors += 1
                continue
            if len(a) <= 3 and re.fullmatch(r"[\u3040-\u30ffー]+", a):
                warns.append(f"WARN: 「{a}」（{term} の言い換え）は短いかなの語で、他の語の一部として誤検出されやすい")
            pats.append(a)
        if pats:
            rules.append((term, pats))

    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write("# このファイルは doc_check.py glossary-to-prh が docs/D2/GLOSSARY.md から生成する。手で編集しない。\n")
        f.write("version: 1\nrules:\n")
        for term, pats in rules:
            f.write(f"  - expected: {yaml_str(term)}\n    patterns:\n")
            for p in pats:
                f.write(f"      - {yaml_str(p)}\n")
            f.write(f"    prh: {yaml_str('用語集（GLOSSARY.md）の用語「' + term + '」を使う')}\n")
    for w in warns:
        print(w)
    print(f"生成：{out}（用語 {len(terms)} 件、言い換えの規則 {len(rules)} 件）")
    return 1 if errors else 0


def yaml_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


# ---------------------------------------------------------------- table-length

def table_length(paths: list[str], max_len: int) -> int:
    files = []
    for p in paths:
        if os.path.isdir(p):
            for d, _, fs in os.walk(p):
                files += [os.path.join(d, f) for f in fs if f.endswith(".md")]
        elif p.endswith(".md") and os.path.isfile(p):
            files.append(p)
    count = 0
    for path in sorted(files):
        for line_no, header, cells in read_tables(path):
            for ci, cell in enumerate(cells):
                if ID_ONLY.match(cell or "-"):
                    continue
                for sentence in re.split(r"(?<=[。！？])", plain(cell)):
                    n = len(sentence.strip())
                    if n > max_len:
                        col = header[ci] if ci < len(header) else str(ci + 1)
                        print(f"{path}:{line_no}  列「{col}」の文が {n} 字（上限 {max_len}）：{sentence.strip()[:30]}…")
                        count += 1
    print(f"表のセルの文の長さ：違反 {count} 件")
    return 1 if count else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("glossary-to-prh")
    g.add_argument("--glossary", default="docs/D2/GLOSSARY.md")
    g.add_argument("--out", default=".textlint/prh.generated.yml")
    t = sub.add_parser("table-length")
    t.add_argument("--max", type=int, default=80)
    t.add_argument("paths", nargs="*", default=["docs/D1", "docs/D2"])
    a = ap.parse_args()
    if a.cmd == "glossary-to-prh":
        return glossary_to_prh(a.glossary, a.out)
    return table_length(a.paths, a.max)


if __name__ == "__main__":
    sys.exit(main())
