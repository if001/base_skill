---
name: create-local-issue
description: 会話の内容や計画からlocalファイルとしてissueを作成するときに使う
---

ローカルのファイルとしてissueを作成します。
Issueごとに、branchを変更し、実装を進めます。
Issue案だけ作成し実装は進めないこと。
Issueはissues/ディレクトリ以下に、1ファイル1Issueとして作成してください。
フロントマターとして、created_at: YYYY-MM-DDと、status: created/doing/done/stop を設定してください。
あわせて、関連する ID を `plan: [W-N]`、`requirements: [FR-…]`、（必要なら）`ui: [UI-N]` として設定してください。ID の規則は `../document-interview/references/ID-Rules.md`（このスキルのディレクトリからの相対パス） に従います。
計画や要件にない内容の Issue（ユーザーとの会話から生まれた変更など）は、`requirements: [追加]` とし、Background に、どの文書（一次ドキュメントを含む）に反映が必要かを書いてください。
対応済のissueはstatusをdoneにすること。

## 条件
- 1 Issue = Codexが1セッション程度で実装・検証できるサイズ
- 各Issueは可能な限り独立させる
- 依存関係がある場合は明記する
- 各Issueに以下を含める
  - Background
  - Scope
  - Out of scope
  - Implementation notes
  - Acceptance criteria
  - Tests（各テストの先頭に、検証する要件 ID を書く）
- 元計画へのリンクを付ける

## issue
- 1 Issueは1commitである必要はありません。複数のstepに分けて実装可能です。
- Issueがその場限りの修正とならないようにする
- Issueはコードの修正を行うだけでなく、ユーザーと議論、検討したり、ドキュメントの修正も可能
