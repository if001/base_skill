# README


以下のフローを想定(各ステップでsession分けた方が良さそう)

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


## install
`npx skills add if001/base_skill`


``` shell
docs/
docs/D2/
docs/note/
docs/planning/
```
