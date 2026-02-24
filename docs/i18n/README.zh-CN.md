<div align="center">

# MemoTrail

> 🌐 这是自动翻译。欢迎社区纠正！ · [English](../../README.md)

[🇨🇳 中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇵🇹 Português](README.pt.md) · [🇰🇷 한국어](README.ko.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇮🇱 עברית](README.he.md) · [🇸🇦 العربية](README.ar.md) · [🇷🇺 Русский](README.ru.md) · [🇵🇱 Polski](README.pl.md) · [🇨🇿 Čeština](README.cs.md) · [🇳🇱 Nederlands](README.nl.md) · [🇹🇷 Türkçe](README.tr.md) · [🇺🇦 Українська](README.uk.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Indonesia](README.id.md) · [🇹🇭 ไทย](README.th.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇧🇩 বাংলা](README.bn.md) · [🇵🇰 اردو](README.ur.md) · [🇷🇴 Română](README.ro.md) · [🇸🇪 Svenska](README.sv.md) · [🇮🇹 Italiano](README.it.md) · [🇬🇷 Ελληνικά](README.el.md) · [🇭🇺 Magyar](README.hu.md) · [🇫🇮 Suomi](README.fi.md) · [🇩🇰 Dansk](README.da.md) · [🇳🇴 Norsk](README.no.md)

**你的 AI 编程助手会忘记一切。MemoTrail 解决了这个问题。**

