---
name: document-interview
description: Requirements、Architecture、ADR、Test Strategy など、指定された1つのドキュメントをインタビューを通じて完成させる。DOCUMENTATION_PLAN.md で作成対象が決まった後、各ドキュメントを個別に作成するときに使う。
---

指定された1つのドキュメントを完成させる。ドキュメントが指定されていない場合、手順を実行せず終了する。

## 手順

1. `spec/` 以下の一次ドキュメント、`./docs/D1/PROJECT_OVERVIEW.md`、`./docs/D2/DOCUMENTATION_PLAN.md`、既存ドキュメントを読む。
2. 指定されたドキュメントと対応するskillディレクトリの  `document-interview/references/`以下をリファレンスとして参照する。あわせて `references/ID-Rules.md`、`references/Writing-Rules.md`、`references/Glossary.md` を読む。
   - Requirements を作る場合は、同時に `./docs/D2/GLOSSARY.md` を作る（または更新する）。
   - UI / Design Guidelines を作る場合は `references/UI-Guidelines.md` を参照し、`./docs/D2/UI_GUIDELINES.md` として作成する。
4. 不足・曖昧・矛盾を整理する。
5. skill `grill-me-with-goal` を使い、完成に必要な事項を一問ずつ確認する。
6. 完了条件を満たしたら質問を終了する。
7. ドキュメントを `./docs/D2/` に作成する（例：`./docs/D2/REQUIREMENTS.md`）。インタビュー中の作業状態は `./docs/work/planning/` に置く。

既に決まっていることを再質問しない。

質問すること自体を目的にせず、ドキュメント完成をゴールとする。

## 制約

ID の規則は `references/ID-Rules.md` に従う。

- 作成するドキュメントの各項目に、その文書の ID（`FR`、`NFR`、`AC`、`UI`、`ADR` など）を振る。
- 各 ID の同じ行に、由来となる上流の ID（`OV-NN` または `C-NN`、下流の文書では `FR` / `NFR`）を書く。どこにも由来しない項目は `追加` と書き、理由を添える。
- 上流の文書（一次ドキュメントを含む）と矛盾する決定をした場合や、上流の未決事項を決めた場合は、文書末尾の「上流への反映」節に列挙し、ユーザーに報告する。一次ドキュメントは承認なしに編集しない。

## 書き方と用語

- すべての文書は `references/Writing-Rules.md` に従って短く書く。散文で説明せず、表と箇条書きを基本にする。
- 用語は `./docs/D2/GLOSSARY.md` の「用語」を使う。新しい用語が必要になったら、先に GLOSSARY に追加する。
- ドキュメントを作成したら、文書の検査（`python3 ../spec-analyze/scripts/doc_check.py glossary-to-prh`、`npx textlint docs/D1 docs/D2`、`python3 ../spec-analyze/scripts/doc_check.py table-length`。パスはこのスキルのディレクトリからの相対パス）を実行し、違反を0件にする。textlint がプロジェクトに導入されていない場合は、導入をユーザーに提案し、表のセルの検査だけを行う。

## 完成後

ドキュメントを作成したら、skill `spec-analyze` を `docs` の段階で実行し、上流との矛盾や ID の漏れがないかを確認するようユーザーに提案する。
