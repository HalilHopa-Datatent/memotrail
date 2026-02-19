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
| **1. Ghi lại** | MemoTrail tự động lập chỉ mục phiên mới mỗi khi server khởi động |
| **2. Phân đoạn** | Cuộc trò chuyện được chia thành các phân đoạn có ý nghĩa |
| **3. Nhúng** | Mỗi đoạn được nhúng bằng `all-MiniLM-L6-v2` (~80MB, chạy trên CPU) |
| **4. Lưu trữ** | Vector đến ChromaDB, metadata đến SQLite — tất cả trong `~/.memotrail/` |
| **5. Tìm kiếm** | Phiên tiếp theo, Claude tìm kiếm ngữ nghĩa toàn bộ lịch sử của bạn |
| **6. Hiển thị** | Ngữ cảnh quá khứ liên quan nhất xuất hiện đúng lúc bạn cần |

> **100% cục bộ** — không cloud, không API key, không dữ liệu rời máy bạn.

## Công Cụ Có Sẵn

| Công cụ | Mô tả |
|------|-------------|
| `search_chats` | Tìm kiếm ngữ nghĩa trong tất cả cuộc trò chuyện trước |
| `get_decisions` | Truy xuất các quyết định kiến trúc đã ghi |
| `get_recent_sessions` | Liệt kê các phiên gần đây với tóm tắt |
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

## Giấy Phép

MIT — xem [LICENSE](../../LICENSE)

---

<div align="center">

**Được xây dựng bởi [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

Nếu MemoTrail giúp ích cho bạn, hãy cân nhắc cho một ngôi sao trên GitHub.

</div>
