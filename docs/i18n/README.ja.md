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

## v0.3.0 の新機能

- **自動セッション要約** -- すべてのセッションに AI 生成の要約が付きます（API キー不要）
- **自動決定抽出** -- パターンマッチングにより会話からアーキテクチャの決定を検出
- **BM25 キーワード検索** -- 正確な用語、エラーメッセージ、関数名に最適な新しい `search_keyword` ツール
- **ハイブリッド検索** -- 逆数ランク融合によりセマンティック + キーワード結果を統合
- **Cursor IDE サポート** -- `state.vscdb` ファイルから Cursor チャット履歴をインデックス
- **リアルタイムファイル監視** -- watchdog により新しいセッションを即座にインデックス（再起動不要）
- **チャンキング戦略** -- トークンベース、ターンベース、再帰分割から選択可能
- **VS Code 拡張機能** -- VS Code から直接検索、インデックス、統計表示
- **69 テスト** -- すべてのモジュールにわたる包括的なテストカバレッジ

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


<div align="center">
<img src="../../demo.gif" alt="MemoTrail Demo" width="800">
<br>
<sub>Install → Connect → See stats → Search past sessions → Save memory → Duplicate &amp; contradiction detection</sub>
</div>

## 仕組み

| ステップ | 何が起こるか |
|:----:|:-------------|
| **1. 記録** | MemoTrail は起動時に新しいセッションを自動インデックス + リアルタイムで新しいファイルを監視 |
| **2. 分割** | 会話はトークン、ターンベース、または再帰戦略で分割される |
| **3. 埋め込み** | 各チャンクは `all-MiniLM-L6-v2` で埋め込み（約 80MB、CPU で実行） |
| **4. 抽出** | 要約とアーキテクチャの決定が自動的に抽出される |
| **5. 保存** | ベクトルは ChromaDB に、メタデータは SQLite に -- すべて `~/.memotrail/` 配下 |
| **6. 検索** | セマンティック + BM25 キーワード検索で全履歴を横断 |
| **7. 表示** | 最も関連性の高い過去のコンテキストが必要な時に表示される |

> **100% ローカル** -- クラウドなし、API キー不要、データはマシンから出ません。
>
> **マルチプラットフォーム** -- Claude Code と Cursor IDE をサポート、さらに多くのプラットフォームに近日対応予定。

## 利用可能なツール

接続すると、Claude Code は以下の MCP ツールを使用できます：

| ツール | 説明 |
|------|-------------|
| `search_chats` | すべての過去の会話を横断するセマンティック検索 |
| `search_keyword` | BM25 キーワード検索 -- 正確な用語、関数名、エラーメッセージに最適 |
| `get_decisions` | 記録されたアーキテクチャの決定を取得（自動抽出 + 手動） |
| `get_recent_sessions` | 最近のコーディングセッションを AI 生成サマリー付きでリスト表示 |
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
| キーワード検索 | BM25 | Pure Python、追加依存なし |
| メタデータ | SQLite | 単一ファイルデータベース |
| ファイル監視 | watchdog | リアルタイムセッション検出 |
| プロトコル | MCP | Model Context Protocol |

### サポートプラットフォーム

| プラットフォーム | ステータス | フォーマット |
|----------|--------|--------|
| Claude Code | サポート済み | JSONL セッションファイル |
| Cursor IDE | サポート済み | state.vscdb (SQLite) |
| GitHub Copilot | 予定 | -- |

### チャンキング戦略

| 戦略 | 最適な用途 |
|----------|----------|
| `token`（デフォルト） | 汎用 -- トークン制限までメッセージをグループ化 |
| `turn` | 会話重視 -- ユーザー+アシスタントのペアでグループ化 |
| `recursive` | 長いコンテンツ -- 段落、文、単語で分割 |

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
- [x] 7 つのツールを備えた MCP サーバー
- [x] インデックスと検索のための CLI
- [x] サーバー起動時の自動インデックス
- [x] 自動決定抽出
- [x] セッション要約
- [x] Cursor IDE コレクター
- [x] BM25 キーワード検索 + ハイブリッド検索
- [x] リアルタイムファイル監視（watchdog）
- [x] 複数のチャンキング戦略（token、turn、recursive）
- [x] VS Code 拡張機能
- [ ] Copilot コレクター
- [ ] クラウド同期（Pro）
- [ ] チームメモリ（Team）

## VS Code 拡張機能

MemoTrail には IDE から直接統合できる VS Code 拡張機能が含まれています。

**利用可能なコマンド：**
- `MemoTrail: Search Conversations` -- セマンティック検索
- `MemoTrail: Keyword Search` -- BM25 キーワード検索
- `MemoTrail: Recent Sessions` -- セッション統計を表示
- `MemoTrail: Index Sessions Now` -- 手動インデックスをトリガー
- `MemoTrail: Show Stats` -- インデックス統計を表示

**セットアップ：**
```bash
cd vscode-extension
npm install
npm run compile
# VS Code で F5 を押して拡張機能開発ホストを起動
```

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
