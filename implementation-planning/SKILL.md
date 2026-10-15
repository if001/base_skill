---
name: implementation-planning
description: Project Overview と作成済みドキュメントを基に、実装対象、依存関係、実装順序、テスト方針を整理し、IMPLEMENTATION_PLAN.md を作成する。必要な設計ドキュメントが揃い、Issueへ分割する前に使う。
---

作成済みドキュメントから実装計画を作成する。

## 手順

1. Project Overview(`./docs/D1/PROJECT_OVERVIEW.md`) と `./docs/D2/` の全ドキュメントを読む。
2. 実装対象を技術的な作業単位へ分解する。
3. 依存関係と実装順序を整理する。
4. テスト方針を各作業へ反映する。
5. `./docs/D2/IMPLEMENTATION_PLAN.md` を作成する。
6. skill `spec-analyze` を `plan` の段階で実行し、要件の割り当て漏れがないかを確認するようユーザーに提案する。

## ID

ID の規則は `../document-interview/references/ID-Rules.md`（このスキルのディレクトリからの相対パス） に従う。

- 各作業に `W-N` を振り、同じ行に実装する要件 ID（`FR` / `NFR`）と、満たすべき `UI` を書く。
- すべての `FR` / `NFR` を、少なくとも1つの `W` に割り当てる。割り当てない要件は、理由（手動確認のみ、設計上の非実装など）を対応表に書く。
- 各作業のテスト欄には、検証する要件 ID を書く。テスト名の先頭にその ID を書く規則を守る。

## UI がある場合

`./docs/D2/UI_GUIDELINES.md` がある場合は、次を計画に含める。

- 画面の作業より前に、UI 基盤の作業（デザイントークン、共通部品、部品の見本ページ、確認ツール）を置く。
- 画面を追加・変更する作業の完了条件に、UI_GUIDELINES のセルフチェックの合格を含める。
- 最後に、全画面を通しでセルフチェックする作業を置く。

## 原則

実装はTDDで進める。(`implementation-planning/references/tdd.md`を参照する。)

各作業は原則として:

1. failing test
2. minimal implementation
3. test pass
4. refactor

の順で進める。

計画にはコードの細かな実装手順を書きすぎない。
Issueへ分割可能な粒度まで整理する。
