<div align="center">

# MemoTrail

> 🌐 นี่คือการแปลอัตโนมัติ ยินดีรับการแก้ไขจากชุมชน! · [English](../../README.md)

[🇨🇳 中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇵🇹 Português](README.pt.md) · [🇰🇷 한국어](README.ko.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇮🇱 עברית](README.he.md) · [🇸🇦 العربية](README.ar.md) · [🇷🇺 Русский](README.ru.md) · [🇵🇱 Polski](README.pl.md) · [🇨🇿 Čeština](README.cs.md) · [🇳🇱 Nederlands](README.nl.md) · [🇹🇷 Türkçe](README.tr.md) · [🇺🇦 Українська](README.uk.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Indonesia](README.id.md) · [🇹🇭 ไทย](README.th.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇧🇩 বাংলা](README.bn.md) · [🇵🇰 اردو](README.ur.md) · [🇷🇴 Română](README.ro.md) · [🇸🇪 Svenska](README.sv.md) · [🇮🇹 Italiano](README.it.md) · [🇬🇷 Ελληνικά](README.el.md) · [🇭🇺 Magyar](README.hu.md) · [🇫🇮 Suomi](README.fi.md) · [🇩🇰 Dansk](README.da.md) · [🇳🇴 Norsk](README.no.md)

**ผู้ช่วยเขียนโค้ด AI ของคุณลืมทุกอย่าง MemoTrail แก้ปัญหานี้**

[![PyPI version](https://img.shields.io/pypi/v/memotrail?color=blue)](https://pypi.org/project/memotrail/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/HalilHopa-Datatent/memotrail?style=social)](https://github.com/HalilHopa-Datatent/memotrail)

ชั้นหน่วยความจำถาวรสำหรับผู้ช่วยเขียนโค้ด AI
ทุกเซสชันถูกบันทึก ทุกการตัดสินใจค้นหาได้ ทุกบริบทถูกจดจำ

</div>

---

## ปัญหา

ทุกเซสชันใหม่ของ Claude Code เริ่มต้นจากศูนย์ AI ของคุณไม่จำเซสชันดีบัก 3 ชั่วโมงเมื่อวาน การตัดสินใจด้านสถาปัตยกรรมเมื่อสัปดาห์ที่แล้ว หรือแนวทางที่ล้มเหลวไปแล้ว

**ไม่มี MemoTrail:**
```
คุณ: "ใช้ Redis สำหรับ caching กัน"
AI:   "ได้เลย มาตั้งค่า Redis กัน"
         ... 2 สัปดาห์ต่อมา เซสชันใหม่ ...
คุณ: "ทำไมเราถึงใช้ Redis?"
AI:   "ผมไม่มีบริบทเกี่ยวกับการตัดสินใจนั้น"
```

**มี MemoTrail:**
```
คุณ: "ทำไมเราถึงใช้ Redis?"
AI:   "จากเซสชันวันที่ 15 มกราคม — คุณประเมิน Redis กับ Memcached
       Redis ถูกเลือกเพราะรองรับโครงสร้างข้อมูลและความคงทน
       การสนทนาอยู่ในเซสชัน #42"
```

## เริ่มต้นอย่างรวดเร็ว

```bash
# 1. ติดตั้ง
pip install memotrail

# 2. เชื่อมต่อกับ Claude Code
claude mcp add memotrail -- memotrail serve
```

แค่นั้น MemoTrail จะจัดทำดัชนีประวัติของคุณโดยอัตโนมัติเมื่อเปิดใช้ครั้งแรก

## วิธีการทำงาน

| ขั้นตอน | สิ่งที่เกิดขึ้น |
|:----:|:-------------|
| **1. บันทึก** | MemoTrail จัดทำดัชนีเซสชันใหม่โดยอัตโนมัติทุกครั้งที่เซิร์ฟเวอร์เริ่ม |
| **2. แบ่ง** | บทสนทนาถูกแบ่งเป็นส่วนที่มีความหมาย |
| **3. ฝัง** | แต่ละส่วนถูกฝังด้วย `all-MiniLM-L6-v2` (~80MB, ทำงานบน CPU) |
| **4. เก็บ** | เวกเตอร์ไปที่ ChromaDB, เมตาดาต้าไปที่ SQLite — ทั้งหมดใน `~/.memotrail/` |
| **5. ค้นหา** | เซสชันถัดไป Claude ค้นหาเชิงความหมายทั่วประวัติทั้งหมดของคุณ |
| **6. แสดง** | บริบทในอดีตที่เกี่ยวข้องที่สุดปรากฏขึ้นเมื่อคุณต้องการ |

> **100% ในเครื่อง** — ไม่มีคลาวด์ ไม่มี API key ไม่มีข้อมูลออกจากเครื่องของคุณ

## เครื่องมือที่มี

| เครื่องมือ | คำอธิบาย |
|------|-------------|
| `search_chats` | ค้นหาเชิงความหมายในบทสนทนาทั้งหมด |
| `get_decisions` | ดึงการตัดสินใจด้านสถาปัตยกรรมที่บันทึกไว้ |
| `get_recent_sessions` | แสดงรายการเซสชันล่าสุดพร้อมสรุป |
| `get_session_detail` | ดูรายละเอียดเนื้อหาของเซสชันที่ระบุ |
| `save_memory` | บันทึกข้อเท็จจริงหรือการตัดสินใจสำคัญด้วยตนเอง |
| `memory_stats` | ดูสถิติการจัดทำดัชนีและการใช้พื้นที่จัดเก็บ |

## คำสั่ง CLI

```bash
memotrail serve                          # เริ่มเซิร์ฟเวอร์ MCP (จัดทำดัชนีเซสชันใหม่โดยอัตโนมัติ)
memotrail search "redis caching decision"  # ค้นหาจากเทอร์มินัล
memotrail stats                          # ดูสถิติการจัดทำดัชนี
memotrail index                          # จัดทำดัชนีใหม่ด้วยตนเอง (ไม่จำเป็น)
```

## สัญญาอนุญาต

MIT — ดู [LICENSE](../../LICENSE)

---

<div align="center">

**สร้างโดย [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

หาก MemoTrail ช่วยคุณได้ โปรดพิจารณาให้ดาวบน GitHub

</div>
