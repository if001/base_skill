---
name: spec-analyze
description: 一次ドキュメント（spec/）を最上位の基準として、docs・実装計画・Issue・テスト・コードを横断して照合し、矛盾、ID の漏れ、文書にない機能、上流に戻っていない決定を報告する読み取り専用の分析。ドキュメント作成後、計画・Issue 作成後、実装完了後、変更の後に使う。GitHub Spec Kit の analyze に相当する。
argument-hint: "[docs|plan|issues|impl|change|all]"
context: fork
agent: general-purpose
background: false
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/trace_check.py *) Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/doc_check.py *) Bash(npx textlint *)
---

一次ドキュメント（`spec/` 以下）と下流の成果物を照合し、乖離を報告する。
引数で段階を受け取る（`$ARGUMENTS`）。指定がない場合は `all` とする。

Claude Code 以外で実行する場合や `context: fork` が効かない環境では、作成者とは別のセッション（またはサブエージェント）で実行する。成果物を作った文脈のまま照合すると、同じ前提で見落とすため。

## 原則

- **読み取り専用**：レポートファイル（と検査用に生成する `.textlint/prh.generated.yml`）以外は作成・変更しない。修正案は書いてよいが、適用しない。
- **一次ドキュメントが最上位**：一次ドキュメントとの矛盾は、他の文書がどう書いていても CRITICAL とする（Spec Kit の constitution と同じ扱い）。
- **中間の解釈を前提にしない**：下流の文書の解釈を正しいと仮定せず、一次ドキュメントの文言と直接比べる。
- **指摘を絞る**：一次ドキュメント、要件、ID の対応に関わるずれだけを報告する。好みの問題や、要件に関わらない改善提案は報告しない。指摘を探す役割を与えられると、問題のない箇所にも指摘を作りがちなため。
- **直す側を決めない**：各指摘には「上流を直す／下流を直す／実装を直す」の候補を示し、どれを選ぶかはユーザーに委ねる。一次ドキュメントの修正は、ユーザーの承認が必要であることを明記する。

## 段階ごとの対象

| 段階 | 照合する成果物 |
|---|---|
| `docs` | `spec/`、`docs/D1/`、`docs/D2/` の各設計文書 |
| `plan` | 上記＋`docs/D2/IMPLEMENTATION_PLAN.md` |
| `issues` | 上記＋`issues/` |
| `impl` | 上記＋テストとコード（画面がある場合は画面の構成と文言） |
| `change` | 直近の変更（`git diff`、変更 Issue）に関係する範囲。変更が一次ドキュメントの目的・決定事項・非スコープに反しないかを重点的に見る |
| `all` | 存在するすべて |

## 手順

1. `spec/`、`docs/D1/`、`docs/D2/`、`issues/`、テスト、コードの所在を確認する。`docs/work/` は作業中の記録であり、照合の基準にしない。ID の規則は `${CLAUDE_SKILL_DIR}/../document-interview/references/ID-Rules.md` を読む。
2. 機械検査を実行する。

   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/trace_check.py --root .
   ```

   結果（ERROR / WARN / INFO）をレポートに取り込む。範囲表記（`FR-1〜4`）など、規則違反が原因の WARN はその旨を書く。
   プロジェクトに textlint が導入されている場合は、`python3 ${CLAUDE_SKILL_DIR}/scripts/doc_check.py glossary-to-prh` のあとに `npx textlint docs/D1 docs/D2` と `python3 ${CLAUDE_SKILL_DIR}/scripts/doc_check.py table-length` を実行し、件数をレポートに書く（ただし `.textlint/prh.generated.yml` 以外のファイルは変更しない）。
3. 意味の照合を行う。次の観点ごとに、根拠（ファイルと行、または節）を添えて記録する。

   | 観点 | 内容 |
   |---|---|
   | A. 一次ドキュメントとの矛盾 | 下流の文書・実装が、一次ドキュメントの決定事項・機能スコープ・非スコープに反していないか。文言どおりに読んだときの矛盾も含める（解釈で吸収されていても、一次ドキュメントの文言が更新されていなければ指摘する） |
   | B. 上流に戻っていない決定 | 下流で決めた事項（未決事項の決定、追加された制約、由来が `追加` の項目）が、上流の文書に反映されているか。上流に「未決」のまま残っている事項はないか |
   | C. 文書にない機能 | テスト・コード・画面に存在するが、要件・UI ガイドライン・設計のどこにも書かれていない機能や画面要素はないか（`impl` 以降） |
   | D. 文書間の不整合 | 用語の揺れ、画面数・ルート・データ項目・文言の食い違い、変更後に古くなった記述 |
   | E. 網羅性 | 機械検査の結果の解釈。要件に対応する作業・Issue・テストがない、根拠のない作業がある、受け入れ条件が未照合のまま |
   | F. 曖昧さ | 検証できない要件、`[NEEDS CLARIFICATION]` などの未解決の印、判断が分かれる記述 |
   | G. 用語 | `docs/D2/GLOSSARY.md` にない用語の使用、使わない言い換えの使用（表記揺れ）、コード上の名前と実装の識別子のずれ（`impl` 以降） |

4. 各指摘に重大度を付ける。

   | 重大度 | 基準 |
   |---|---|
   | CRITICAL | 一次ドキュメントとの矛盾。未定義の ID への参照 |
   | HIGH | 要件の未実装・未テスト。文書にない機能。上流に戻っていない決定 |
   | MEDIUM | 文書間の不整合、古い記述、由来のない ID |
   | LOW | 表記揺れ、文の長さなど、動作や判断に影響しないもの（用語の意味が食い違う場合は MEDIUM 以上） |

5. レポートを `docs/work/analyze/YYYY-MM-DD-<段階>.md` に書く（形式は [references/report-template.md](references/report-template.md)）。
6. 会話には、重大度ごとの件数と、Issue 化を推奨する指摘の一覧だけを返す。

## 終了条件

- 段階に対応するすべての成果物を照合した
- すべての指摘に根拠、重大度、直す側の候補がある
- 一次ドキュメントの修正が必要な指摘には、ユーザーの承認が必要と明記した
