<div align="center">

# MemoTrail

> 🌐 זהו תרגום אוטומטי. תיקונים מהקהילה מתקבלים בברכה! · [English](../../README.md)

[🇨🇳 中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇵🇹 Português](README.pt.md) · [🇰🇷 한국어](README.ko.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇮🇱 עברית](README.he.md) · [🇸🇦 العربية](README.ar.md) · [🇷🇺 Русский](README.ru.md) · [🇵🇱 Polski](README.pl.md) · [🇨🇿 Čeština](README.cs.md) · [🇳🇱 Nederlands](README.nl.md) · [🇹🇷 Türkçe](README.tr.md) · [🇺🇦 Українська](README.uk.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Indonesia](README.id.md) · [🇹🇭 ไทย](README.th.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇧🇩 বাংলা](README.bn.md) · [🇵🇰 اردو](README.ur.md) · [🇷🇴 Română](README.ro.md) · [🇸🇪 Svenska](README.sv.md) · [🇮🇹 Italiano](README.it.md) · [🇬🇷 Ελληνικά](README.el.md) · [🇭🇺 Magyar](README.hu.md) · [🇫🇮 Suomi](README.fi.md) · [🇩🇰 Dansk](README.da.md) · [🇳🇴 Norsk](README.no.md)

**עוזר הקוד ה-AI שלך שוכח הכל. MemoTrail פותר את זה.**

