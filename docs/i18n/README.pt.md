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

## Novidades na v0.3.0

- **Resumo automatico de sessoes** -- cada sessao recebe um resumo gerado por IA (sem necessidade de chaves API)
- **Extracao automatica de decisoes** -- decisoes arquiteturais sao detectadas nas conversas usando correspondencia de padroes
- **Busca por palavras-chave BM25** -- nova ferramenta `search_keyword` para termos exatos, mensagens de erro, nomes de funcoes
- **Busca hibrida** -- combina resultados semanticos + palavras-chave usando fusao de classificacao reciproca
- **Suporte ao Cursor IDE** -- indexa o historico de chat do Cursor a partir de arquivos `state.vscdb`
- **Monitoramento de arquivos em tempo real** -- novas sessoes sao indexadas instantaneamente via watchdog (sem necessidade de reiniciar)
- **Estrategias de fragmentacao** -- escolha entre divisao por tokens, por turnos ou recursiva
- **Extensao VS Code** -- busca, indexacao e estatisticas diretamente no VS Code
- **69 testes** -- cobertura de testes abrangente em todos os modulos

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
| **1. Registrar** | MemoTrail auto-indexa novas sessoes na inicializacao + monitora novos arquivos em tempo real |
| **2. Dividir** | Conversas sao divididas usando estrategias por tokens, por turnos ou recursivas |
| **3. Incorporar** | Cada trecho e incorporado usando `all-MiniLM-L6-v2` (~80MB, roda na CPU) |
| **4. Extrair** | Resumos e decisoes arquiteturais sao extraidos automaticamente |
| **5. Armazenar** | Vetores vao para ChromaDB, metadados para SQLite -- tudo em `~/.memotrail/` |
| **6. Buscar** | Busca semantica + BM25 por palavras-chave em todo seu historico |
| **7. Exibir** | O contexto passado mais relevante aparece quando voce precisa |

> **100% local** -- sem nuvem, sem chaves de API, nenhum dado sai da sua maquina.

> **Multi-plataforma** -- suporta Claude Code e Cursor IDE, mais plataformas em breve.

## Ferramentas Disponíveis

Uma vez conectado, Claude Code recebe estas ferramentas MCP:

| Ferramenta | Descricao |
|------|-------------|
| `search_chats` | Busca semantica em todas as conversas passadas |
| `search_keyword` | Busca por palavras-chave BM25 -- ideal para termos exatos, nomes de funcoes, mensagens de erro |
| `get_decisions` | Recuperar decisoes de arquitetura registradas (extraidas automaticamente + manuais) |
| `get_recent_sessions` | Listar sessoes recentes com resumos gerados por IA |
| `get_session_detail` | Explorar em detalhes o conteudo de uma sessao especifica |
| `save_memory` | Salvar manualmente fatos ou decisoes importantes |
| `memory_stats` | Ver estatisticas de indexacao e uso de armazenamento |

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
| Busca por palavras-chave | BM25 | Python puro, sem dependencias adicionais |
| Metadados | SQLite | Banco de dados em arquivo unico |
| Monitoramento de arquivos | watchdog | Deteccao de sessoes em tempo real |
| Protocolo | MCP | Model Context Protocol |

#### Plataformas suportadas

| Plataforma | Status | Detalhes |
|------------|--------|---------|
| Claude Code | Suportado | Arquivos de sessao JSONL |
| Cursor IDE | Suportado | state.vscdb (SQLite) |
| GitHub Copilot | Planejado | -- |

#### Estrategias de fragmentacao

| Estrategia | Caso de uso |
|------------|------------|
| `token` (padrao) | Uso geral -- agrupa mensagens ate o limite de tokens |
| `turn` | Focado em conversacao -- agrupa pares usuario+assistente |
| `recursive` | Conteudo longo -- divide por paragrafos, frases, palavras |

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

- [x] Indexacao de sessoes do Claude Code
- [x] Busca semantica entre conversas
- [x] Servidor MCP com 7 ferramentas
- [x] CLI para indexacao e busca
- [x] Auto-indexacao na inicializacao do servidor
- [x] Extracao automatica de decisoes
- [x] Resumo de sessoes
- [x] Coletor Cursor IDE
- [x] Busca por palavras-chave BM25 + busca hibrida
- [x] Monitoramento de arquivos em tempo real (watchdog)
- [x] Multiplas estrategias de fragmentacao (token, turn, recursive)
- [x] Extensao VS Code
- [ ] Coletor Copilot
- [ ] Sincronizacao na nuvem (Pro)
- [ ] Memoria de equipe (Team)

## Extensao VS Code

MemoTrail funciona diretamente no VS Code. Use os seguintes comandos na paleta de comandos:

- **MemoTrail: Buscar conversas** -- busca semantica em sessoes passadas
- **MemoTrail: Busca por palavras-chave** -- busca por palavras-chave BM25
- **MemoTrail: Sessoes recentes** -- ver sessoes de codificacao recentes
- **MemoTrail: Indexar sessoes agora** -- indexar sessoes imediatamente
- **MemoTrail: Mostrar estatisticas** -- ver estatisticas de indexacao

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
