<div align="center">

# MemoTrail

> 🌐 Esta é uma tradução automática. Correções da comunidade são bem-vindas! · [English](../../README.md)

[🇨🇳 中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇵🇹 Português](README.pt.md) · [🇰🇷 한국어](README.ko.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇮🇱 עברית](README.he.md) · [🇸🇦 العربية](README.ar.md) · [🇷🇺 Русский](README.ru.md) · [🇵🇱 Polski](README.pl.md) · [🇨🇿 Čeština](README.cs.md) · [🇳🇱 Nederlands](README.nl.md) · [🇹🇷 Türkçe](README.tr.md) · [🇺🇦 Українська](README.uk.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Indonesia](README.id.md) · [🇹🇭 ไทย](README.th.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇧🇩 বাংলা](README.bn.md) · [🇵🇰 اردو](README.ur.md) · [🇷🇴 Română](README.ro.md) · [🇸🇪 Svenska](README.sv.md) · [🇮🇹 Italiano](README.it.md) · [🇬🇷 Ελληνικά](README.el.md) · [🇭🇺 Magyar](README.hu.md) · [🇫🇮 Suomi](README.fi.md) · [🇩🇰 Dansk](README.da.md) · [🇳🇴 Norsk](README.no.md)

**Seu assistente de código AI esquece tudo. MemoTrail resolve isso.**

[![PyPI version](https://img.shields.io/pypi/v/memotrail?color=blue)](https://pypi.org/project/memotrail/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/HalilHopa-Datatent/memotrail?style=social)](https://github.com/HalilHopa-Datatent/memotrail)

Uma camada de memória persistente para assistentes de código AI.
Cada sessão registrada, cada decisão pesquisável, cada contexto lembrado.

[Início Rápido](#início-rápido) · [Como Funciona](#como-funciona) · [Ferramentas Disponíveis](#ferramentas-disponíveis) · [Roadmap](#roadmap)

</div>

---

## O Problema

Cada nova sessão do Claude Code começa do zero. Sua AI não lembra da sessão de debugging de 3 horas de ontem, das decisões de arquitetura da semana passada, ou das abordagens que já falharam.

**Sem MemoTrail:**
```
Você: "Vamos usar Redis para cache"
AI:   "Claro, vamos configurar o Redis"
         ... 2 semanas depois, nova sessão ...
Você: "Por que estamos usando Redis?"
AI:   "Não tenho contexto sobre essa decisão"
```

**Com MemoTrail:**
```
Você: "Por que estamos usando Redis?"
AI:   "Com base na sessão de 15 de janeiro — você avaliou Redis vs Memcached.
      Redis foi escolhido pelo suporte a estruturas de dados e persistência.
      A discussão está na sessão #42."
```

## Início Rápido

```bash
# 1. Instalar
pip install memotrail

# 2. Conectar ao Claude Code
claude mcp add memotrail -- memotrail serve
```

É isso. MemoTrail indexa automaticamente seu histórico na primeira execução.
Inicie uma nova sessão e pergunte: *"O que trabalhamos na semana passada?"*

## Como Funciona

| Etapa | O que acontece |
|:----:|:-------------|
| **1. Registrar** | MemoTrail auto-indexa novas sessões toda vez que o servidor inicia |
| **2. Dividir** | Conversas são divididas em segmentos significativos |
| **3. Incorporar** | Cada trecho é incorporado usando `all-MiniLM-L6-v2` (~80MB, roda na CPU) |
| **4. Armazenar** | Vetores vão para ChromaDB, metadados para SQLite — tudo em `~/.memotrail/` |
| **5. Buscar** | Na próxima sessão, Claude consulta todo seu histórico semanticamente |
| **6. Exibir** | O contexto passado mais relevante aparece quando você precisa |

> **100% local** — sem nuvem, sem chaves de API, nenhum dado sai da sua máquina.

## Ferramentas Disponíveis

Uma vez conectado, Claude Code recebe estas ferramentas MCP:

| Ferramenta | Descrição |
|------|-------------|
| `search_chats` | Busca semântica em todas as conversas passadas |
| `get_decisions` | Recuperar decisões de arquitetura registradas |
| `get_recent_sessions` | Listar sessões recentes com resumos |
| `get_session_detail` | Explorar em detalhes o conteúdo de uma sessão específica |
| `save_memory` | Salvar manualmente fatos ou decisões importantes |
| `memory_stats` | Ver estatísticas de indexação e uso de armazenamento |

## Comandos CLI

```bash
memotrail serve                          # Iniciar servidor MCP (auto-indexa novas sessões)
memotrail search "redis caching decision"  # Buscar pelo terminal
memotrail stats                          # Ver estatísticas de indexação
memotrail index                          # Re-indexar manualmente (opcional)
```

## Arquitetura

```
~/.memotrail/
├── chroma/          # Embeddings vetoriais (ChromaDB)
└── memotrail.db     # Metadados de sessão (SQLite)
```

| Componente | Tecnologia | Detalhes |
|-----------|-----------|---------|
| Embeddings | `all-MiniLM-L6-v2` | ~80MB, roda na CPU |
| Banco Vetorial | ChromaDB | Armazenamento local persistente |
| Metadados | SQLite | Banco de dados em arquivo único |
| Protocolo | MCP | Model Context Protocol |

## Por que MemoTrail?

| | MemoTrail | CLAUDE.md / Arquivos de regras | Notas manuais |
|---|---|---|---|
| Automático | Sim — indexa a cada início de sessão | Não — você escreve | Não |
| Pesquisável | Busca semântica | AI lê, mas só o que você escreveu | Apenas Ctrl+F |
| Escalável | Milhares de sessões | Arquivo único | Arquivos espalhados |
| Contextual | Retorna contexto relevante | Regras estáticas | Busca manual |
| Configuração | 5 minutos | Manutenção constante | Manutenção constante |

MemoTrail não substitui o `CLAUDE.md` — ele o complementa. Arquivos de regras são para instruções. MemoTrail é para memória.

## Roadmap

- [x] Indexação de sessões do Claude Code
- [x] Busca semântica entre conversas
- [x] Servidor MCP com 6 ferramentas
- [x] CLI para indexação e busca
- [x] Auto-indexação na inicialização do servidor
- [ ] Extração automática de decisões
- [ ] Resumo de sessões
- [ ] Coletor Cursor
- [ ] Coletor Copilot
- [ ] Extensão VS Code
- [ ] Sincronização na nuvem (Pro)
- [ ] Memória de equipe (Team)

## Desenvolvimento

```bash
git clone https://github.com/HalilHopa-Datatent/memotrail.git
cd memotrail
pip install -e ".[dev]"
pytest
ruff check src/
```

## Contribuindo

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](../../docs/CONTRIBUTING.md) para diretrizes.

## Licença

MIT — veja [LICENSE](../../LICENSE)

---

<div align="center">

**Criado por [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

Se MemoTrail te ajuda, considere dar uma estrela no GitHub.

</div>
