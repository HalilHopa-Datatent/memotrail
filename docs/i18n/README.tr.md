<div align="center">

# MemoTrail

> 🌐 Bu otomatik bir çeviridir. Topluluk düzeltmeleri memnuniyetle karşılanır! · [English](../../README.md)

[🇨🇳 中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇵🇹 Português](README.pt.md) · [🇰🇷 한국어](README.ko.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇮🇱 עברית](README.he.md) · [🇸🇦 العربية](README.ar.md) · [🇷🇺 Русский](README.ru.md) · [🇵🇱 Polski](README.pl.md) · [🇨🇿 Čeština](README.cs.md) · [🇳🇱 Nederlands](README.nl.md) · [🇹🇷 Türkçe](README.tr.md) · [🇺🇦 Українська](README.uk.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Indonesia](README.id.md) · [🇹🇭 ไทย](README.th.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇧🇩 বাংলা](README.bn.md) · [🇵🇰 اردو](README.ur.md) · [🇷🇴 Română](README.ro.md) · [🇸🇪 Svenska](README.sv.md) · [🇮🇹 Italiano](README.it.md) · [🇬🇷 Ελληνικά](README.el.md) · [🇭🇺 Magyar](README.hu.md) · [🇫🇮 Suomi](README.fi.md) · [🇩🇰 Dansk](README.da.md) · [🇳🇴 Norsk](README.no.md)

**AI kodlama asistanınız her şeyi unutuyor. MemoTrail bunu çözüyor.**

