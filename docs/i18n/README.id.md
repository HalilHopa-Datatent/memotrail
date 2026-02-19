<div align="center">

# MemoTrail

> 🌐 Ini adalah terjemahan otomatis. Koreksi dari komunitas sangat diterima! · [English](../../README.md)

[🇨🇳 中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇵🇹 Português](README.pt.md) · [🇰🇷 한국어](README.ko.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇮🇱 עברית](README.he.md) · [🇸🇦 العربية](README.ar.md) · [🇷🇺 Русский](README.ru.md) · [🇵🇱 Polski](README.pl.md) · [🇨🇿 Čeština](README.cs.md) · [🇳🇱 Nederlands](README.nl.md) · [🇹🇷 Türkçe](README.tr.md) · [🇺🇦 Українська](README.uk.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Indonesia](README.id.md) · [🇹🇭 ไทย](README.th.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇧🇩 বাংলা](README.bn.md) · [🇵🇰 اردو](README.ur.md) · [🇷🇴 Română](README.ro.md) · [🇸🇪 Svenska](README.sv.md) · [🇮🇹 Italiano](README.it.md) · [🇬🇷 Ελληνικά](README.el.md) · [🇭🇺 Magyar](README.hu.md) · [🇫🇮 Suomi](README.fi.md) · [🇩🇰 Dansk](README.da.md) · [🇳🇴 Norsk](README.no.md)

**Asisten coding AI Anda melupakan segalanya. MemoTrail memperbaiki itu.**

[![PyPI version](https://img.shields.io/pypi/v/memotrail?color=blue)](https://pypi.org/project/memotrail/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/HalilHopa-Datatent/memotrail?style=social)](https://github.com/HalilHopa-Datatent/memotrail)

Lapisan memori persisten untuk asisten coding AI.
Setiap sesi direkam, setiap keputusan dapat dicari, setiap konteks diingat.

</div>

---

## Masalahnya

Setiap sesi baru Claude Code dimulai dari nol. AI Anda tidak mengingat sesi debugging 3 jam kemarin, keputusan arsitektur minggu lalu, atau pendekatan yang sudah gagal.

**Tanpa MemoTrail:**
```
Anda: "Mari gunakan Redis untuk caching"
AI:    "Tentu, mari siapkan Redis"
         ... 2 minggu kemudian, sesi baru ...
Anda: "Mengapa kita menggunakan Redis?"
AI:    "Saya tidak punya konteks tentang keputusan itu"
```

**Dengan MemoTrail:**
```
Anda: "Mengapa kita menggunakan Redis?"
AI:    "Berdasarkan sesi 15 Januari — Anda mengevaluasi Redis vs Memcached.
        Redis dipilih karena dukungan struktur data dan persistensi.
        Diskusi ada di sesi #42."
```

## Mulai Cepat

```bash
# 1. Instal
pip install memotrail

# 2. Hubungkan ke Claude Code
claude mcp add memotrail -- memotrail serve
```

Itu saja. MemoTrail secara otomatis mengindeks riwayat Anda saat pertama kali diluncurkan.

## Cara Kerjanya

| Langkah | Apa yang terjadi |
|:----:|:-------------|
| **1. Rekam** | MemoTrail mengindeks sesi baru secara otomatis setiap server dimulai |
| **2. Bagi** | Percakapan dibagi menjadi segmen bermakna |
| **3. Embed** | Setiap bagian di-embed menggunakan `all-MiniLM-L6-v2` (~80MB, berjalan di CPU) |
| **4. Simpan** | Vektor ke ChromaDB, metadata ke SQLite — semua di `~/.memotrail/` |
| **5. Cari** | Di sesi berikutnya, Claude mencari secara semantik di seluruh riwayat Anda |
| **6. Tampilkan** | Konteks masa lalu paling relevan muncul tepat saat Anda membutuhkannya |

> **100% lokal** — tanpa cloud, tanpa API key, tidak ada data yang meninggalkan mesin Anda.

## Alat Tersedia

| Alat | Deskripsi |
|------|-------------|
| `search_chats` | Pencarian semantik di semua percakapan sebelumnya |
| `get_decisions` | Mengambil keputusan arsitektur yang tercatat |
| `get_recent_sessions` | Daftar sesi coding terbaru dengan ringkasan |
| `get_session_detail` | Melihat detail konten sesi tertentu |
| `save_memory` | Menyimpan fakta atau keputusan penting secara manual |
| `memory_stats` | Melihat statistik pengindeksan dan penggunaan penyimpanan |

## Perintah CLI

```bash
memotrail serve                          # Mulai server MCP (mengindeks sesi baru secara otomatis)
memotrail search "redis caching decision"  # Cari dari terminal
memotrail stats                          # Lihat statistik pengindeksan
memotrail index                          # Indeks ulang secara manual (opsional)
```

## Lisensi

MIT — lihat [LICENSE](../../LICENSE)

---

<div align="center">

**Dibuat oleh [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

Jika MemoTrail membantu Anda, pertimbangkan untuk memberi bintang di GitHub.

</div>
