# Test Strategy

## Goal

要件と主要リスクをどのテストで検証するか明確にする。
具体的にどのテストライブラリを使用して、カバレッジはどこまで求めるのかもここで議論する。
要件とテストをIDで対応させる仕組みとする。
テスト名の先頭に検証する要件 ID（`FR` / `NFR` / `AC`）を書く規則とし、要件 ID ごとに検証するテストのレベルとファイルを対応表にする（`ID-Rules.md`）。

## Topics

- Test scope
- Unit tests
- Integration tests
- E2E tests
- Platform-specific tests
- Manual tests
- Test environment
- Acceptance criteria coverage

## Complete when

- 主要な要件に検証方法がある
- テストレベルの役割分担が明確
- 重要な統合部分の検証方法が明確
- 必要な実行環境や外部依存の扱いが明確
- 主要な未検証リスクが把握されている
- テスト名に要件 ID を書く規則が定まっている
- すべての `FR` に、検証方法（自動テストまたは手動チェック）が対応している
