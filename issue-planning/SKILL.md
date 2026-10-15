---
name: issue-planning
description: IMPLEMENTATION_PLAN.md を、独立して実装・テスト可能なIssueへ分割し、依存関係と完了条件を整理する。実装計画が完成し、実際の開発タスクへ落とし込むときに使う。
---

`./docs/IMPLEMENTATION_PLAN.md` を実行可能な Issue に分割する。

Issueを作成する前に、ghコマンドでgithub上にissueを作成するか、`./issues/`以下に作成するか尋ねること。

## 手順

1. Implementation Plan の作業と依存関係を読む。
2. 独立して実装・テストできる単位へ分割する。
3. Issue 間の依存関係を整理する。
4. 各 Issue に完了条件を設定する。

## ローカルissueの実施手順
Issueごとに、branchを変更し、実装を進めます。
Issue案だけ作成し実装は進めないこと。

- 1 Issue = Codexが1セッション程度で実装・検証できるサイズ
- フロントマターとして、created_at: YYYY-MM-DDと、status: created/doing/done/stop を設定する
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
