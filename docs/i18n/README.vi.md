<div align="center">

# MemoTrail

> 🌐 Đây là bản dịch tự động. Chúng tôi hoan nghênh các bản sửa từ cộng đồng! · [English](../../README.md)

[🇨🇳 中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇵🇹 Português](README.pt.md) · [🇰🇷 한국어](README.ko.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇮🇱 עברית](README.he.md) · [🇸🇦 العربية](README.ar.md) · [🇷🇺 Русский](README.ru.md) · [🇵🇱 Polski](README.pl.md) · [🇨🇿 Čeština](README.cs.md) · [🇳🇱 Nederlands](README.nl.md) · [🇹🇷 Türkçe](README.tr.md) · [🇺🇦 Українська](README.uk.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Indonesia](README.id.md) · [🇹🇭 ไทย](README.th.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇧🇩 বাংলা](README.bn.md) · [🇵🇰 اردو](README.ur.md) · [🇷🇴 Română](README.ro.md) · [🇸🇪 Svenska](README.sv.md) · [🇮🇹 Italiano](README.it.md) · [🇬🇷 Ελληνικά](README.el.md) · [🇭🇺 Magyar](README.hu.md) · [🇫🇮 Suomi](README.fi.md) · [🇩🇰 Dansk](README.da.md) · [🇳🇴 Norsk](README.no.md)

**Trợ lý lập trình AI của bạn quên mọi thứ. MemoTrail giải quyết điều đó.**