[![PyPI version](https://img.shields.io/pypi/v/memotrail?color=blue)](https://pypi.org/project/memotrail/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/HalilHopa-Datatent/memotrail?style=social)](https://github.com/HalilHopa-Datatent/memotrail)

AI kodlama asistanları için kalıcı hafıza katmanı.
Her oturum kaydedilir, her karar aranabilir, her bağlam hatırlanır.

[Hızlı Başlangıç](#hızlı-başlangıç) · [Nasıl Çalışır](#nasıl-çalışır) · [Mevcut Araçlar](#mevcut-araçlar) · [Yol Haritası](#yol-haritası)

</div>

---

## Problem

Her yeni Claude Code oturumu sıfırdan başlar. AI'nız dünkü 3 saatlik hata ayıklama oturumunu, geçen hafta aldığınız mimari kararları ya da daha önce başarısız olan yaklaşımları hatırlamaz.

**MemoTrail olmadan:**
```
Sen: "Cache için Redis kullanalım"
AI:   "Tabii, Redis'i kuralım"
         ... 2 hafta sonra, yeni oturum ...
Sen: "Neden Redis kullanıyoruz?"
AI:   "Bu kararla ilgili bir bağlamım yok"
```

**MemoTrail ile:**
```
Sen: "Neden Redis kullanıyoruz?"
AI:   "15 Ocak tarihli oturuma göre — Redis ve Memcached'i karşılaştırdın.
       Redis, veri yapısı desteği ve kalıcılık nedeniyle seçildi.
       Tartışma #42 numaralı oturumda."
```

## Hızlı Başlangıç

```bash
# 1. Yükle
pip install memotrail

# 2. Claude Code'a bağla
claude mcp add memotrail -- memotrail serve
```

Bu kadar. MemoTrail ilk açılışta geçmişinizi otomatik olarak indeksler.
Yeni bir oturum başlatın ve sorun: *"Geçen hafta ne üzerinde çalıştık?"*

## Nasıl Çalışır

| Adım | Ne olur |
|:----:|:-------------|
| **1. Kaydet** | MemoTrail her sunucu başlangıcında yeni oturumları otomatik indeksler |
| **2. Böl** | Konuşmalar anlamlı parçalara bölünür |
| **3. Göm** | Her parça `all-MiniLM-L6-v2` ile gömülür (~80MB, CPU'da çalışır) |
| **4. Depola** | Vektörler ChromaDB'ye, meta veriler SQLite'a — hepsi `~/.memotrail/` altında |
| **5. Ara** | Bir sonraki oturumda Claude tüm geçmişinizi anlamsal olarak arar |
| **6. Göster** | En ilgili geçmiş bağlam tam ihtiyacınız olduğunda belirir |

> **%100 yerel** — bulut yok, API anahtarı yok, hiçbir veri makinenizi terk etmez.

## Mevcut Araçlar

Bağlandıktan sonra Claude Code şu MCP araçlarını kullanabilir:

| Araç | Açıklama |
|------|-------------|
| `search_chats` | Tüm geçmiş konuşmalarda anlamsal arama |
| `get_decisions` | Kaydedilmiş mimari kararları getir |
| `get_recent_sessions` | Son kodlama oturumlarını özetleriyle listele |
| `get_session_detail` | Belirli bir oturumun içeriğini detaylı incele |
| `save_memory` | Önemli gerçekleri veya kararları elle kaydet |
| `memory_stats` | İndeksleme istatistikleri ve depolama kullanımını gör |

## CLI Komutları

```bash
memotrail serve                          # MCP sunucusunu başlat (yeni oturumları otomatik indeksler)
memotrail search "redis caching decision"  # Terminalden ara
memotrail stats                          # İndeksleme istatistiklerini gör
memotrail index                          # Elle yeniden indeksle (isteğe bağlı)
```

## Mimari

```
~/.memotrail/
├── chroma/          # Vektör gömmeleri (ChromaDB)
└── memotrail.db     # Oturum meta verileri (SQLite)
```

| Bileşen | Teknoloji | Detaylar |
|-----------|-----------|---------|
| Gömmeler | `all-MiniLM-L6-v2` | ~80MB, CPU'da çalışır |
| Vektör DB | ChromaDB | Kalıcı yerel depolama |
| Meta Veri | SQLite | Tek dosya veritabanı |
| Protokol | MCP | Model Context Protocol |

## Neden MemoTrail?

| | MemoTrail | CLAUDE.md / Kural dosyaları | Elle notlar |
|---|---|---|---|
| Otomatik | Evet — her oturum başlangıcında indeksler | Hayır — siz yazarsınız | Hayır |
| Aranabilir | Anlamsal arama | AI okur, ama sadece yazdıklarınızı | Sadece Ctrl+F |
| Ölçeklenebilir | Binlerce oturum | Tek dosya | Dağınık dosyalar |
| Bağlam farkında | İlgili bağlamı döndürür | Statik kurallar | Elle arama |
| Kurulum | 5 dakika | Sürekli bakım | Sürekli bakım |

MemoTrail `CLAUDE.md`'nin yerine geçmez — onu tamamlar. Kural dosyaları talimatlar içindir. MemoTrail hafıza içindir.

## Yol Haritası

- [x] Claude Code oturum indeksleme
- [x] Konuşmalar arası anlamsal arama
- [x] 6 araçlı MCP sunucusu
- [x] İndeksleme ve arama için CLI
- [x] Sunucu başlangıcında otomatik indeksleme
- [ ] Otomatik karar çıkarma
- [ ] Oturum özetleme
- [ ] Cursor toplayıcı
- [ ] Copilot toplayıcı
- [ ] VS Code eklentisi
- [ ] Bulut senkronizasyonu (Pro)
- [ ] Takım hafızası (Team)

## Geliştirme

```bash
git clone https://github.com/HalilHopa-Datatent/memotrail.git
cd memotrail
pip install -e ".[dev]"
pytest
ruff check src/
```

## Katkıda Bulunma

Katkılar memnuniyetle karşılanır! Yönergeler için [CONTRIBUTING.md](../../docs/CONTRIBUTING.md) dosyasına bakın.

## Lisans

MIT — [LICENSE](../../LICENSE) dosyasına bakın

---

<div align="center">

**[Halil Hopa](https://halilhopa.com) tarafından geliştirildi** · [memotrail.ai](https://memotrail.ai)

MemoTrail işinize yarıyorsa, GitHub'da bir yıldız vermeyi düşünün.

</div>
