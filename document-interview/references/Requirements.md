# Requirements

## Goal

実装する対象と期待される振る舞いを明確にする。
各要件には識別としてIDを割り当てること。
ID と由来の書き方は `ID-Rules.md` に従う（機能要件 `FR`、非機能要件 `NFR`、受け入れ条件 `AC`）。
各要件の同じ行に、由来となる `OV-NN` または `C-NN` を書く。受け入れ条件には、検証する `FR` / `NFR` を書く。
要件は1要件1文、80字以内で書く（`Writing-Rules.md`）。用語は Requirements の中で定義せず、同時に作る `docs/D2/GLOSSARY.md` で定義する（`Glossary.md`）。

## Topics

- Purpose
- Users
- Scope
- Use cases
- Functional requirements
- Non-functional requirements
- Constraints
- Out of scope
- Acceptance criteria

## Complete when

- スコープが明確
- 主要機能の振る舞いが明確
- 主要な制約が明確
- 要件が検証可能
- 実装を妨げる重大な未決事項がない
- すべての要件と受け入れ条件に ID と由来がある
- すべての要件が1文で、文書の検査（textlint、表のセルの長さ）で違反がない
- 要件で使う主要な名詞が GLOSSARY に定義されている
- 上流の未決事項を決めた場合、その内容が「上流への反映」節に列挙されている
