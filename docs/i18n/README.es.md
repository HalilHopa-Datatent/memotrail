<div align="center">

# MemoTrail

> 🌐 Esta es una traducción automática. ¡Las correcciones de la comunidad son bienvenidas! · [English](../../README.md)

[🇨🇳 中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇵🇹 Português](README.pt.md) · [🇰🇷 한국어](README.ko.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇮🇱 עברית](README.he.md) · [🇸🇦 العربية](README.ar.md) · [🇷🇺 Русский](README.ru.md) · [🇵🇱 Polski](README.pl.md) · [🇨🇿 Čeština](README.cs.md) · [🇳🇱 Nederlands](README.nl.md) · [🇹🇷 Türkçe](README.tr.md) · [🇺🇦 Українська](README.uk.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Indonesia](README.id.md) · [🇹🇭 ไทย](README.th.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇧🇩 বাংলা](README.bn.md) · [🇵🇰 اردو](README.ur.md) · [🇷🇴 Română](README.ro.md) · [🇸🇪 Svenska](README.sv.md) · [🇮🇹 Italiano](README.it.md) · [🇬🇷 Ελληνικά](README.el.md) · [🇭🇺 Magyar](README.hu.md) · [🇫🇮 Suomi](README.fi.md) · [🇩🇰 Dansk](README.da.md) · [🇳🇴 Norsk](README.no.md)

**Tu asistente de código AI lo olvida todo. MemoTrail soluciona eso.**

[![PyPI version](https://img.shields.io/pypi/v/memotrail?color=blue)](https://pypi.org/project/memotrail/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/HalilHopa-Datatent/memotrail?style=social)](https://github.com/HalilHopa-Datatent/memotrail)

Una capa de memoria persistente para asistentes de código AI.
Cada sesión registrada, cada decisión buscable, cada contexto recordado.

[Inicio Rápido](#inicio-rápido) · [Cómo Funciona](#cómo-funciona) · [Herramientas Disponibles](#herramientas-disponibles) · [Roadmap](#roadmap)

</div>

---

## El Problema

Cada nueva sesión de Claude Code empieza desde cero. Tu AI no recuerda la sesión de depuración de 3 horas de ayer, las decisiones de arquitectura de la semana pasada, ni los enfoques que ya fallaron.

**Sin MemoTrail:**
```
Tú: "Usemos Redis para el caché"
AI:  "Claro, configuremos Redis"
         ... 2 semanas después, nueva sesión ...
Tú: "¿Por qué estamos usando Redis?"
AI:  "No tengo contexto sobre esa decisión"
```

**Con MemoTrail:**
```
Tú: "¿Por qué estamos usando Redis?"
AI:  "Basado en la sesión del 15 de enero — evaluaste Redis vs Memcached.
      Se eligió Redis por su soporte de estructuras de datos y persistencia.
      La discusión está en la sesión #42."
```

## Inicio Rápido

```bash
# 1. Instalar
pip install memotrail

# 2. Conectar a Claude Code
claude mcp add memotrail -- memotrail serve
```

Eso es todo. MemoTrail indexa automáticamente tu historial en el primer inicio.
Comienza una nueva sesión y pregunta: *"¿En qué trabajamos la semana pasada?"*

## Cómo Funciona

| Paso | Qué sucede |
|:----:|:-------------|
| **1. Registrar** | MemoTrail auto-indexa nuevas sesiones cada vez que el servidor inicia |
| **2. Dividir** | Las conversaciones se dividen en segmentos significativos |
| **3. Embeber** | Cada fragmento se embebe usando `all-MiniLM-L6-v2` (~80MB, funciona en CPU) |
| **4. Almacenar** | Los vectores van a ChromaDB, los metadatos a SQLite — todo en `~/.memotrail/` |
| **5. Buscar** | En la siguiente sesión, Claude consulta todo tu historial semánticamente |
| **6. Mostrar** | El contexto pasado más relevante aparece justo cuando lo necesitas |

> **100% local** — sin nube, sin claves API, ningún dato sale de tu máquina.

## Herramientas Disponibles

Una vez conectado, Claude Code obtiene estas herramientas MCP:

| Herramienta | Descripción |
|------|-------------|
| `search_chats` | Búsqueda semántica en todas las conversaciones pasadas |
| `get_decisions` | Recuperar decisiones de arquitectura registradas |
| `get_recent_sessions` | Listar sesiones de código recientes con resúmenes |
| `get_session_detail` | Explorar en detalle el contenido de una sesión específica |
| `save_memory` | Guardar manualmente hechos o decisiones importantes |
| `memory_stats` | Ver estadísticas de indexación y uso de almacenamiento |

## Comandos CLI

```bash
memotrail serve                          # Iniciar servidor MCP (auto-indexa nuevas sesiones)
memotrail search "redis caching decision"  # Buscar desde terminal
memotrail stats                          # Ver estadísticas de indexación
memotrail index                          # Re-indexar manualmente (opcional)
```

## Arquitectura

```
~/.memotrail/
├── chroma/          # Embeddings vectoriales (ChromaDB)
└── memotrail.db     # Metadatos de sesión (SQLite)
```

| Componente | Tecnología | Detalles |
|-----------|-----------|---------|
| Embeddings | `all-MiniLM-L6-v2` | ~80MB, funciona en CPU |
| BD Vectorial | ChromaDB | Almacenamiento local persistente |
| Metadatos | SQLite | Base de datos de archivo único |
| Protocolo | MCP | Model Context Protocol |

## ¿Por qué MemoTrail?

| | MemoTrail | CLAUDE.md / Archivos de reglas | Notas manuales |
|---|---|---|---|
| Automático | Sí — indexa en cada inicio de sesión | No — tú lo escribes | No |
| Buscable | Búsqueda semántica | La AI lo lee, pero solo lo que escribiste | Solo Ctrl+F |
| Escalable | Miles de sesiones | Archivo único | Archivos dispersos |
| Contextual | Devuelve contexto relevante | Reglas estáticas | Búsqueda manual |
| Configuración | 5 minutos | Mantenimiento constante | Mantenimiento constante |

MemoTrail no reemplaza `CLAUDE.md` — lo complementa. Los archivos de reglas son para instrucciones. MemoTrail es para la memoria.

## Roadmap

- [x] Indexación de sesiones de Claude Code
- [x] Búsqueda semántica entre conversaciones
- [x] Servidor MCP con 6 herramientas
- [x] CLI para indexación y búsqueda
- [x] Auto-indexación al iniciar el servidor
- [ ] Extracción automática de decisiones
- [ ] Resumen de sesiones
- [ ] Recolector de Cursor
- [ ] Recolector de Copilot
- [ ] Extensión VS Code
- [ ] Sincronización en la nube (Pro)
- [ ] Memoria de equipo (Team)

## Desarrollo

```bash
git clone https://github.com/HalilHopa-Datatent/memotrail.git
cd memotrail
pip install -e ".[dev]"
pytest
ruff check src/
```

## Contribuir

¡Las contribuciones son bienvenidas! Consulta [CONTRIBUTING.md](../../docs/CONTRIBUTING.md) para las directrices.

## Licencia

MIT — ver [LICENSE](../../LICENSE)

---

<div align="center">

**Creado por [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

Si MemoTrail te ayuda, considera darle una estrella en GitHub.

</div>
