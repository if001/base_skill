# README
## install
`npx skills add issei-fujimoto-accelia/base_skills`

claudeの場合
`npx skills add issei-fujimoto-accelia/base_skills -a claude-code`


## ドキュメント構成

``` shell
spec/          :概念設計などを配置(人が把握しているもの)
---
docs/          :document-interviewで作成した、ARCHITECTURE.md, TEST_STRATEGY.mdなど
docs/D2/       :AIが実装中に作成したチェックリストなど
docs/D2/analyze/ :spec-analyze の分析レポート
docs/note/     :一時的なメモ
docs/planning/ :AIが実装中に作成する計画など
```

## skillの利用フロー
以下のフローを想定(各ステップでsession分けた方が良さそう)

``` shell
1. 1枚の概念設計を作成する(ChatGPTとかgeminiとかでOK)
これは人が確認し内容を把握しておく
各項目に C-01 のような ID を振っておく（ID の規則は document-interview/references/ID-Rules.md）

    ↓

2. discovery-interview: 「xxxをyyyするwebアプリケーションを作成する。」の指示と概念設計からプロジェクトのoverviewを作成する。

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

6. Issue ごとに実装する

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


## TODO
- issueのレビュー
- テストのカバレッジ
- sub agent周り
- ドキュメントのレビュー
- 変更フロー：差分（ADDED / MODIFIED / REMOVED）と影響範囲の洗い出し、上流への反映（OpenSpec の archive 相当）
