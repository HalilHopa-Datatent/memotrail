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

## Yang Baru di v0.3.0

- **Ringkasan sesi otomatis** — setiap sesi mendapat ringkasan buatan AI (tanpa API key)
- **Ekstraksi keputusan otomatis** — keputusan arsitektur terdeteksi dari percakapan menggunakan pencocokan pola
- **Pencarian kata kunci BM25** — alat `search_keyword` baru untuk istilah tepat, pesan error, nama fungsi
- **Pencarian hibrida** — menggabungkan hasil semantik + kata kunci menggunakan reciprocal rank fusion
- **Dukungan Cursor IDE** — mengindeks riwayat chat Cursor dari file `state.vscdb`
- **Pemantauan file real-time** — sesi baru diindeks secara instan melalui watchdog (tanpa restart)
- **Strategi chunking** — pilih antara token-based, turn-based, atau pemisahan rekursif
- **Ekstensi VS Code** — cari, indeks, dan lihat statistik langsung dari VS Code
- **69 tes** — cakupan pengujian komprehensif di semua modul

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
| **1. Rekam** | MemoTrail mengindeks sesi baru secara otomatis saat startup + memantau file baru secara real-time |
| **2. Bagi** | Percakapan dibagi menggunakan strategi token, turn-based, atau recursive |
| **3. Embed** | Setiap bagian di-embed menggunakan `all-MiniLM-L6-v2` (~80MB, berjalan di CPU) |
| **4. Ekstrak** | Ringkasan dan keputusan arsitektur diekstrak secara otomatis |
| **5. Simpan** | Vektor ke ChromaDB, metadata ke SQLite — semua di `~/.memotrail/` |
| **6. Cari** | Pencarian semantik + BM25 kata kunci di seluruh riwayat Anda |
| **7. Tampilkan** | Konteks masa lalu paling relevan muncul tepat saat Anda membutuhkannya |

> **100% lokal** — tanpa cloud, tanpa API key, tidak ada data yang meninggalkan mesin Anda.
>
> **Multi-platform** — mendukung Claude Code dan Cursor IDE, lebih banyak segera hadir.

## Alat Tersedia

| Alat | Deskripsi |
|------|-------------|
| `search_chats` | Pencarian semantik di semua percakapan sebelumnya |
| `search_keyword` | Pencarian kata kunci BM25 — bagus untuk istilah tepat, nama fungsi, pesan error |
| `get_decisions` | Mengambil keputusan arsitektur yang tercatat (diekstrak otomatis + manual) |
| `get_recent_sessions` | Daftar sesi coding terbaru dengan ringkasan buatan AI |
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

## Arsitektur

```
~/.memotrail/
├── chroma/          # Embedding vektor (ChromaDB)
└── memotrail.db     # Metadata sesi (SQLite)
```

| Komponen | Teknologi | Detail |
|-----------|-----------|---------|
| Embedding | `all-MiniLM-L6-v2` | ~80MB, berjalan di CPU |
| Vector DB | ChromaDB | Penyimpanan lokal persisten |
| Pencarian Kata Kunci | BM25 | Python murni, tanpa dependensi tambahan |
| Metadata | SQLite | Database satu file |
| Pemantauan File | watchdog | Deteksi sesi real-time |
| Protokol | MCP | Model Context Protocol |

### Platform yang Didukung

| Platform | Status | Format |
|----------|--------|--------|
| Claude Code | Didukung | File sesi JSONL |
| Cursor IDE | Didukung | state.vscdb (SQLite) |
| GitHub Copilot | Direncanakan | — |

### Strategi Chunking

| Strategi | Terbaik untuk |
|----------|----------|
| `token` (default) | Penggunaan umum — mengelompokkan pesan hingga batas token |
| `turn` | Fokus percakapan — mengelompokkan pasangan pengguna+asisten |
| `recursive` | Konten panjang — membagi berdasarkan paragraf, kalimat, kata |

## Mengapa MemoTrail?

| | MemoTrail | CLAUDE.md / File aturan | Catatan manual |
|---|---|---|---|
| Otomatis | Ya — mengindeks setiap sesi dimulai | Tidak — Anda menulis sendiri | Tidak |
| Dapat dicari | Pencarian semantik | AI membaca, tapi hanya yang Anda tulis | Hanya Ctrl+F |
| Skalabilitas | Ribuan sesi | Satu file | File tersebar |
| Konteks-aware | Mengembalikan konteks relevan | Aturan statis | Pencarian manual |
| Setup | 5 menit | Selalu dipelihara | Selalu dipelihara |

MemoTrail tidak menggantikan `CLAUDE.md` — melengkapinya. File aturan untuk instruksi. MemoTrail untuk memori.

## Peta Jalan

- [x] Pengindeksan sesi Claude Code
- [x] Pencarian semantik antar percakapan
- [x] MCP server dengan 7 alat
- [x] CLI untuk pengindeksan dan pencarian
- [x] Pengindeksan otomatis saat server startup
- [x] Ekstraksi keputusan otomatis
- [x] Ringkasan sesi
- [x] Kolektor Cursor IDE
- [x] Pencarian kata kunci BM25 + pencarian hibrida
- [x] Pemantauan file real-time (watchdog)
- [x] Berbagai strategi chunking (token, turn, recursive)
- [x] Ekstensi VS Code
- [ ] Kolektor Copilot
- [ ] Sinkronisasi cloud (Pro)
- [ ] Memori tim (Team)

## Ekstensi VS Code

MemoTrail menyertakan ekstensi VS Code untuk integrasi langsung dengan IDE.

**Perintah yang tersedia:**
- `MemoTrail: Search Conversations` — pencarian semantik
- `MemoTrail: Keyword Search` — pencarian kata kunci BM25
- `MemoTrail: Recent Sessions` — lihat statistik sesi
- `MemoTrail: Index Sessions Now` — jalankan pengindeksan manual
- `MemoTrail: Show Stats` — tampilkan statistik pengindeksan

**Setup:**
```bash
cd vscode-extension
npm install
npm run compile
# Kemudian tekan F5 di VS Code untuk menjalankan Extension Development Host
```

## Pengembangan

```bash
git clone https://github.com/HalilHopa-Datatent/memotrail.git
cd memotrail
pip install -e ".[dev]"
pytest
ruff check src/
```

## Kontribusi

Kontribusi diterima! Lihat [CONTRIBUTING.md](../../docs/CONTRIBUTING.md) untuk panduan.

## Lisensi

MIT — lihat [LICENSE](../../LICENSE)

---

<div align="center">

**Dibuat oleh [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

Jika MemoTrail membantu Anda, pertimbangkan untuk memberi bintang di GitHub.

</div>
