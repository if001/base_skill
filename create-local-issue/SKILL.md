---
name: create-local-issue
description: 会話の内容、計画、spec-analyze やコードレビューの指摘から、ローカルファイルとして Issue を作成するときに使う。既存の文書や実装を変える「変更 Issue」もこのスキルで作る。Issue の作成だけを行い、実装はしない。
---

ローカルのファイルとして Issue を作成する。
Issue 案を作成するだけで、実装は進めない（実装は skill `implement-issue` で行う）。

## 手順

1. 起点（会話、計画、レポートの指摘）と、関係する正の文書（`spec/`、`docs/D1/`、`docs/D2/`）を読む。`docs/work/` は起点として読んでよいが、根拠にはしない。
2. 書式は [references/issue-template.md](references/issue-template.md) に従う。
3. 既存の文書や実装を変える場合は、変更 Issue（`type: change`）として、差分・影響範囲・上流への反映を書く。影響範囲は検索で洗い出す。
4. `issues/` 以下に1ファイル1件で作成する。番号は既存の最大番号の次から振る。
5. 作成した Issue の一覧と依存関係を報告する。

## 条件

- 1 Issue = エージェントが1セッション程度で実装・検証できるサイズ
- 各 Issue は可能な限り独立させ、依存関係がある場合は明記する
- ID の規則は `../document-interview/references/ID-Rules.md`（このスキルのディレクトリからの相対パス）に従う
- 計画や要件にない内容の Issue は `requirements: [追加]` とし、どの文書（一次ドキュメントを含む）に反映が必要かを書く
- 人の作業や判断が必要な Issue には `requires: human` を付ける

## Issue の性質

- 1 Issue は1コミットである必要はない。複数のステップに分けて実装してよい。
- Issue がその場限りの修正にならないようにする。
- Issue はコードの修正だけでなく、ユーザーとの議論や検討、ドキュメントの修正を扱ってもよい。
