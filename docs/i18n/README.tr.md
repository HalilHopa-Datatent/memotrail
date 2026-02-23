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

## v0.3.0'daki Yenilikler

- **Otomatik oturum ozetleme** -- her oturum yapay zeka tarafindan olusturulan bir ozet alir (API anahtari gerekmez)
- **Otomatik karar cikarma** -- mimari kararlar, oruntu eslestirme kullanilarak konusmalardan tespit edilir
- **BM25 anahtar kelime aramasi** -- kesin terimler, hata mesajlari, fonksiyon adlari icin yeni `search_keyword` araci
- **Hibrit arama** -- karsilikli siralama fuzyon yontemiyle anlamsal + anahtar kelime sonuclarini birlestirir
- **Cursor IDE destegi** -- `state.vscdb` dosyalarindan Cursor sohbet gecmisini indeksler
- **Gercek zamanli dosya izleme** -- yeni oturumlar watchdog araciligiyla aninda indekslenir (yeniden baslatma gerekmez)
- **Parcalama stratejileri** -- token tabanli, tur tabanli veya ozyinelemeli bolme arasinda secim yapin
- **VS Code eklentisi** -- VS Code icerisinden dogrudan arama, indeksleme ve istatistik goruntuleme
- **69 test** -- tum moduller icin kapsamli test kapsamasi

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
| **1. Kaydet** | MemoTrail başlangıçta yeni oturumları otomatik indeksler + gerçek zamanlı yeni dosyaları izler |
| **2. Böl** | Konuşmalar token, tur tabanlı veya özyinelemeli stratejilerle bölünür |
| **3. Göm** | Her parça `all-MiniLM-L6-v2` ile gömülür (~80MB, CPU'da çalışır) |
| **4. Çıkar** | Özetler ve mimari kararlar otomatik olarak çıkarılır |
| **5. Depola** | Vektörler ChromaDB'ye, meta veriler SQLite'a — hepsi `~/.memotrail/` altında |
| **6. Ara** | Anlamsal + BM25 anahtar kelime araması tüm geçmişinizde |
| **7. Göster** | En ilgili geçmiş bağlam tam ihtiyacınız olduğunda belirir |

> **%100 yerel** — bulut yok, API anahtarı yok, hiçbir veri makinenizi terk etmez.

> **Çoklu platform** — Claude Code ve Cursor IDE destekler, daha fazlası yakında.

## Mevcut Araçlar

Bağlandıktan sonra Claude Code şu MCP araçlarını kullanabilir:

| Araç | Açıklama |
|------|-------------|
| `search_chats` | Tüm geçmiş konuşmalarda anlamsal arama |
| `search_keyword` | BM25 anahtar kelime araması — kesin terimler, fonksiyon adları, hata mesajları için idealdir |
| `get_decisions` | Kaydedilmiş mimari kararları getir (otomatik çıkarılan + manuel) |
| `get_recent_sessions` | Son kodlama oturumlarını yapay zeka tarafından oluşturulan özetlerle listele |
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
| Anahtar Kelime Araması | BM25 | Saf Python, ek bağımlılık yok |
| Meta Veri | SQLite | Tek dosya veritabanı |
| Dosya İzleme | watchdog | Gerçek zamanlı oturum algılama |
| Protokol | MCP | Model Context Protocol |

#### Desteklenen Platformlar

| Platform | Durum | Detaylar |
|----------|-------|---------|
| Claude Code | Destekleniyor | JSONL oturum dosyaları |
| Cursor IDE | Destekleniyor | state.vscdb (SQLite) |
| GitHub Copilot | Planlanıyor | — |

#### Parçalama Stratejileri

| Strateji | Kullanım Alanı |
|----------|---------------|
| `token` (varsayılan) | Genel kullanım — mesajları token sınırına kadar gruplar |
| `turn` | Konuşma odaklı — kullanıcı+asistan çiftlerini gruplar |
| `recursive` | Uzun içerik — paragraflara, cümlelere, kelimelere göre böler |

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
- [x] 7 araçlı MCP sunucusu
- [x] İndeksleme ve arama için CLI
- [x] Sunucu başlangıcında otomatik indeksleme
- [x] Otomatik karar çıkarma
- [x] Oturum özetleme
- [x] Cursor IDE toplayıcı
- [x] BM25 anahtar kelime araması + hibrit arama
- [x] Gerçek zamanlı dosya izleme (watchdog)
- [x] Çoklu parçalama stratejileri (token, turn, recursive)
- [x] VS Code eklentisi
- [ ] Copilot toplayıcı
- [ ] Bulut senkronizasyonu (Pro)
- [ ] Takım hafızası (Team)

## VS Code Eklentisi

MemoTrail dogrudan VS Code icerisinde calisir. Komut paletinden su komutlari kullanabilirsiniz:

- **MemoTrail: Konusmalari Ara** -- gecmis oturumlarda anlamsal arama
- **MemoTrail: Anahtar Kelime Aramasi** -- BM25 anahtar kelime aramasi
- **MemoTrail: Son Oturumlar** -- son kodlama oturumlarini goruntule
- **MemoTrail: Oturumlari Simdi Indeksle** -- oturumlari hemen indeksle
- **MemoTrail: Istatistikleri Goster** -- indeksleme istatistiklerini gor

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
