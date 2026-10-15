#!/usr/bin/env python3
"""ID のトレーサビリティを機械的に検査する。

ID-Rules.md（document-interview/references/ID-Rules.md）の規則に従い、
一次ドキュメント → docs → 計画 → Issue → テスト の ID の定義と参照を集計し、
次を報告する。

- ERROR : 未定義の ID への参照、所有文書内での重複定義
- WARN  : 下流で参照されていない ID、由来（上流 ID）のない定義
- INFO  : 参考情報（テストのない AC / UI、ID を持たない Issue など）

使い方:
    python3 trace_check.py [--root .] [--format md|json] [--strict]

終了コード: ERROR があれば 1（--strict では WARN でも 1）、それ以外は 0。
標準ライブラリのみを使う。
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import sys
from dataclasses import dataclass, field

ID_RE = re.compile(r"(?<![A-Za-z0-9_-])((?:C|OV|FR|NFR|AC|UI|ADR|W)(?:-[A-Z]{1,6})?-\d+)(?![0-9-])")

# 接頭辞ごとの所有文書（定義を置く文書）
# 標準の配置は docs/D1/（Overview）と docs/D2/（設計文書と計画）。
# 旧配置（docs/ 直下）のプロジェクトも検査できるよう、両方を受け付ける。
def _d2(name: str) -> list[str]:
    return [f"docs/D2/{name}", f"docs/{name}"]


OWNERS = {
    "C": ["spec/**/*.md", "spec/*.md"],
    "OV": ["docs/D1/PROJECT_OVERVIEW.md", "docs/PROJECT_OVERVIEW.md"],
    "FR": _d2("REQUIREMENTS.md"),
    "NFR": _d2("REQUIREMENTS.md"),
    "AC": _d2("REQUIREMENTS.md"),
    "UI": _d2("UI_GUIDELINES.md"),
    "ADR": _d2("ARCHITECTURE.md") + ["docs/D2/adr/*.md", "docs/D2/adr/**/*.md", "docs/adr/*.md", "docs/adr/**/*.md"],
    "W": _d2("IMPLEMENTATION_PLAN.md"),
}
PLAN_FILES = set(_d2("IMPLEMENTATION_PLAN.md"))

# 定義と同じ行に書くべき上流の接頭辞
UPSTREAM = {
    "OV": {"C"},
    "FR": {"OV", "C"},
    "NFR": {"OV", "C"},
    "AC": {"FR", "NFR"},
    "UI": {"FR", "NFR", "C", "OV"},
    "ADR": {"FR", "NFR"},
    "W": {"FR", "NFR", "UI"},
}

SCAN_DIRS = ["spec", "docs", "issues", "src", "test", "tests", "e2e", "app", "lib"]
EXCLUDE_DIRS = {"node_modules", ".git", "dist", "build", ".wrangler", "coverage", ".next", ".svelte-kit"}
# docs/work/ は作業中の記録（正ではない）。旧配置の作業用ディレクトリも除外する。
EXCLUDE_PATHS = ["docs/work", "docs/reports", "docs/note", "docs/notes", "docs/planning"]
EXTS = {".md", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".py", ".go", ".rs", ".java",
        ".kt", ".rb", ".php", ".vue", ".svelte", ".sql", ".swift", ".dart"}


def prefix_of(id_: str) -> str:
    return id_.split("-", 1)[0]


@dataclass
class Definition:
    id: str
    path: str
    line: int
    text: str
    deprecated: bool


@dataclass
class Ref:
    id: str
    path: str
    line: int
    kind: str  # spec / doc / plan / issue / test / src


@dataclass
class Report:
    errors: list = field(default_factory=list)
    warns: list = field(default_factory=list)
    infos: list = field(default_factory=list)


def matches(rel: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(rel, p) for p in patterns)


def walk(root: str):
    for d in SCAN_DIRS:
        base = os.path.join(root, d)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            rel_dir = os.path.relpath(dirpath, root).replace(os.sep, "/")
            dirnames[:] = [x for x in dirnames if x not in EXCLUDE_DIRS
                           and not any((rel_dir + "/" + x).startswith(e) for e in EXCLUDE_PATHS)]
            if any(rel_dir == e or rel_dir.startswith(e + "/") for e in EXCLUDE_PATHS):
                continue
            for fn in filenames:
                if os.path.splitext(fn)[1] in EXTS:
                    full = os.path.join(dirpath, fn)
                    yield full, os.path.relpath(full, root).replace(os.sep, "/")


def kind_of(rel: str) -> str:
    name = rel.rsplit("/", 1)[-1]
    if rel.startswith("spec/"):
        return "spec"
    if rel in PLAN_FILES:
        return "plan"
    if rel.startswith("issues/"):
        return "issue"
    if (rel.split("/", 1)[0] in {"test", "tests", "e2e"} or re.search(r"\.(test|spec)\.[a-z]+$", name)
            or re.search(r"_test\.[a-z]+$", name) or "/__tests__/" in rel):
        return "test"
    if rel.startswith("docs/"):
        return "doc"
    return "src"


def is_definition_line(line: str, id_: str) -> bool:
    s = line.strip()
    token = r"[*`]*" + re.escape(id_) + r"[*`]*"
    if s.startswith("|"):
        cells = [c.strip() for c in s.strip("|").split("|")]
        return bool(cells) and re.fullmatch(token + r"(\s*[（(].*)?", cells[0]) is not None
    if re.match(r"#{1,6}\s+" + token + r"(?![0-9-])", s):
        return True
    if re.match(r"[-*+]\s+(\[[ xX]\]\s+)?" + token + r"(?![0-9-])", s):
        return True
    return False


def frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[3:end]
    return ""


def analyze(root: str) -> tuple[Report, dict]:
    defs: dict[str, list[Definition]] = {}
    refs: dict[str, list[Ref]] = {}
    issues_without_ids: list[str] = []
    owner_files_present: set[str] = set()

    for full, rel in walk(root):
        try:
            text = open(full, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue
        kind = kind_of(rel)
        if kind == "issue" and rel.endswith(".md") and not rel.endswith("README.md"):
            fm = frontmatter(text)
            if fm and not re.search(r"^\s*(requirements|plan)\s*:", fm, re.M):
                issues_without_ids.append(rel)
        for pfx, pats in OWNERS.items():
            if matches(rel, pats):
                owner_files_present.add(pfx)
        lines = text.splitlines()
        for i, line in enumerate(lines, 1):
            for m in ID_RE.finditer(line):
                id_ = m.group(1)
                pfx = prefix_of(id_)
                if matches(rel, OWNERS[pfx]) and m.start() == min(x.start() for x in ID_RE.finditer(line)) \
                        and is_definition_line(line, id_):
                    block = line.strip()
                    if line.lstrip().startswith("#"):
                        # 見出しで定義した場合は、次の見出しまでの本文を由来の確認に含める
                        for nxt in lines[i:i + 20]:
                            if nxt.lstrip().startswith("#"):
                                break
                            block += "\n" + nxt
                    defs.setdefault(id_, []).append(
                        Definition(id_, rel, i, block, "廃止" in line))
                else:
                    refs.setdefault(id_, []).append(Ref(id_, rel, i, kind))

    rep = Report()
    defined_prefixes = {prefix_of(i) for i in defs}

    # ERROR: 重複定義
    for id_, ds in sorted(defs.items()):
        if len(ds) > 1:
            rep.errors.append(("重複定義", id_, ", ".join(f"{d.path}:{d.line}" for d in ds)))

    # ERROR: 未定義の参照
    for id_, rs in sorted(refs.items()):
        if id_ not in defs:
            locs = ", ".join(f"{r.path}:{r.line}" for r in rs[:5]) + (" ほか" if len(rs) > 5 else "")
            rep.errors.append(("未定義の ID への参照", id_, locs))

    has_tests = any(r.kind == "test" for rs in refs.values() for r in rs) or any(
        os.path.isdir(os.path.join(root, d)) for d in ("test", "tests", "e2e"))
    has_issues = os.path.isdir(os.path.join(root, "issues"))
    has_plan = any(os.path.isfile(os.path.join(root, f)) for f in PLAN_FILES)

    def ref_kinds(id_):
        return {r.kind for r in refs.get(id_, [])}

    def ref_paths(id_):
        return {r.path for r in refs.get(id_, [])}

    for id_, ds in sorted(defs.items()):
        d = ds[0]
        if d.deprecated:
            continue
        pfx = prefix_of(id_)
        kinds = ref_kinds(id_)
        loc = f"{d.path}:{d.line}"

        # WARN: 由来のない定義
        ups = UPSTREAM.get(pfx, set())
        if ups and (ups & defined_prefixes):
            line_ids = {prefix_of(x) for x in ID_RE.findall(d.text)} - {pfx} if pfx not in ups else \
                {prefix_of(x) for x in ID_RE.findall(d.text) if x != id_}
            if not (line_ids & ups) and "追加" not in d.text:
                rep.warns.append(("由来（上流 ID）がない", id_, loc))
        if "追加" in d.text and pfx in {"OV", "FR", "NFR", "UI"}:
            rep.infos.append(("由来が「追加」（上流への反映候補）", id_, loc))

        # WARN / INFO: 下流での参照
        if pfx == "C":
            if not (kinds - {"spec"}):
                rep.warns.append(("一次ドキュメントの ID が下流で参照されていない", id_, loc))
        elif pfx == "OV":
            if not any(p != d.path and p.startswith("docs/") for p in ref_paths(id_)):
                rep.warns.append(("Overview の ID が下流の文書で参照されていない", id_, loc))
        elif pfx in {"FR", "NFR"}:
            if has_plan and "plan" not in kinds:
                rep.warns.append(("要件が実装計画で参照されていない", id_, loc))
            if has_tests and "test" not in kinds:
                (rep.warns if pfx == "FR" else rep.infos).append(("要件を参照するテストがない", id_, loc))
        elif pfx == "AC":
            if has_tests and "test" not in kinds:
                rep.infos.append(("受け入れ条件を参照するテストがない", id_, loc))
        elif pfx == "UI":
            if (has_plan or has_issues) and not (kinds & {"plan", "issue"}):
                rep.infos.append(("UI の規則が計画・Issue で参照されていない", id_, loc))
        elif pfx == "W":
            if has_issues and "issue" not in kinds:
                rep.warns.append(("実装作業を参照する Issue がない", id_, loc))

    for p in sorted(issues_without_ids):
        rep.infos.append(("Issue のフロントマターに plan / requirements がない", "-", p))

    stats = {
        "defined": {p: sum(1 for i in defs if prefix_of(i) == p) for p in OWNERS},
        "referenced_ids": len(refs),
        "owner_files_present": sorted(owner_files_present),
    }
    return rep, stats


def render_md(rep: Report, stats: dict) -> str:
    out = ["# ID トレース検査結果", ""]
    out.append("| 接頭辞 | 定義数 |")
    out.append("|---|---|")
    for p, n in stats["defined"].items():
        out.append(f"| {p} | {n} |")
    out.append("")
    out.append(f"ERROR {len(rep.errors)} 件 / WARN {len(rep.warns)} 件 / INFO {len(rep.infos)} 件")
    for title, rows in (("ERROR", rep.errors), ("WARN", rep.warns), ("INFO", rep.infos)):
        out += ["", f"## {title}", ""]
        if not rows:
            out.append("なし")
            continue
        out.append("| 種類 | ID | 場所 |")
        out.append("|---|---|---|")
        for kind, id_, loc in rows:
            out.append(f"| {kind} | {id_} | {loc} |")
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    ap.add_argument("--strict", action="store_true", help="WARN でも終了コード 1 にする")
    a = ap.parse_args()
    rep, stats = analyze(a.root)
    if a.format == "json":
        print(json.dumps({"errors": rep.errors, "warns": rep.warns, "infos": rep.infos, "stats": stats},
                         ensure_ascii=False, indent=2))
    else:
        print(render_md(rep, stats), end="")
    if rep.errors or (a.strict and rep.warns):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
