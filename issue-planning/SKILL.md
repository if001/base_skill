---
name: issue-planning
description: IMPLEMENTATION_PLAN.md を、独立して実装・テスト可能なIssueへ分割し、依存関係と完了条件を整理する。実装計画が完成し、実際の開発タスクへ落とし込むときに使う。
---

`./docs/D2/IMPLEMENTATION_PLAN.md` を実行可能な Issue に分割する。

Issueを作成する前に、ghコマンドでgithub上にissueを作成するか、`./issues/`以下に作成するか尋ねること。

## 手順

1. Implementation Plan の作業と依存関係を読む。
2. 独立して実装・テストできる単位へ分割する。
3. Issue 間の依存関係を整理する。
4. 各 Issue に完了条件を設定する。
5. Issue を作成したら、skill `spec-analyze` を `issues` の段階で実行し、`W` の割り当て漏れや要件の漏れがないかを確認するようユーザーに提案する。

## ID

ID の規則は `../document-interview/references/ID-Rules.md`（このスキルのディレクトリからの相対パス） に従う。

- 1つの `W` を1つ以上の Issue に対応させる。すべての `W` が、いずれかの Issue から参照されるようにする。
- Issue のフロントマターに `plan`、`requirements`、必要なら `ui` を書く。
- Tests 欄の各テストは、先頭に検証する要件 ID を書く（例：`FR-T-7: 返信があるスレッドは削除できない`）。
- 受け入れ条件には、対応する `AC` を書く。

## ローカル Issue の書式

Issue の書式は `../create-local-issue/references/issue-template.md`（このスキルのディレクトリからの相対パス）に従う。
Issue 案を作成するだけで、実装は進めない（実装は skill `implement-issue` で行う）。

- 1 Issue = エージェントが1セッション程度で実装・検証できるサイズ
- 各 Issue は可能な限り独立させ、依存関係がある場合は明記する
- 計画どおりの実装は `type: feature` とする
- 本番環境の設定や手動確認など、人の作業を含む Issue には `requires: human` を付ける
- 元計画（`W-N` の節）へのリンクを付ける

## Issue の性質

- 1 Issue は1コミットである必要はない。複数のステップに分けて実装してよい。
- Issue がその場限りの修正にならないようにする。
- Issue はコードの修正だけでなく、ユーザーとの議論や検討、ドキュメントの修正を扱ってもよい。
