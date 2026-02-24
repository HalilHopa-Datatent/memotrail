<div align="center">

# MemoTrail

> 🌐 이것은 자동 번역입니다. 커뮤니티 수정을 환영합니다! · [English](../../README.md)

[🇨🇳 中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇵🇹 Português](README.pt.md) · [🇰🇷 한국어](README.ko.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇮🇱 עברית](README.he.md) · [🇸🇦 العربية](README.ar.md) · [🇷🇺 Русский](README.ru.md) · [🇵🇱 Polski](README.pl.md) · [🇨🇿 Čeština](README.cs.md) · [🇳🇱 Nederlands](README.nl.md) · [🇹🇷 Türkçe](README.tr.md) · [🇺🇦 Українська](README.uk.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Indonesia](README.id.md) · [🇹🇭 ไทย](README.th.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇧🇩 বাংলা](README.bn.md) · [🇵🇰 اردو](README.ur.md) · [🇷🇴 Română](README.ro.md) · [🇸🇪 Svenska](README.sv.md) · [🇮🇹 Italiano](README.it.md) · [🇬🇷 Ελληνικά](README.el.md) · [🇭🇺 Magyar](README.hu.md) · [🇫🇮 Suomi](README.fi.md) · [🇩🇰 Dansk](README.da.md) · [🇳🇴 Norsk](README.no.md)

**당신의 AI 코딩 어시스턴트는 모든 것을 잊습니다. MemoTrail이 이를 해결합니다.**

