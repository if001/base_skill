---
name: documentation-planning
description: プロジェクト概要を基に、プロジェクトの規模・複雑性・リスクを評価し、実装前に必要なドキュメントと作成順序を決める。Overview完成後、詳細な設計や要件整理を始める前に使う。
---

`./docs/D1/PROJECT_OVERVIEW.md` を読み、実装前に必要なドキュメントを決定する。

## 手順

1. プロジェクトの規模、複雑性、リスクを確認する。
2. 必要なドキュメントだけを選ぶ。
3. 作成順序と理由を `./docs/D2/DOCUMENTATION_PLAN.md` に記録する。

## 主な候補

* Requirements
* Architecture
* ADR
* Data Design
* API Spec
* UI / Design Guidelines
* UX / User Flow
* Security Design
* Privacy Design
* Sync / State Design
* Test Strategy
* Operations Design

必要以上に文書を増やさない。

複雑な領域だけ独立した文書にしてよい。
小さな関心事は他の文書のセクションに含める。

## 例
### 小規模な場合に含めるべきドキュメント
- Requirements
- Architecture
- Test Strategy

### 中規模な場合に含めるべきドキュメント
- Requirements
- Architecture
- ADR
- Data Design
- API Spec
- Test Strategy

## UI / Design Guidelines

画面を持つアプリケーションでは、規模にかかわらず UI / Design Guidelines（`./docs/D2/UI_GUIDELINES.md`）を作成対象に含める。
見た目の方針と共通部品が決まらないまま Issue に分割すると、各画面が場当たり的に作られ、後からまとめて直すことになるため。

- 作成順序は Requirements（画面一覧と操作の流れが決まる）の後、Implementation Plan の前に置く。
- 内容と品質方針は `document-interview/references/UI-Guidelines.md` に従う。品質方針は「Awwwards、Webby Awards、The FWA で賞を獲れるくらいのクオリティを目指し、セルフチェックでその基準になるまでクオリティアップを繰り返す」とする。
- UX / User Flow を独立文書にしない場合は、主要な操作シナリオと画面遷移を UI / Design Guidelines に含める。

## ID

DOCUMENTATION_PLAN.md には、作成する各文書がどの ID を定義するか（`FR`、`UI`、`ADR` など）を記載する。規則は `../document-interview/references/ID-Rules.md`（このスキルのディレクトリからの相対パス） に従う。
