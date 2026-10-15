# README
## install
`npx skills add issei-fujimoto-accelia/base_skills`

claudeの場合
`npx skills add issei-fujimoto-accelia/base_skills -a claude-code`


## ドキュメント構成

ディレクトリはあらかじめ固定する。エージェントが任意にディレクトリを作らないようにする。

``` shell
spec/              :一次ドキュメント（人が書き、内容を把握しているもの）C-NN
docs/D1/           :discovery-interview が作成する PROJECT_OVERVIEW.md（OV-NN）
docs/D2/           :設計文書と計画（DOCUMENTATION_PLAN、REQUIREMENTS、ARCHITECTURE、
                    TEST_STRATEGY、UI_GUIDELINES、IMPLEMENTATION_PLAN）
docs/work/         :作業中の記録（正ではない）
  analyze/         :spec-analyze のレポート
  reviews/         :コードレビューの結果
  test-runs/       :テスト実行後のメモ、カバレッジ
  checklists/      :作業用のチェックリスト
  planning/        :grill-me-with-goal の goal-state など
  design/          :UI セルフチェックのラウンド記録
  notes/           :上のどれにも当たらないメモ
issues/            :Issue（1ファイル1件）
```

- 実装とテストの根拠にしてよいのは `spec/`、`docs/D1/`、`docs/D2/` だけ。`docs/work/` は記録であり、見つかった指摘は Issue か正の文書に反映する。
- プロジェクトには `templates/AGENTS.md` と `templates/CLAUDE.md` をコピーして使う（CLAUDE.md は `@AGENTS.md` で AGENTS.md を取り込む）。

## skillの利用フロー
以下のフローを想定(各ステップでsession分けた方が良さそう)

``` shell
1. 1枚の概念設計を作成する(ChatGPTとかgeminiとかでOK)
これは人が確認し内容を把握しておく
各項目に C-01 のような ID を振っておく（ID の規則は document-interview/references/ID-Rules.md）

    ↓

2. discovery-interview: 「xxxをyyyするwebアプリケーションを作成する。」の指示と概念設計からプロジェクトのoverview（docs/D1/PROJECT_OVERVIEW.md）を作成する。

    ↓

2. documentation-planning: 必要なドキュメントの一覧(ARCHITECTURE.md, TEST_STRATEGY.md等)を作成。markdownを出力する。

    ↓

3. document-interview: 各ドキュメントを作成していく
   必要ドキュメントとして、ARCHITECTURE.md, TEST_STRATEGY.mdなどが作成されるので、各ドキュメントごとにskillを実行する
   画面がある場合は UI_GUIDELINES.md も作成する（主要な操作の画面遷移を人が確認する）

    ↓

   spec-analyze docs: 一次ドキュメントとドキュメント群の矛盾・ID の漏れを確認する

    ↓

4. implementation-plan: 各ドキュメントからどのように実装を進めるかの計画を立てる。(TDDにより進めることはここで設定する)

    ↓

5. Issue planning: 計画をissueに分割していく(ghコマンドでgithub上に作成するか、`./issues/`以下に作成するか指定する)

    ↓

   spec-analyze issues: 要件・作業・Issue の対応漏れを確認する

    ↓

6. implement-issue: Issue を1件ずつ実装する（TDD、検証、新しい文脈でのレビュー、上流への反映、完了処理）
   requires: human の Issue は、人の作業を終えてから完了にする

    ↓

   spec-analyze impl: 実装・テストと一次ドキュメント・要件の乖離、文書にない機能を確認する
```

## ID によるトレーサビリティ

一次ドキュメント（C）→ Overview（OV）→ 要件（FR / NFR / AC）→ UI の規則（UI）・設計判断（ADR）→ 実装作業（W）→ Issue → テスト を ID でつなぐ。
規則は `document-interview/references/ID-Rules.md`。
`spec-analyze/scripts/trace_check.py` で、未定義の参照、重複定義、下流で参照されていない ID、由来のない定義を機械的に検査できる。

``` shell
python3 .claude/skills/spec-analyze/scripts/trace_check.py --root .
```


## Issue駆動で開発を進める
spec/以下の一次ドキュメントをベースに、ドキュメントを作成、Issueを作成する。

修正する場合も、spec/以下の一次ドキュメントをベースに、ドキュメントを作成、Issueを作成のフローで修正する。

### 変更フロー

既存の文書や実装を変える場合は、create-local-issue で変更 Issue（`type: change`）を作る。原則として2つの Issue に分ける。

``` shell
1. ドキュメント Issue: 差分（ADDED / MODIFIED / REMOVED）、影響範囲（検索で洗い出す）、上流への反映を書き、docs/D1・D2 を更新する
   一次ドキュメント（spec/）の変更はユーザーの承認を得る

    ↓

2. 実装 Issue: 1 の差分と影響範囲を受け入れ条件に転記し、implement-issue で実装する

    ↓

   spec-analyze change: 変更が一次ドキュメントと矛盾しないか、反映漏れがないかを確認する
```

上流への反映がすべて「反映済み」または「不要」になるまで、変更 Issue は完了にしない（OpenSpec の archive に相当）。
書式は `create-local-issue/references/issue-template.md`。

### レビューや分析の指摘

spec-analyze のレポート（`docs/work/analyze/`）やコードレビュー（`docs/work/reviews/`）の指摘は、create-local-issue で Issue にする。記録に残すだけで終えない。


## TODO
- issueのレビュー
- sub agent周り
