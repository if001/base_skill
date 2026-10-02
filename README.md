# README

以下のフローを想定
1. discovery-interview: 「xxxをyyyするwebアプリケーションを作成する。」のような指示からプロジェクトのoverviewを作成する。

    ↓

3. documentation-planning: 必要なドキュメントの一覧(ARCHITECTURE.md, TEST_STRATEGY.md等)を作成。markdownを出力する。

    ↓

4. document-interview: 各ドキュメントを作成していく
   必要ドキュメントとして、ARCHITECTURE.md, TEST_STRATEGY.mdなどが作成されるので、各ドキュメントごとにskillを実行する

    ↓
5. Implementation Plan: 各ドキュメントからどのように実装を進めるかの計画を立てる。(TDDにより進めることはここで設定する)

    ↓

6. Issue planning: 計画をissueに分割していく(ghコマンドでgithub上に作成するか、`./issues/`以下に作成するか指定する)


## install
`npx skills add if001/base_skill`
