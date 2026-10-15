# AGENTS.md

このリポジトリは、一次ドキュメントを起点に、ドキュメント → 計画 → Issue → 実装の順で開発する。
エージェントは、以下のディレクトリ構成と規則に従って文書を読み書きする。

## ディレクトリ構成

```
spec/                 一次ドキュメント（人が書く）
docs/
  D1/                 プロジェクト概要（discovery-interview）
  D2/                 設計文書と計画（document-interview、documentation-planning、implementation-planning）
  work/               作業中の記録（エージェントが作業中に作るもの）
    analyze/          spec-analyze のレポート
    reviews/          コードレビューの結果
    test-runs/        テスト実行後のメモ、カバレッジ
    checklists/       作業用のチェックリスト
    planning/         grill-me-with-goal の goal-state など、対話中の作業状態
    design/           UI のセルフチェックの記録（ラウンドごとの review.md）
    notes/            上のどれにも当たらないメモ
issues/               Issue（1ファイル1件）
```

| 場所 | 位置づけ | 主なファイル | ID |
|---|---|---|---|
| `spec/` | 正（最上位） | `CONCEPT.md` | `C-NN` |
| `docs/D1/` | 正 | `PROJECT_OVERVIEW.md` | `OV-NN` |
| `docs/D2/` | 正 | `DOCUMENTATION_PLAN.md`、`REQUIREMENTS.md`、`ARCHITECTURE.md`、`TEST_STRATEGY.md`、`UI_GUIDELINES.md`、`IMPLEMENTATION_PLAN.md` | `FR` / `NFR` / `AC` / `UI` / `ADR` / `W` |
| `docs/work/` | 記録（正ではない） | `YYYY-MM-DD-<内容>.md` | 参照のみ |
| `issues/` | 作業の単位 | `NNN-<内容>.md` | フロントマターで参照 |

## 規則

### 一次ドキュメント（spec/）

- ユーザーの明示的な承認なしに変更しない。
- 下流で一次ドキュメントと矛盾する決定をした場合や、一次ドキュメントの未決事項を決めた場合は、変更案を提示して承認を求める。

### 正の文書（docs/D1/、docs/D2/）

- 実装とテストは、この2つと `spec/` だけを根拠にする。`docs/work/` の内容を根拠にしない。
- 内容を変えるときは、変更用の Issue を作り、その中で更新する。
- ID は `document-interview/references/ID-Rules.md`（スキルのディレクトリ）に従って振り、参照する。ID を振り直さない。

### 作業中の記録（docs/work/）

- エージェントが作業中に作る文書は、すべて `docs/work/` の決められたサブディレクトリに置く。`docs/` の直下や、リポジトリの他の場所に新しいディレクトリを作らない。
- 当てはまるサブディレクトリがない場合は `notes/` に置く。新しいサブディレクトリが必要な場合は、先に本ファイルの構成に追記してから作る。
- ファイル名は `YYYY-MM-DD-<内容>.md` とする（`design/` は `rounds/NN/review.md`）。
- 記録の中で見つかった、正の文書や実装に影響する事項（レビューの指摘、未検証のリスクなど）は、記録に残すだけで終えず、Issue にするか、該当する正の文書に反映する。
- 古くなった記録は、ユーザーの判断で削除してよい。

### Issue（issues/）

- 作成は skill `create-local-issue`（計画からは `issue-planning`）、実装は skill `implement-issue` で行う。書式は `create-local-issue/references/issue-template.md`。
- フロントマターに `created_at`、`status`（created / doing / done / stop）、`type`、`plan`、`requirements`、`requires`（agent / human）を書く。
- `requires: human` の Issue は、人の作業が終わるまで `done` にしない。
- 既存の文書や実装を変える場合は、変更 Issue（`type: change`）として差分・影響範囲・上流への反映を書く。上流への反映が終わるまで `done` にしない。
- Issue ごとにブランチ（`issue/NNN-<内容>`）を切って実装する。

## 確認のタイミング

| タイミング | 実行するもの |
|---|---|
| `docs/D2/` の設計文書がそろったとき | `spec-analyze docs` |
| 計画と Issue を作ったとき | `spec-analyze issues` |
| 実装が一通り終わったとき | `spec-analyze impl` |
| 変更の Issue が完了したとき | `spec-analyze change` |

ID の機械検査だけを行う場合：

```
python3 <スキルのディレクトリ>/spec-analyze/scripts/trace_check.py --root .
```

## コマンド

<!-- プロジェクトに合わせて記載する -->

| 用途 | コマンド |
|---|---|
| 開発サーバー | |
| テスト | |
| カバレッジ | |
| 型チェック | |