[![PyPI version](https://img.shields.io/pypi/v/memotrail?color=blue)](https://pypi.org/project/memotrail/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/HalilHopa-Datatent/memotrail?style=social)](https://github.com/HalilHopa-Datatent/memotrail)

Tầng bộ nhớ bền vững cho trợ lý lập trình AI.
Mọi phiên được ghi lại, mọi quyết định có thể tìm kiếm, mọi ngữ cảnh được ghi nhớ.

</div>

---

## Có gì mới trong v0.3.0

- **Tóm tắt phiên tự động** — mỗi phiên được tóm tắt bằng AI (không cần API key)
- **Trích xuất quyết định tự động** — các quyết định kiến trúc được phát hiện từ cuộc trò chuyện bằng so khớp mẫu
- **Tìm kiếm từ khóa BM25** — công cụ `search_keyword` mới cho thuật ngữ chính xác, thông báo lỗi, tên hàm
- **Tìm kiếm kết hợp** — kết hợp kết quả ngữ nghĩa + từ khóa bằng reciprocal rank fusion
- **Hỗ trợ Cursor IDE** — lập chỉ mục lịch sử chat Cursor từ các tệp `state.vscdb`
- **Theo dõi tệp thời gian thực** — phiên mới được lập chỉ mục ngay lập tức qua watchdog (không cần khởi động lại)
- **Chiến lược phân đoạn** — chọn giữa token-based, turn-based hoặc chia đệ quy
- **Tiện ích mở rộng VS Code** — tìm kiếm, lập chỉ mục và xem thống kê trực tiếp từ VS Code
- **69 bài test** — phạm vi kiểm thử toàn diện trên tất cả module

## Vấn Đề

Mỗi phiên Claude Code mới bắt đầu từ số không. AI của bạn không nhớ phiên debug 3 giờ hôm qua, các quyết định kiến trúc tuần trước, hay các cách tiếp cận đã thất bại.

**Không có MemoTrail:**
```
Bạn: "Hãy dùng Redis cho caching"
AI:   "Được, hãy cấu hình Redis"
         ... 2 tuần sau, phiên mới ...
Bạn: "Tại sao chúng ta dùng Redis?"
AI:   "Tôi không có ngữ cảnh về quyết định đó"
```

**Với MemoTrail:**
```
Bạn: "Tại sao chúng ta dùng Redis?"
AI:   "Dựa trên phiên ngày 15 tháng 1 — bạn đã đánh giá Redis so với Memcached.
       Redis được chọn vì hỗ trợ cấu trúc dữ liệu và tính bền vững.
       Cuộc thảo luận ở phiên #42."
```

## Bắt Đầu Nhanh

```bash
# 1. Cài đặt
pip install memotrail

# 2. Kết nối với Claude Code
claude mcp add memotrail -- memotrail serve
```

Vậy thôi. MemoTrail tự động lập chỉ mục lịch sử của bạn khi khởi chạy lần đầu.

## Cách Hoạt Động

| Bước | Điều gì xảy ra |
|:----:|:-------------|
| **1. Ghi lại** | MemoTrail tự động lập chỉ mục phiên mới khi khởi động + theo dõi tệp mới theo thời gian thực |
| **2. Phân đoạn** | Cuộc trò chuyện được chia bằng chiến lược token, turn-based hoặc recursive |
| **3. Nhúng** | Mỗi đoạn được nhúng bằng `all-MiniLM-L6-v2` (~80MB, chạy trên CPU) |
| **4. Trích xuất** | Tóm tắt và quyết định kiến trúc được trích xuất tự động |
| **5. Lưu trữ** | Vector đến ChromaDB, metadata đến SQLite — tất cả trong `~/.memotrail/` |
| **6. Tìm kiếm** | Tìm kiếm ngữ nghĩa + BM25 từ khóa trên toàn bộ lịch sử của bạn |
| **7. Hiển thị** | Ngữ cảnh quá khứ liên quan nhất xuất hiện đúng lúc bạn cần |

> **100% cục bộ** — không cloud, không API key, không dữ liệu rời máy bạn.
>
> **Đa nền tảng** — hỗ trợ Claude Code và Cursor IDE, thêm nền tảng sắp ra mắt.

## Công Cụ Có Sẵn

| Công cụ | Mô tả |
|------|-------------|
| `search_chats` | Tìm kiếm ngữ nghĩa trong tất cả cuộc trò chuyện trước |
| `search_keyword` | Tìm kiếm từ khóa BM25 — tuyệt vời cho thuật ngữ chính xác, tên hàm, thông báo lỗi |
| `get_decisions` | Truy xuất các quyết định kiến trúc đã ghi (tự động trích xuất + thủ công) |
| `get_recent_sessions` | Liệt kê các phiên gần đây với tóm tắt do AI tạo |
| `get_session_detail` | Xem chi tiết nội dung một phiên cụ thể |
| `save_memory` | Lưu thủ công các sự kiện hoặc quyết định quan trọng |
| `memory_stats` | Xem thống kê lập chỉ mục và sử dụng lưu trữ |

## Lệnh CLI

```bash
memotrail serve                          # Khởi động server MCP (tự động lập chỉ mục phiên mới)
memotrail search "redis caching decision"  # Tìm kiếm từ terminal
memotrail stats                          # Xem thống kê lập chỉ mục
memotrail index                          # Lập chỉ mục lại thủ công (tùy chọn)
```

## Kiến Trúc

```
~/.memotrail/
├── chroma/          # Vector embedding (ChromaDB)
└── memotrail.db     # Metadata phiên (SQLite)
```

| Thành phần | Công nghệ | Chi tiết |
|-----------|-----------|---------|
| Embedding | `all-MiniLM-L6-v2` | ~80MB, chạy trên CPU |
| Vector DB | ChromaDB | Lưu trữ cục bộ, bền vững |
| Tìm kiếm từ khóa | BM25 | Python thuần, không cần thêm dependency |
| Metadata | SQLite | Cơ sở dữ liệu một tệp |
| Theo dõi tệp | watchdog | Phát hiện phiên thời gian thực |
| Giao thức | MCP | Model Context Protocol |

### Nền Tảng Được Hỗ Trợ

| Nền tảng | Trạng thái | Định dạng |
|----------|--------|--------|
| Claude Code | Được hỗ trợ | Tệp phiên JSONL |
| Cursor IDE | Được hỗ trợ | state.vscdb (SQLite) |
| GitHub Copilot | Đang lên kế hoạch | — |

### Chiến Lược Phân Đoạn

| Chiến lược | Phù hợp nhất cho |
|----------|----------|
| `token` (mặc định) | Sử dụng chung — nhóm tin nhắn đến giới hạn token |
| `turn` | Tập trung hội thoại — nhóm cặp người dùng+trợ lý |
| `recursive` | Nội dung dài — chia theo đoạn văn, câu, từ |

## Tại Sao Chọn MemoTrail?

| | MemoTrail | CLAUDE.md / Tệp rules | Ghi chú thủ công |
|---|---|---|---|
| Tự động | Có — lập chỉ mục mỗi lần bắt đầu phiên | Không — bạn tự viết | Không |
| Tìm kiếm được | Tìm kiếm ngữ nghĩa | AI đọc, nhưng chỉ những gì bạn viết | Chỉ Ctrl+F |
| Mở rộng | Hàng ngàn phiên | Một tệp duy nhất | Tệp rải rác |
| Nhận biết ngữ cảnh | Trả về ngữ cảnh liên quan | Quy tắc tĩnh | Tìm kiếm thủ công |
| Thiết lập | 5 phút | Phải duy trì liên tục | Phải duy trì liên tục |

MemoTrail không thay thế `CLAUDE.md` — nó bổ sung cho nó. Tệp rules dành cho hướng dẫn. MemoTrail dành cho bộ nhớ.

## Lộ Trình

- [x] Lập chỉ mục phiên Claude Code
- [x] Tìm kiếm ngữ nghĩa giữa các cuộc trò chuyện
- [x] MCP server với 7 công cụ
- [x] CLI để lập chỉ mục và tìm kiếm
- [x] Tự động lập chỉ mục khi server khởi động
- [x] Trích xuất quyết định tự động
- [x] Tóm tắt phiên
- [x] Bộ thu thập Cursor IDE
- [x] Tìm kiếm từ khóa BM25 + tìm kiếm kết hợp
- [x] Theo dõi tệp thời gian thực (watchdog)
- [x] Nhiều chiến lược phân đoạn (token, turn, recursive)
- [x] Tiện ích mở rộng VS Code
- [ ] Bộ thu thập Copilot
- [ ] Đồng bộ đám mây (Pro)
- [ ] Bộ nhớ nhóm (Team)

## Tiện Ích Mở Rộng VS Code

MemoTrail bao gồm tiện ích mở rộng VS Code để tích hợp trực tiếp với IDE.

**Các lệnh có sẵn:**
- `MemoTrail: Search Conversations` — tìm kiếm ngữ nghĩa
- `MemoTrail: Keyword Search` — tìm kiếm từ khóa BM25
- `MemoTrail: Recent Sessions` — xem thống kê phiên
- `MemoTrail: Index Sessions Now` — kích hoạt lập chỉ mục thủ công
- `MemoTrail: Show Stats` — hiển thị thống kê lập chỉ mục

**Thiết lập:**
```bash
cd vscode-extension
npm install
npm run compile
# Sau đó nhấn F5 trong VS Code để khởi chạy Extension Development Host
```

## Phát Triển

```bash
git clone https://github.com/HalilHopa-Datatent/memotrail.git
cd memotrail
pip install -e ".[dev]"
pytest
ruff check src/
```

## Đóng Góp

Đóng góp luôn được hoan nghênh! Xem [CONTRIBUTING.md](../../docs/CONTRIBUTING.md) để biết hướng dẫn.

## Giấy Phép

MIT — xem [LICENSE](../../LICENSE)

---

<div align="center">

**Được xây dựng bởi [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

Nếu MemoTrail giúp ích cho bạn, hãy cân nhắc cho một ngôi sao trên GitHub.

</div>
