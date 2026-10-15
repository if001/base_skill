# Issue の書式

Issue は `issues/NNN-<内容>.md` に1ファイル1件で作る。
ID の規則は `../../document-interview/references/ID-Rules.md` に従う。

## フロントマター

```yaml
---
created_at: YYYY-MM-DD
status: created        # created / doing / done / stop
type: feature          # feature（計画どおりの実装）/ change（変更）/ fix（不具合）/ docs（文書のみ）
plan: [W-13]           # 対応する実装作業。計画にない場合は []
requirements: [FR-T-1] # 対応する要件。計画や要件にない内容は [追加]
ui: [UI-21]            # 任意。満たすべき UI の規則
requires: agent        # agent（エージェントだけで完了できる）/ human（人の作業や判断が必要）
---
```

`requires: human` は、アカウントの操作、本番環境の設定、手動での確認、一次ドキュメントの変更の承認など、エージェントだけでは完了できない作業を含む Issue に付ける。
Implementation notes に、人が行う作業とエージェントが行う作業を分けて書く。

## 本文（共通）

```markdown
# NNN タイトル

元計画：[IMPLEMENTATION_PLAN.md W-13](../docs/D2/IMPLEMENTATION_PLAN.md#...)（計画以外が起点の場合は、起点の文書やレポートへのリンク）

## Background
## Dependencies
## Scope
## Out of scope
## Implementation notes
## Acceptance criteria
- [ ] AC-14：…
## Tests
- FR-T-7：返信があるスレッドは削除できない
```

- 受け入れ条件には対応する `AC` を、Tests の各項目には先頭に検証する要件 ID を書く。
- spec-analyze のレポート（`docs/work/analyze/`）やコードレビュー（`docs/work/reviews/`）の指摘から作る場合は、Background にレポートのパスと指摘番号を書く。

## 変更 Issue（type: change）

既存の文書や実装を変える場合は、原則として2つの Issue に分ける。

1. **ドキュメント Issue**：差分、影響範囲、上流への反映を決め、正の文書（`docs/D1/`、`docs/D2/`）を更新する。
2. **実装 Issue**：1 の決定に従って実装を変える。1 を Dependencies に書く。

変更が小さく、文書と実装を1セッションで変えられる場合は、1つの Issue にまとめてよい。

ドキュメント Issue（または1つにまとめた Issue）には、共通の節に加えて次の3節を書く。

```markdown
## 差分

| 種別 | ID | 内容 | 文書 |
|---|---|---|---|
| MODIFIED | FR-T-5 | 投稿先のコミュニティを選んで作成する | docs/D2/REQUIREMENTS.md |
| ADDED | FR-T-8 | … | docs/D2/REQUIREMENTS.md |
| REMOVED | UI-12 | … | docs/D2/UI_GUIDELINES.md |

## 影響範囲

検索した語：FR-T-5、「スレッド作成」、`/c/:id/threads`、「最初のスレッドを立てましょう」（用語を変える場合は、旧い用語とコード上の名前も含める）

| 場所 | 内容 | 対応 |
|---|---|---|
| docs/D2/ARCHITECTURE.md §5 | ルーティング表 | 更新する |
| src/views/pages/home.tsx | 空状態の文言 | 更新する（実装 Issue） |
| test/http/threads.test.ts | 作成のテスト | 更新する（実装 Issue） |
| docs/D2/ARCHITECTURE.md §3 | 構成図 | 更新しない（画面の追加に影響しないため） |

## 上流への反映

| 文書 | 反映内容 | 状態 |
|---|---|---|
| spec/CONCEPT.md C-07 | 画面表にスレッド作成画面を追加 | 承認待ち／反映済み／不要 |
```

- **差分**：変える ID を ADDED / MODIFIED / REMOVED で書く。ID を持たない記述を変える場合は、先に ID を振る。用語の追加・変更は `docs/D2/GLOSSARY.md` の行として差分に含める。
- **影響範囲**：差分の ID、関係する用語、画面名、ルート、画面の文言を `spec/`、`docs/D1/`、`docs/D2/`、ソース、テストで検索し、見つかった箇所と対応（更新する／しない理由）をすべて書く。列挙を記憶や推測で済ませない。
- **上流への反映**：一次ドキュメントの変更はユーザーの承認が必要。承認前は「承認待ち」とし、承認されるまで Issue を done にしない。

実装 Issue の受け入れ条件には、ドキュメント Issue の差分の各項目と、影響範囲で「更新する（実装 Issue）」とした各箇所を1項目ずつ転記する。

変更 Issue の完了条件には、次を必ず含める。

- [ ] 差分が正の文書に反映されている
- [ ] 上流への反映がすべて「反映済み」または「不要」になっている
- [ ] `spec-analyze change` で CRITICAL と HIGH の指摘がない
