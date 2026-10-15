# 分析レポート：<段階>（YYYY-MM-DD）

## 対象

| 項目 | 内容 |
|---|---|
| 段階 | docs / plan / issues / impl / change / all |
| 基準 | `spec/...`（一次ドキュメント） |
| 照合した成果物 | ... |
| 対象のコミット | `git rev-parse HEAD` の値 |

## 要約

| 重大度 | 件数 |
|---|---|
| CRITICAL | n |
| HIGH | n |
| MEDIUM | n |
| LOW | n |

機械検査：ERROR n 件 / WARN n 件 / INFO n 件

## 指摘

| # | 重大度 | 観点 | 内容 | 根拠 | 直す側の候補 |
|---|---|---|---|---|---|
| 1 | CRITICAL | A | ... | `spec/CONCEPT.md` C-08、`docs/REQUIREMENTS.md` FR-T-7 | 上流（要承認）／下流 |

## Issue 化を推奨する指摘

- #1：...（一次ドキュメントの修正を含むため、ユーザーの承認が必要）

## 機械検査の結果

（`trace_check.py` の出力を貼る。件数が多い場合は ERROR と WARN のみ）
