---
name: create-local-issue
description: 会話の内容や計画からlocalファイルとしてissueを作成するときに使う
---

ローカルのファイルとしてissueを作成します。
Issueごとに、branchを変更し、実装を進めます。
Issue案だけ作成し実装は進めないこと。
Issueはissues/ディレクトリ以下に、1ファイル1Issueとして作成してください。
フロントマターとして、created_at: YYYY-MM-DDと、status: created/doing/done/stop を設定してください。
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
  - Tests
- 元計画へのリンクを付ける

## issue
- 1 Issueは1commitである必要はありません。複数のstepに分けて実装可能です。
- Issueがその場限りの修正とならないようにする
- Issueはコードの修正を行うだけでなく、ユーザーと議論、検討したり、ドキュメントの修正も可能