[![PyPI version](https://img.shields.io/pypi/v/memotrail?color=blue)](https://pypi.org/project/memotrail/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/HalilHopa-Datatent/memotrail?style=social)](https://github.com/HalilHopa-Datatent/memotrail)

שכבת זיכרון קבועה לעוזרי קוד AI.
כל סשן מתועד, כל החלטה ניתנת לחיפוש, כל הקשר נזכר.

[התחלה מהירה](#התחלה-מהירה) · [איך זה עובד](#איך-זה-עובד) · [כלים זמינים](#כלים-זמינים) · [מפת דרכים](#מפת-דרכים)

</div>

---

## הבעיה

כל סשן חדש של Claude Code מתחיל מאפס. ה-AI שלך לא זוכר את סשן הדיבאג של 3 שעות מאתמול, את ההחלטות הארכיטקטוניות מהשבוע שעבר, או את הגישות שכבר נכשלו.

**ללא MemoTrail:**
```
אתה: "בוא נשתמש ב-Redis לקאשינג"
AI:    "בטח, בוא נגדיר Redis"
         ... שבועיים אחר כך, סשן חדש ...
אתה: "למה אנחנו משתמשים ב-Redis?"
AI:    "אין לי הקשר לגבי ההחלטה הזו"
```

**עם MemoTrail:**
```
אתה: "למה אנחנו משתמשים ב-Redis?"
AI:    "על סמך הסשן מ-15 בינואר — השווית בין Redis ל-Memcached.
        Redis נבחר בזכות תמיכה במבני נתונים ופרסיסטנטיות.
        הדיון בסשן #42."
```

## התחלה מהירה

```bash
# 1. התקנה
pip install memotrail

# 2. חיבור ל-Claude Code
claude mcp add memotrail -- memotrail serve
```

זהו. MemoTrail מאנדקס אוטומטית את ההיסטוריה שלך בהפעלה הראשונה.
התחל סשן חדש ושאל: *"על מה עבדנו בשבוע שעבר?"*

## איך זה עובד

| שלב | מה קורה |
|:----:|:-------------|
| **1. הקלטה** | MemoTrail מאנדקס אוטומטית סשנים חדשים בכל הפעלה של השרת |
| **2. חלוקה** | שיחות מחולקות למקטעים משמעותיים |
| **3. הטמעה** | כל מקטע מוטמע באמצעות `all-MiniLM-L6-v2` (~80MB, רץ על CPU) |
| **4. אחסון** | וקטורים הולכים ל-ChromaDB, מטא-דאטה ל-SQLite — הכל תחת `~/.memotrail/` |
| **5. חיפוש** | בסשן הבא, Claude מחפש סמנטית בכל ההיסטוריה שלך |
| **6. הצגה** | ההקשר העבר הרלוונטי ביותר מופיע בדיוק כשאתה צריך |

> **100% מקומי** — ללא ענן, ללא מפתחות API, אף מידע לא עוזב את המחשב שלך.

## כלים זמינים

לאחר החיבור, Claude Code מקבל את כלי ה-MCP האלה:

| כלי | תיאור |
|------|-------------|
| `search_chats` | חיפוש סמנטי בכל השיחות הקודמות |
| `get_decisions` | אחזור החלטות ארכיטקטוניות מתועדות |
| `get_recent_sessions` | רשימת סשנים אחרונים עם סיכומים |
| `get_session_detail` | צלילה עמוקה לתוכן של סשן ספציפי |
| `save_memory` | שמירה ידנית של עובדות או החלטות חשובות |
| `memory_stats` | צפייה בסטטיסטיקות אינדוקס ושימוש באחסון |

## פקודות CLI

```bash
memotrail serve                          # הפעלת שרת MCP (אינדוקס אוטומטי של סשנים חדשים)
memotrail search "redis caching decision"  # חיפוש מהטרמינל
memotrail stats                          # צפייה בסטטיסטיקות אינדוקס
memotrail index                          # אינדוקס מחדש ידני (אופציונלי)
```

## ארכיטקטורה

```
~/.memotrail/
├── chroma/          # הטמעות וקטוריות (ChromaDB)
└── memotrail.db     # מטא-דאטה של סשנים (SQLite)
```

| רכיב | טכנולוגיה | פרטים |
|-----------|-----------|---------|
| הטמעות | `all-MiniLM-L6-v2` | ~80MB, רץ על CPU |
| מסד וקטורי | ChromaDB | אחסון מקומי קבוע |
| מטא-דאטה | SQLite | מסד נתונים בקובץ בודד |
| פרוטוקול | MCP | Model Context Protocol |

## למה MemoTrail?

| | MemoTrail | CLAUDE.md / קבצי כללים | הערות ידניות |
|---|---|---|---|
| אוטומטי | כן — מאנדקס בכל התחלת סשן | לא — אתה כותב | לא |
| ניתן לחיפוש | חיפוש סמנטי | AI קורא, אבל רק מה שכתבת | רק Ctrl+F |
| סקיילבילי | אלפי סשנים | קובץ בודד | קבצים מפוזרים |
| מודע להקשר | מחזיר הקשר רלוונטי | כללים סטטיים | חיפוש ידני |
| הגדרה | 5 דקות | תחזוקה מתמדת | תחזוקה מתמדת |

MemoTrail לא מחליף את `CLAUDE.md` — הוא משלים אותו. קבצי כללים להוראות. MemoTrail לזיכרון.

## מפת דרכים

- [x] אינדוקס סשנים של Claude Code
- [x] חיפוש סמנטי בין שיחות
- [x] שרת MCP עם 6 כלים
- [x] CLI לאינדוקס וחיפוש
- [x] אינדוקס אוטומטי בהפעלת השרת
- [ ] חילוץ החלטות אוטומטי
- [ ] סיכום סשנים
- [ ] אספן Cursor
- [ ] אספן Copilot
- [ ] הרחבת VS Code
- [ ] סנכרון ענן (Pro)
- [ ] זיכרון צוות (Team)

## פיתוח

```bash
git clone https://github.com/HalilHopa-Datatent/memotrail.git
cd memotrail
pip install -e ".[dev]"
pytest
ruff check src/
```

## תרומה

תרומות מתקבלות בברכה! ראה [CONTRIBUTING.md](../../docs/CONTRIBUTING.md) להנחיות.

## רישיון

MIT — ראה [LICENSE](../../LICENSE)

---

<div align="center">

**נבנה על ידי [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

אם MemoTrail עוזר לך, שקול לתת כוכב ב-GitHub.

</div>
