<div align="center">

# MemoTrail

> 🌐 這是自動翻譯。歡迎社區糾正！ · [English](../../README.md)

[🇨🇳 中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇵🇹 Português](README.pt.md) · [🇰🇷 한국어](README.ko.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇮🇱 עברית](README.he.md) · [🇸🇦 العربية](README.ar.md) · [🇷🇺 Русский](README.ru.md) · [🇵🇱 Polski](README.pl.md) · [🇨🇿 Čeština](README.cs.md) · [🇳🇱 Nederlands](README.nl.md) · [🇹🇷 Türkçe](README.tr.md) · [🇺🇦 Українська](README.uk.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Indonesia](README.id.md) · [🇹🇭 ไทย](README.th.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇧🇩 বাংলা](README.bn.md) · [🇵🇰 اردو](README.ur.md) · [🇷🇴 Română](README.ro.md) · [🇸🇪 Svenska](README.sv.md) · [🇮🇹 Italiano](README.it.md) · [🇬🇷 Ελληνικά](README.el.md) · [🇭🇺 Magyar](README.hu.md) · [🇫🇮 Suomi](README.fi.md) · [🇩🇰 Dansk](README.da.md) · [🇳🇴 Norsk](README.no.md)

**你的 AI 程式助手會忘記一切。MemoTrail 解決了這個問題。**