[![PyPI version](https://img.shields.io/pypi/v/memotrail?color=blue)](https://pypi.org/project/memotrail/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/HalilHopa-Datatent/memotrail?style=social)](https://github.com/HalilHopa-Datatent/memotrail)

AI 코딩 어시스턴트를 위한 영구 메모리 레이어.
모든 세션이 기록되고, 모든 결정이 검색 가능하며, 모든 컨텍스트가 기억됩니다.

[빠른 시작](#빠른-시작) · [작동 방식](#작동-방식) · [사용 가능한 도구](#사용-가능한-도구) · [로드맵](#로드맵)

</div>

---

## v0.3.0 새로운 기능

- **자동 세션 요약** -- 모든 세션에 AI 생성 요약이 제공됩니다 (API 키 불필요)
- **자동 결정 추출** -- 패턴 매칭을 통해 대화에서 아키텍처 결정을 감지
- **BM25 키워드 검색** -- 정확한 용어, 오류 메시지, 함수명에 적합한 새로운 `search_keyword` 도구
- **하이브리드 검색** -- 역순위 융합을 사용하여 시맨틱 + 키워드 결과를 결합
- **Cursor IDE 지원** -- `state.vscdb` 파일에서 Cursor 채팅 기록을 인덱싱
- **실시간 파일 감시** -- watchdog을 통해 새 세션을 즉시 인덱싱 (재시작 불필요)
- **청킹 전략** -- 토큰 기반, 턴 기반 또는 재귀적 분할 중 선택 가능
- **VS Code 확장 프로그램** -- VS Code에서 직접 검색, 인덱싱, 통계 확인
- **69개 테스트** -- 모든 모듈에 걸친 포괄적인 테스트 커버리지

## 문제점

새로운 Claude Code 세션은 매번 처음부터 시작됩니다. AI는 어제 3시간 동안의 디버깅 세션, 지난주에 내린 아키텍처 결정, 이미 실패한 접근 방식을 기억하지 못합니다.

**MemoTrail 없이:**
```
당신: "캐싱에 Redis를 사용하자"
AI:   "네, Redis를 설정하겠습니다"
         ... 2주 후, 새 세션 ...
당신: "왜 Redis를 사용하고 있지?"
AI:   "해당 결정에 대한 컨텍스트가 없습니다"
```

**MemoTrail과 함께:**
```
당신: "왜 Redis를 사용하고 있지?"
AI:   "1월 15일 세션에 따르면 — Redis와 Memcached를 평가했습니다.
      데이터 구조 지원과 영속성 때문에 Redis가 선택되었습니다.
      해당 논의는 세션 #42에 있습니다."
```

## 빠른 시작

```bash
# 1. 설치
pip install memotrail

# 2. Claude Code에 연결
claude mcp add memotrail -- memotrail serve
```

끝입니다. MemoTrail은 첫 실행 시 자동으로 히스토리를 인덱싱합니다.
새 세션을 시작하고 물어보세요: *"지난주에 무엇을 작업했나요?"*


<div align="center">
<img src="../../demo.gif" alt="MemoTrail Demo" width="800">
<br>
<sub>Install → Connect → See stats → Search past sessions → Save memory → Duplicate &amp; contradiction detection</sub>
</div>

## 작동 방식

| 단계 | 무슨 일이 일어나는가 |
|:----:|:-------------|
| **1. 기록** | MemoTrail은 시작 시 새 세션을 자동 인덱싱 + 실시간으로 새 파일 감시 |
| **2. 분할** | 대화가 토큰, 턴 기반 또는 재귀적 전략으로 분할됨 |
| **3. 임베딩** | 각 청크가 `all-MiniLM-L6-v2`로 임베딩 (약 80MB, CPU에서 실행) |
| **4. 추출** | 요약과 아키텍처 결정이 자동으로 추출됨 |
| **5. 저장** | 벡터는 ChromaDB에, 메타데이터는 SQLite에 -- 모두 `~/.memotrail/` 아래 |
| **6. 검색** | 시맨틱 + BM25 키워드 검색으로 전체 히스토리를 횡단 |
| **7. 표시** | 가장 관련성 높은 과거 컨텍스트가 필요할 때 나타남 |

> **100% 로컬** -- 클라우드 없음, API 키 불필요, 데이터가 머신을 떠나지 않습니다.
>
> **멀티플랫폼** -- Claude Code와 Cursor IDE를 지원하며, 더 많은 플랫폼이 곧 추가될 예정입니다.

## 사용 가능한 도구

연결되면 Claude Code는 다음 MCP 도구를 사용할 수 있습니다:

| 도구 | 설명 |
|------|-------------|
| `search_chats` | 모든 과거 대화에 대한 시맨틱 검색 |
| `search_keyword` | BM25 키워드 검색 -- 정확한 용어, 함수명, 오류 메시지에 적합 |
| `get_decisions` | 기록된 아키텍처 결정 조회 (자동 추출 + 수동) |
| `get_recent_sessions` | 최근 코딩 세션을 AI 생성 요약과 함께 목록 표시 |
| `get_session_detail` | 특정 세션의 내용을 상세히 확인 |
| `save_memory` | 중요한 사실이나 결정을 수동으로 저장 |
| `memory_stats` | 인덱싱 통계 및 저장소 사용량 확인 |

## CLI 명령어

```bash
memotrail serve                          # MCP 서버 시작 (새 세션 자동 인덱싱)
memotrail search "redis caching decision"  # 터미널에서 검색
memotrail stats                          # 인덱싱 통계 확인
memotrail index                          # 수동 재인덱싱 (선택사항)
```

## 아키텍처

```
~/.memotrail/
├── chroma/          # 벡터 임베딩 (ChromaDB)
└── memotrail.db     # 세션 메타데이터 (SQLite)
```

| 구성 요소 | 기술 | 상세 |
|-----------|-----------|---------|
| 임베딩 | `all-MiniLM-L6-v2` | 약 80MB, CPU에서 실행 |
| 벡터 DB | ChromaDB | 영구 로컬 저장소 |
| 키워드 검색 | BM25 | 순수 Python, 추가 의존성 없음 |
| 메타데이터 | SQLite | 단일 파일 데이터베이스 |
| 파일 감시 | watchdog | 실시간 세션 감지 |
| 프로토콜 | MCP | Model Context Protocol |

### 지원 플랫폼

| 플랫폼 | 상태 | 형식 |
|----------|--------|--------|
| Claude Code | 지원됨 | JSONL 세션 파일 |
| Cursor IDE | 지원됨 | state.vscdb (SQLite) |
| GitHub Copilot | 예정 | -- |

### 청킹 전략

| 전략 | 최적 용도 |
|----------|----------|
| `token` (기본값) | 범용 -- 토큰 제한까지 메시지를 그룹화 |
| `turn` | 대화 중심 -- 사용자+어시스턴트 쌍으로 그룹화 |
| `recursive` | 긴 콘텐츠 -- 단락, 문장, 단어로 분할 |

## 왜 MemoTrail인가?

| | MemoTrail | CLAUDE.md / 규칙 파일 | 수동 메모 |
|---|---|---|---|
| 자동화 | 예 — 세션 시작 시마다 인덱싱 | 아니오 — 직접 작성 | 아니오 |
| 검색 가능 | 시맨틱 검색 | AI가 읽지만, 작성한 내용만 | Ctrl+F만 |
| 확장성 | 수천 개의 세션 | 단일 파일 | 흩어진 파일 |
| 컨텍스트 인식 | 관련 컨텍스트 반환 | 정적 규칙 | 수동 검색 |
| 설정 | 5분 | 지속적 유지보수 | 지속적 유지보수 |

MemoTrail은 `CLAUDE.md`를 대체하지 않습니다 — 보완합니다. 규칙 파일은 지시용, MemoTrail은 메모리용입니다.

## 로드맵

- [x] Claude Code 세션 인덱싱
- [x] 대화 간 시맨틱 검색
- [x] 7개 도구를 갖춘 MCP 서버
- [x] 인덱싱 및 검색을 위한 CLI
- [x] 서버 시작 시 자동 인덱싱
- [x] 자동 결정 추출
- [x] 세션 요약
- [x] Cursor IDE 수집기
- [x] BM25 키워드 검색 + 하이브리드 검색
- [x] 실시간 파일 감시 (watchdog)
- [x] 다중 청킹 전략 (token, turn, recursive)
- [x] VS Code 확장 프로그램
- [ ] Copilot 수집기
- [ ] 클라우드 동기화 (Pro)
- [ ] 팀 메모리 (Team)

## VS Code 확장 프로그램

MemoTrail에는 IDE에서 직접 통합할 수 있는 VS Code 확장 프로그램이 포함되어 있습니다.

**사용 가능한 명령:**
- `MemoTrail: Search Conversations` -- 시맨틱 검색
- `MemoTrail: Keyword Search` -- BM25 키워드 검색
- `MemoTrail: Recent Sessions` -- 세션 통계 보기
- `MemoTrail: Index Sessions Now` -- 수동 인덱싱 트리거
- `MemoTrail: Show Stats` -- 인덱싱 통계 표시

**설정:**
```bash
cd vscode-extension
npm install
npm run compile
# VS Code에서 F5를 눌러 확장 프로그램 개발 호스트 실행
```

## 개발

```bash
git clone https://github.com/HalilHopa-Datatent/memotrail.git
cd memotrail
pip install -e ".[dev]"
pytest
ruff check src/
```

## 기여

기여를 환영합니다! 가이드라인은 [CONTRIBUTING.md](../../docs/CONTRIBUTING.md)를 참조하세요.

## 라이선스

MIT — [LICENSE](../../LICENSE) 참조

---

<div align="center">

**[Halil Hopa](https://halilhopa.com)가 제작** · [memotrail.ai](https://memotrail.ai)

MemoTrail이 도움이 되셨다면 GitHub에서 스타를 눌러주세요.

</div>
