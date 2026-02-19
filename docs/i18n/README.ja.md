<div align="center">

# MemoTrail

> 🌐 これは自動翻訳です。コミュニティによる修正を歓迎します！ · [English](../../README.md)

[🇨🇳 中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇵🇹 Português](README.pt.md) · [🇰🇷 한국어](README.ko.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇮🇱 עברית](README.he.md) · [🇸🇦 العربية](README.ar.md) · [🇷🇺 Русский](README.ru.md) · [🇵🇱 Polski](README.pl.md) · [🇨🇿 Čeština](README.cs.md) · [🇳🇱 Nederlands](README.nl.md) · [🇹🇷 Türkçe](README.tr.md) · [🇺🇦 Українська](README.uk.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Indonesia](README.id.md) · [🇹🇭 ไทย](README.th.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇧🇩 বাংলা](README.bn.md) · [🇵🇰 اردو](README.ur.md) · [🇷🇴 Română](README.ro.md) · [🇸🇪 Svenska](README.sv.md) · [🇮🇹 Italiano](README.it.md) · [🇬🇷 Ελληνικά](README.el.md) · [🇭🇺 Magyar](README.hu.md) · [🇫🇮 Suomi](README.fi.md) · [🇩🇰 Dansk](README.da.md) · [🇳🇴 Norsk](README.no.md)

**あなたの AI コーディングアシスタントはすべてを忘れます。MemoTrail がそれを解決します。**

[![PyPI version](https://img.shields.io/pypi/v/memotrail?color=blue)](https://pypi.org/project/memotrail/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/HalilHopa-Datatent/memotrail?style=social)](https://github.com/HalilHopa-Datatent/memotrail)

AI コーディングアシスタントのための永続的メモリレイヤー。
すべてのセッションが記録され、すべての決定が検索可能で、すべてのコンテキストが記憶されます。

[クイックスタート](#クイックスタート) · [仕組み](#仕組み) · [利用可能なツール](#利用可能なツール) · [ロードマップ](#ロードマップ)

</div>

---

## 問題

新しい Claude Code セッションは毎回ゼロから始まります。AI は昨日の 3 時間のデバッグセッション、先週行ったアーキテクチャの決定、すでに失敗したアプローチを覚えていません。

**MemoTrail なし：**
```
あなた：「キャッシュに Redis を使おう」
AI：    「はい、Redis をセットアップしましょう」
         ... 2 週間後、新しいセッション ...
あなた：「なぜ Redis を使っているの？」
AI：    「その決定に関するコンテキストがありません」
```

**MemoTrail あり：**
```
あなた：「なぜ Redis を使っているの？」
AI：    「1 月 15 日のセッションによると — Redis と Memcached を評価しました。
         データ構造のサポートと永続性のために Redis が選ばれました。
         議論はセッション #42 に記録されています。」
```

## クイックスタート

```bash
# 1. インストール
pip install memotrail

# 2. Claude Code に接続
claude mcp add memotrail -- memotrail serve
```

以上です。MemoTrail は初回起動時に自動的に履歴をインデックスします。
新しいセッションを開始して聞いてみましょう：*「先週何をしましたか？」*

## 仕組み

| ステップ | 何が起こるか |
|:----:|:-------------|
| **1. 記録** | MemoTrail はサーバー起動時に新しいセッションを自動インデックス |
| **2. 分割** | 会話は意味のあるセグメントに分割される |
| **3. 埋め込み** | 各チャンクは `all-MiniLM-L6-v2` で埋め込み（約 80MB、CPU で実行） |
| **4. 保存** | ベクトルは ChromaDB に、メタデータは SQLite に — すべて `~/.memotrail/` 配下 |
| **5. 検索** | 次のセッションで、Claude が全履歴をセマンティック検索 |
| **6. 表示** | 最も関連性の高い過去のコンテキストが必要な時に表示される |

> **100% ローカル** — クラウドなし、API キー不要、データはマシンから出ません。

## 利用可能なツール

接続すると、Claude Code は以下の MCP ツールを使用できます：

| ツール | 説明 |
|------|-------------|
| `search_chats` | すべての過去の会話を横断するセマンティック検索 |
| `get_decisions` | 記録されたアーキテクチャの決定を取得 |
| `get_recent_sessions` | 最近のコーディングセッションをサマリー付きでリスト表示 |
| `get_session_detail` | 特定のセッションの内容を詳細に確認 |
| `save_memory` | 重要な事実や決定を手動で保存 |
| `memory_stats` | インデックス統計とストレージ使用量を表示 |

## CLI コマンド

```bash
memotrail serve                          # MCP サーバーを起動（新しいセッションを自動インデックス）
memotrail search "redis caching decision"  # ターミナルから検索
memotrail stats                          # インデックス統計を表示
memotrail index                          # 手動で再インデックス（オプション）
```

## アーキテクチャ

```
~/.memotrail/
├── chroma/          # ベクトル埋め込み（ChromaDB）
└── memotrail.db     # セッションメタデータ（SQLite）
```

| コンポーネント | 技術 | 詳細 |
|-----------|-----------|---------|
| 埋め込み | `all-MiniLM-L6-v2` | 約 80MB、CPU で実行 |
| ベクトル DB | ChromaDB | 永続的なローカルストレージ |
| メタデータ | SQLite | 単一ファイルデータベース |
| プロトコル | MCP | Model Context Protocol |

## なぜ MemoTrail？

| | MemoTrail | CLAUDE.md / ルールファイル | 手動メモ |
|---|---|---|---|
| 自動化 | はい — セッション開始時にインデックス | いいえ — 手動で記述 | いいえ |
| 検索可能 | セマンティック検索 | AI が読み取るが、記述した内容のみ | Ctrl+F のみ |
| スケール | 数千のセッション | 単一ファイル | 散在するファイル |
| コンテキスト対応 | 関連するコンテキストを返す | 静的ルール | 手動検索 |
| セットアップ | 5 分 | 常に維持が必要 | 常に維持が必要 |

MemoTrail は `CLAUDE.md` を置き換えるものではありません — 補完するものです。ルールファイルは指示用、MemoTrail はメモリ用です。

## ロードマップ

- [x] Claude Code セッションインデックス
- [x] 会話横断のセマンティック検索
- [x] 6 つのツールを備えた MCP サーバー
- [x] インデックスと検索のための CLI
- [x] サーバー起動時の自動インデックス
- [ ] 自動決定抽出
- [ ] セッション要約
- [ ] Cursor コレクター
- [ ] Copilot コレクター
- [ ] VS Code 拡張機能
- [ ] クラウド同期（Pro）
- [ ] チームメモリ（Team）

## 開発

```bash
git clone https://github.com/HalilHopa-Datatent/memotrail.git
cd memotrail
pip install -e ".[dev]"
pytest
ruff check src/
```

## コントリビューション

コントリビューション歓迎！ガイドラインは [CONTRIBUTING.md](../../docs/CONTRIBUTING.md) をご覧ください。

## ライセンス

MIT — [LICENSE](../../LICENSE) をご覧ください

---

<div align="center">

**[Halil Hopa](https://halilhopa.com) が構築** · [memotrail.ai](https://memotrail.ai)

MemoTrail が役に立ったら、GitHub でスターを付けることを検討してください。

</div>
