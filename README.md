# README
## install
`npx skills add issei-fujimoto-accelia/base_skills`


## ドキュメント構成

``` shell
spec/          :概念設計などを配置(人が把握しているもの)
---
docs/          :document-interviewで作成した、ARCHITECTURE.md, TEST_STRATEGY.mdなど
docs/D2/       :AIが実装中に作成したチェックリストなど
docs/note/     :一時的なメモ
docs/planning/ :AIが実装中に作成する計画など
```

## skillの利用フロー
以下のフローを想定(各ステップでsession分けた方が良さそう)

``` shell
1. 1枚の概念設計を作成する(ChatGPTとかgeminiとかでOK)
これは人が確認し内容を把握しておく

    ↓

2. discovery-interview: 「xxxをyyyするwebアプリケーションを作成する。」の指示と概念設計からプロジェクトのoverviewを作成する。

    ↓

2. documentation-planning: 必要なドキュメントの一覧(ARCHITECTURE.md, TEST_STRATEGY.md等)を作成。markdownを出力する。

    ↓

3. document-interview: 各ドキュメントを作成していく
   必要ドキュメントとして、ARCHITECTURE.md, TEST_STRATEGY.mdなどが作成されるので、各ドキュメントごとにskillを実行する

    ↓
4. Implementation Plan: 各ドキュメントからどのように実装を進めるかの計画を立てる。(TDDにより進めることはここで設定する)

    ↓

5. Issue planning: 計画をissueに分割していく(ghコマンドでgithub上に作成するか、`./issues/`以下に作成するか指定する)
```


## Issue駆動で開発を進める
spec/以下の一次ドキュメントをベースに、ドキュメントを作成、Issueを作成する。

修正する場合も、spec/以下の一次ドキュメントをベースに、ドキュメントを作成、Issueを作成のフローで修正する。


## TODO
- issueのレビュー
- テストのカバレッジ
- sub agent周り
- ドキュメントのレビュー
- 実装からドキュメント、一次ドキュメントの乖離を防ぐフロー