[![PyPI version](https://img.shields.io/pypi/v/memotrail?color=blue)](https://pypi.org/project/memotrail/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/HalilHopa-Datatent/memotrail?style=social)](https://github.com/HalilHopa-Datatent/memotrail)

为 AI 编程助手打造的持久化记忆层。
每次会话都被记录，每个决策都可搜索，每段上下文都被铭记。

[快速开始](#快速开始) · [工作原理](#工作原理) · [可用工具](#可用工具) · [路线图](#路线图)

</div>

---

## v0.3.0 新特性

- **自动会话摘要** —— 每个会话都会生成 AI 摘要（无需 API 密钥）
- **自动决策提取** —— 使用模式匹配从对话中检测架构决策
- **BM25 关键词搜索** —— 新增 `search_keyword` 工具，适用于精确术语、错误信息、函数名
- **混合搜索** —— 使用倒数排名融合结合语义 + 关键词结果
- **Cursor IDE 支持** —— 从 `state.vscdb` 文件索引 Cursor 聊天历史
- **实时文件监控** —— 通过 watchdog 即时索引新会话（无需重启）
- **分块策略** —— 可选择基于 token、基于轮次或递归分割
- **VS Code 扩展** —— 直接在 VS Code 中搜索、索引和查看统计
- **69 个测试** —— 覆盖所有模块的全面测试

## 问题所在

每次新的 Claude Code 会话都从零开始。你的 AI 不记得昨天 3 小时的调试过程、上周做出的架构决策，也不记得已经失败过的方案。

**没有 MemoTrail：**
```
你：  "我们用 Redis 做缓存吧"
AI：  "好的，来配置 Redis"
         ... 两周后，新的会话 ...
你：  "我们为什么用 Redis？"
AI：  "我没有关于这个决策的上下文"
```

**有了 MemoTrail：**
```
你：  "我们为什么用 Redis？"
AI：  "根据 1 月 15 日的会话 —— 你评估了 Redis 和 Memcached。
      选择 Redis 是因为它的数据结构支持和持久化能力。
      讨论记录在第 42 次会话中。"
```

## 快速开始

```bash
# 1. 安装
pip install memotrail

# 2. 连接到 Claude Code
claude mcp add memotrail -- memotrail serve
```

就这样。MemoTrail 会在首次启动时自动索引你的历史记录。
开始新会话并询问：*"我们上周做了什么？"*


<div align="center">
<img src="../../demo.gif" alt="MemoTrail Demo" width="800">
<br>
<sub>Install → Connect → See stats → Search past sessions → Save memory → Duplicate &amp; contradiction detection</sub>
</div>

## 工作原理

| 步骤 | 发生了什么 |
|:----:|:-------------|
| **1. 记录** | MemoTrail 在启动时自动索引新会话 + 实时监控新文件 |
| **2. 分块** | 对话使用 token、轮次或递归策略进行拆分 |
| **3. 嵌入** | 每个分块使用 `all-MiniLM-L6-v2` 进行嵌入（约 80MB，CPU 运行） |
| **4. 提取** | 自动提取摘要和架构决策 |
| **5. 存储** | 向量存入 ChromaDB，元数据存入 SQLite —— 全部在 `~/.memotrail/` 下 |
| **6. 搜索** | 语义 + BM25 关键词搜索覆盖你的完整历史 |
| **7. 呈现** | 最相关的过往上下文在你需要时出现 |

> **100% 本地运行** —— 无需云服务，无需 API 密钥，数据不会离开你的设备。
>
> **多平台支持** —— 支持 Claude Code 和 Cursor IDE，更多平台即将推出。

## 可用工具

连接后，Claude Code 将获得以下 MCP 工具：

| 工具 | 描述 |
|------|-------------|
| `search_chats` | 对所有过往对话进行语义搜索 |
| `search_keyword` | BM25 关键词搜索 —— 适用于精确术语、函数名、错误信息 |
| `get_decisions` | 检索记录的架构决策（自动提取 + 手动） |
| `get_recent_sessions` | 列出最近的编程会话及 AI 生成摘要 |
| `get_session_detail` | 深入查看特定会话的内容 |
| `save_memory` | 手动保存重要事实或决策 |
| `memory_stats` | 查看索引统计和存储使用情况 |

## CLI 命令

```bash
memotrail serve                          # 启动 MCP 服务器（自动索引新会话）
memotrail search "redis caching decision"  # 从终端搜索
memotrail stats                          # 查看索引统计
memotrail index                          # 手动重新索引（可选）
```

## 架构

```
~/.memotrail/
├── chroma/          # 向量嵌入（ChromaDB）
└── memotrail.db     # 会话元数据（SQLite）
```

| 组件 | 技术 | 详情 |
|-----------|-----------|---------|
| 嵌入 | `all-MiniLM-L6-v2` | 约 80MB，CPU 运行 |
| 向量数据库 | ChromaDB | 持久化本地存储 |
| 关键词搜索 | BM25 | 纯 Python，无额外依赖 |
| 元数据 | SQLite | 单文件数据库 |
| 文件监控 | watchdog | 实时会话检测 |
| 协议 | MCP | Model Context Protocol |

### 支持的平台

| 平台 | 状态 | 格式 |
|----------|--------|--------|
| Claude Code | 已支持 | JSONL 会话文件 |
| Cursor IDE | 已支持 | state.vscdb (SQLite) |
| GitHub Copilot | 计划中 | — |

### 分块策略

| 策略 | 最佳用途 |
|----------|----------|
| `token`（默认） | 通用 —— 按 token 限制分组消息 |
| `turn` | 对话导向 —— 按用户+助手对分组 |
| `recursive` | 长内容 —— 按段落、句子、词拆分 |

## 为什么选择 MemoTrail？

| | MemoTrail | CLAUDE.md / 规则文件 | 手动笔记 |
|---|---|---|---|
| 自动化 | 是 —— 每次会话启动时索引 | 否 —— 需要手动编写 | 否 |
| 可搜索 | 语义搜索 | AI 读取，但仅限你写的内容 | 只有 Ctrl+F |
| 可扩展 | 数千个会话 | 单个文件 | 零散的文件 |
| 上下文感知 | 返回相关上下文 | 静态规则 | 手动查找 |
| 设置 | 5 分钟 | 持续维护 | 持续维护 |

MemoTrail 不是要替代 `CLAUDE.md` —— 而是补充它。规则文件用于指令，MemoTrail 用于记忆。

## 路线图

- [x] Claude Code 会话索引
- [x] 跨对话语义搜索
- [x] 带 7 个工具的 MCP 服务器
- [x] 用于索引和搜索的 CLI
- [x] 服务器启动时自动索引
- [x] 自动决策提取
- [x] 会话摘要
- [x] Cursor IDE 收集器
- [x] BM25 关键词搜索 + 混合搜索
- [x] 实时文件监控（watchdog）
- [x] 多种分块策略（token、turn、recursive）
- [x] VS Code 扩展
- [ ] Copilot 收集器
- [ ] 云同步（Pro）
- [ ] 团队记忆（Team）

## VS Code 扩展

MemoTrail 包含一个 VS Code 扩展，可直接在 IDE 中集成。

**可用命令：**
- `MemoTrail: Search Conversations` —— 语义搜索
- `MemoTrail: Keyword Search` —— BM25 关键词搜索
- `MemoTrail: Recent Sessions` —— 查看会话统计
- `MemoTrail: Index Sessions Now` —— 触发手动索引
- `MemoTrail: Show Stats` —— 显示索引统计

**设置：**
```bash
cd vscode-extension
npm install
npm run compile
# 然后在 VS Code 中按 F5 启动扩展开发宿主
```

## 开发

```bash
git clone https://github.com/HalilHopa-Datatent/memotrail.git
cd memotrail
pip install -e ".[dev]"
pytest
ruff check src/
```

## 贡献

欢迎贡献！请参阅 [CONTRIBUTING.md](../../docs/CONTRIBUTING.md) 了解指南。

## 许可证

MIT —— 请参阅 [LICENSE](../../LICENSE)

---

<div align="center">

**由 [Halil Hopa](https://halilhopa.com) 构建** · [memotrail.ai](https://memotrail.ai)

如果 MemoTrail 对你有帮助，请考虑在 GitHub 上给我们一个星标。

</div>