[![PyPI version](https://img.shields.io/pypi/v/memotrail?color=blue)](https://pypi.org/project/memotrail/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/HalilHopa-Datatent/memotrail?style=social)](https://github.com/HalilHopa-Datatent/memotrail)

為 AI 程式助手打造的持久化記憶層。
每次會話都被記錄，每個決策都可搜尋，每段脈絡都被銘記。

[快速開始](#快速開始) · [運作原理](#運作原理) · [可用工具](#可用工具) · [路線圖](#路線圖)

</div>

---

## v0.3.0 新特性

- **自動會話摘要** —— 每個會話都會產生 AI 摘要（無需 API 金鑰）
- **自動決策擷取** —— 使用模式比對從對話中偵測架構決策
- **BM25 關鍵字搜尋** —— 新增 `search_keyword` 工具，適用於精確術語、錯誤訊息、函式名
- **混合搜尋** —— 使用倒數排名融合結合語意 + 關鍵字結果
- **Cursor IDE 支援** —— 從 `state.vscdb` 檔案索引 Cursor 聊天歷史
- **即時檔案監控** —— 透過 watchdog 即時索引新會話（無需重啟）
- **分塊策略** —— 可選擇基於 token、基於輪次或遞迴分割
- **VS Code 擴充功能** —— 直接在 VS Code 中搜尋、索引和檢視統計
- **69 個測試** —— 涵蓋所有模組的全面測試

## 問題所在

每次新的 Claude Code 會話都從零開始。你的 AI 不記得昨天 3 小時的除錯過程、上週做出的架構決策，也不記得已經失敗過的方案。

**沒有 MemoTrail：**
```
你：  "我們用 Redis 做快取吧"
AI：  "好的，來設定 Redis"
         ... 兩週後，新的會話 ...
你：  "我們為什麼用 Redis？"
AI：  "我沒有關於這個決策的上下文"
```

**有了 MemoTrail：**
```
你：  "我們為什麼用 Redis？"
AI：  "根據 1 月 15 日的會話 —— 你評估了 Redis 和 Memcached。
      選擇 Redis 是因為它的資料結構支援和持久化能力。
      討論記錄在第 42 次會話中。"
```

## 快速開始

```bash
# 1. 安裝
pip install memotrail

# 2. 連接到 Claude Code
claude mcp add memotrail -- memotrail serve
```

就這樣。MemoTrail 會在首次啟動時自動索引你的歷史記錄。
開始新會話並詢問：*"我們上週做了什麼？"*


<div align="center">
<img src="../../demo.gif" alt="MemoTrail Demo" width="800">
<br>
<sub>Install → Connect → See stats → Search past sessions → Save memory → Duplicate &amp; contradiction detection</sub>
</div>

## 運作原理

| 步驟 | 發生了什麼 |
|:----:|:-------------|
| **1. 記錄** | MemoTrail 在啟動時自動索引新會話 + 即時監控新檔案 |
| **2. 分塊** | 對話使用 token、輪次或遞迴策略進行拆分 |
| **3. 嵌入** | 每個分塊使用 `all-MiniLM-L6-v2` 進行嵌入（約 80MB，CPU 運行） |
| **4. 擷取** | 自動擷取摘要和架構決策 |
| **5. 儲存** | 向量存入 ChromaDB，中繼資料存入 SQLite —— 全部在 `~/.memotrail/` 下 |
| **6. 搜尋** | 語意 + BM25 關鍵字搜尋涵蓋你的完整歷史 |
| **7. 呈現** | 最相關的過往脈絡在你需要時出現 |

> **100% 本地運行** —— 無需雲端服務，無需 API 金鑰，資料不會離開你的裝置。
>
> **多平台支援** —— 支援 Claude Code 和 Cursor IDE，更多平台即將推出。

## 可用工具

連接後，Claude Code 將獲得以下 MCP 工具：

| 工具 | 描述 |
|------|-------------|
| `search_chats` | 對所有過往對話進行語意搜尋 |
| `search_keyword` | BM25 關鍵字搜尋 —— 適用於精確術語、函式名、錯誤訊息 |
| `get_decisions` | 擷取記錄的架構決策（自動擷取 + 手動） |
| `get_recent_sessions` | 列出最近的程式會話及 AI 生成摘要 |
| `get_session_detail` | 深入查看特定會話的內容 |
| `save_memory` | 手動儲存重要事實或決策 |
| `memory_stats` | 查看索引統計和儲存使用情況 |

## CLI 命令

```bash
memotrail serve                          # 啟動 MCP 伺服器（自動索引新會話）
memotrail search "redis caching decision"  # 從終端搜尋
memotrail stats                          # 查看索引統計
memotrail index                          # 手動重新索引（可選）
```

## 架構

```
~/.memotrail/
├── chroma/          # 向量嵌入（ChromaDB）
└── memotrail.db     # 會話中繼資料（SQLite）
```

| 元件 | 技術 | 詳情 |
|-----------|-----------|---------|
| 嵌入 | `all-MiniLM-L6-v2` | 約 80MB，CPU 運行 |
| 向量資料庫 | ChromaDB | 持久化本地儲存 |
| 關鍵字搜尋 | BM25 | 純 Python，無額外依賴 |
| 中繼資料 | SQLite | 單一檔案資料庫 |
| 檔案監控 | watchdog | 即時會話偵測 |
| 協定 | MCP | Model Context Protocol |

### 支援平台

| 平台 | 狀態 | 格式 |
|----------|--------|--------|
| Claude Code | 已支援 | JSONL 會話檔案 |
| Cursor IDE | 已支援 | state.vscdb (SQLite) |
| GitHub Copilot | 規劃中 | — |

### 分塊策略

| 策略 | 最佳用途 |
|----------|----------|
| `token`（預設） | 通用 —— 按 token 限制分組訊息 |
| `turn` | 對話導向 —— 按使用者+助手對分組 |
| `recursive` | 長內容 —— 按段落、句子、詞拆分 |

## 為什麼選擇 MemoTrail？

| | MemoTrail | CLAUDE.md / 規則檔案 | 手動筆記 |
|---|---|---|---|
| 自動化 | 是 —— 每次會話啟動時索引 | 否 —— 需要手動撰寫 | 否 |
| 可搜尋 | 語意搜尋 | AI 讀取，但僅限你寫的內容 | 只有 Ctrl+F |
| 可擴展 | 數千個會話 | 單一檔案 | 零散的檔案 |
| 脈絡感知 | 回傳相關脈絡 | 靜態規則 | 手動查找 |
| 設定 | 5 分鐘 | 持續維護 | 持續維護 |

MemoTrail 不是要取代 `CLAUDE.md` —— 而是補充它。規則檔案用於指令，MemoTrail 用於記憶。

## 路線圖

- [x] Claude Code 會話索引
- [x] 跨對話語意搜尋
- [x] 帶 7 個工具的 MCP 伺服器
- [x] 用於索引和搜尋的 CLI
- [x] 伺服器啟動時自動索引
- [x] 自動決策擷取
- [x] 會話摘要
- [x] Cursor IDE 收集器
- [x] BM25 關鍵字搜尋 + 混合搜尋
- [x] 即時檔案監控（watchdog）
- [x] 多種分塊策略（token、turn、recursive）
- [x] VS Code 擴充功能
- [ ] Copilot 收集器
- [ ] 雲端同步（Pro）
- [ ] 團隊記憶（Team）

## VS Code 擴充功能

MemoTrail 包含一個 VS Code 擴充功能，可直接在 IDE 中整合。

**可用命令：**
- `MemoTrail: Search Conversations` —— 語意搜尋
- `MemoTrail: Keyword Search` —— BM25 關鍵字搜尋
- `MemoTrail: Recent Sessions` —— 檢視會話統計
- `MemoTrail: Index Sessions Now` —— 觸發手動索引
- `MemoTrail: Show Stats` —— 顯示索引統計

**設定：**
```bash
cd vscode-extension
npm install
npm run compile
# 然後在 VS Code 中按 F5 啟動擴充功能開發宿主
```

## 開發

```bash
git clone https://github.com/HalilHopa-Datatent/memotrail.git
cd memotrail
pip install -e ".[dev]"
pytest
ruff check src/
```

## 貢獻

歡迎貢獻！請參閱 [CONTRIBUTING.md](../../docs/CONTRIBUTING.md) 了解指南。

## 授權條款

MIT —— 請參閱 [LICENSE](../../LICENSE)

---

<div align="center">

**由 [Halil Hopa](https://halilhopa.com) 建構** · [memotrail.ai](https://memotrail.ai)

如果 MemoTrail 對你有幫助，請考慮在 GitHub 上給我們一個星標。

</div>
