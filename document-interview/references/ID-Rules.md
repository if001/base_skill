# ID Rules

一次ドキュメントから実装・テストまでを ID でたどれるようにするための規則。
すべてのスキルはこの規則に従って ID を定義・参照する。

## ID の体系

| 層 | 文書 | ID の形式 | 例 | 付与する人 |
|---|---|---|---|---|
| 一次ドキュメント | `spec/` 以下 | `C-NN` | `C-08` | 人。スキルは提案だけ行い、承認なしに一次ドキュメントを編集しない |
| Overview | `docs/D1/PROJECT_OVERVIEW.md` | `OV-NN` | `OV-03` | discovery-interview |
| 機能要件 | `docs/D2/REQUIREMENTS.md` | `FR-<領域>-N`（領域は英大文字。省略可） | `FR-T-7`、`FR-12` | document-interview |
| 非機能要件 | `docs/D2/REQUIREMENTS.md` | `NFR-N` | `NFR-2` | document-interview |
| 受け入れ条件 | `docs/D2/REQUIREMENTS.md` | `AC-N` | `AC-14` | document-interview |
| UI の規則 | `docs/D2/UI_GUIDELINES.md` | `UI-N` | `UI-21` | document-interview |
| 技術判断 | `docs/D2/ARCHITECTURE.md` または `docs/D2/adr/` | `ADR-N` | `ADR-3` | document-interview |
| 実装作業 | `docs/D2/IMPLEMENTATION_PLAN.md` | `W-N` | `W-13` | implementation-planning |

Issue は番号付きのファイル名（`issues/013-xxx.md`）で識別し、上記の ID をフロントマターで参照する。
`docs/work/`（作業中の記録）では ID を参照してよいが、定義してはいけない。機械検査は `docs/work/` を対象外にする。

## 定義と参照

- **定義**：その ID を持つ文書（上の表の「文書」）で、表の行の先頭セル、見出し、または箇条書きの先頭に ID を置く。
  - 表：`| FR-T-7 | 作成者は… | C-08 |`
  - 見出し：`### ADR-3：…`
  - 箇条書き：`- AC-14：…`
- **参照**：定義以外の場所に ID を書く。
- 参照では範囲表記（`FR-T-1〜4`）を使わず、`FR-T-1, FR-T-2, FR-T-3, FR-T-4` のように列挙する。範囲表記は検索と機械検査で拾えないため。
- 見出しで定義した場合（ADR など）は、由来の ID を見出しの直後の本文に書いてよい。

## 由来（上流への参照）

下流の ID は、定義と同じ行に上流の ID を必ず書く。

| 定義する ID | 同じ行に書く上流の ID |
|---|---|
| `OV-NN` | `C-NN`（一次ドキュメントに ID がある場合） |
| `FR` / `NFR` | `OV-NN` または `C-NN` |
| `AC-N` | 検証する `FR` / `NFR` |
| `UI-N` | 根拠となる `FR` / `NFR`、または `C-NN`（品質方針など） |
| `ADR-N` | 判断の対象となる `FR` / `NFR` |
| `W-N` | 実装する `FR` / `NFR` / `UI` |

上流のどの記述にも由来しない項目を追加した場合は、由来の欄に `追加` と書き、理由を添える。
`追加` は spec-analyze で一次ドキュメントへの反映候補として報告される。

## 下流での参照

| 場所 | 書き方 |
|---|---|
| Issue のフロントマター | `plan: [W-13]`、`requirements: [FR-T-1, FR-T-2]`、必要なら `ui: [UI-21]` |
| テスト名 | 先頭に検証する ID を書く。例：`it("FR-T-7: 返信があるスレッドは削除できない", …)` |
| Test Strategy | 要件 ID（または AC ID）ごとに、検証するテストのレベルとファイルを対応表にする |
| コード | 任意。複雑な業務ルールの箇所にだけ、コメントで要件 ID を書いてよい |

## 変更時の規則

- ID は振り直さない。番号は欠番になってよい。
- 項目を削除するときは行を消さず、`（廃止）` と書いて残す。廃止した ID は再利用しない。
- 内容を大きく変えるときは、元の ID を廃止して新しい ID を振る。
- 一次ドキュメントの ID（`C-NN`）の追加・変更・廃止は、ユーザーの承認を得てから行う。

## 検査

`spec-analyze` スキルの `scripts/trace_check.py` で、次を機械的に検査できる。

- 未定義の ID への参照
- 重複定義
- 下流で一度も参照されていない ID（例：テストのない `FR`、Issue のない `W`）
- 由来のない定義
