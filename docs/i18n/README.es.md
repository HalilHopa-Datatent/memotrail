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

## Novedades en v0.3.0

- **Resumen automatico de sesiones** -- cada sesion recibe un resumen generado por IA (no se necesitan claves API)
- **Extraccion automatica de decisiones** -- las decisiones arquitectonicas se detectan en las conversaciones mediante coincidencia de patrones
- **Busqueda por palabras clave BM25** -- nueva herramienta `search_keyword` para terminos exactos, mensajes de error, nombres de funciones
- **Busqueda hibrida** -- combina resultados semanticos + palabras clave mediante fusion de rango reciproco
- **Soporte para Cursor IDE** -- indexa el historial de chat de Cursor desde archivos `state.vscdb`
- **Vigilancia de archivos en tiempo real** -- las nuevas sesiones se indexan instantaneamente via watchdog (no requiere reinicio)
- **Estrategias de fragmentacion** -- elige entre division por tokens, por turnos o recursiva
- **Extension VS Code** -- busca, indexa y visualiza estadisticas directamente desde VS Code
- **69 tests** -- cobertura de pruebas completa en todos los modulos

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

| Paso | Que sucede |
|:----:|:-------------|
| **1. Registrar** | MemoTrail auto-indexa nuevas sesiones al iniciar + vigila nuevos archivos en tiempo real |
| **2. Dividir** | Las conversaciones se dividen usando estrategias por tokens, por turnos o recursivas |
| **3. Embeber** | Cada fragmento se embebe usando `all-MiniLM-L6-v2` (~80MB, funciona en CPU) |
| **4. Extraer** | Los resumenes y decisiones arquitectonicas se extraen automaticamente |
| **5. Almacenar** | Los vectores van a ChromaDB, los metadatos a SQLite -- todo en `~/.memotrail/` |
| **6. Buscar** | Busqueda semantica + BM25 por palabras clave en todo tu historial |
| **7. Mostrar** | El contexto pasado mas relevante aparece justo cuando lo necesitas |

> **100% local** -- sin nube, sin claves API, ningun dato sale de tu maquina.

> **Multi-plataforma** -- soporta Claude Code y Cursor IDE, mas plataformas proximamente.

## Herramientas Disponibles

Una vez conectado, Claude Code obtiene estas herramientas MCP:

| Herramienta | Descripcion |
|------|-------------|
| `search_chats` | Busqueda semantica en todas las conversaciones pasadas |
| `search_keyword` | Busqueda por palabras clave BM25 -- ideal para terminos exactos, nombres de funciones, mensajes de error |
| `get_decisions` | Recuperar decisiones de arquitectura registradas (extraidas automaticamente + manuales) |
| `get_recent_sessions` | Listar sesiones de codigo recientes con resumenes generados por IA |
| `get_session_detail` | Explorar en detalle el contenido de una sesion especifica |
| `save_memory` | Guardar manualmente hechos o decisiones importantes |
| `memory_stats` | Ver estadisticas de indexacion y uso de almacenamiento |

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

| Componente | Tecnologia | Detalles |
|-----------|-----------|---------|
| Embeddings | `all-MiniLM-L6-v2` | ~80MB, funciona en CPU |
| BD Vectorial | ChromaDB | Almacenamiento local persistente |
| Busqueda por palabras clave | BM25 | Python puro, sin dependencias adicionales |
| Metadatos | SQLite | Base de datos de archivo unico |
| Vigilancia de archivos | watchdog | Deteccion de sesiones en tiempo real |
| Protocolo | MCP | Model Context Protocol |

#### Plataformas soportadas

| Plataforma | Estado | Detalles |
|------------|--------|---------|
| Claude Code | Soportado | Archivos de sesion JSONL |
| Cursor IDE | Soportado | state.vscdb (SQLite) |
| GitHub Copilot | Planificado | -- |

#### Estrategias de fragmentacion

| Estrategia | Caso de uso |
|------------|------------|
| `token` (por defecto) | Uso general -- agrupa mensajes hasta el limite de tokens |
| `turn` | Enfocado en conversacion -- agrupa pares usuario+asistente |
| `recursive` | Contenido largo -- divide por parrafos, oraciones, palabras |

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

- [x] Indexacion de sesiones de Claude Code
- [x] Busqueda semantica entre conversaciones
- [x] Servidor MCP con 7 herramientas
- [x] CLI para indexacion y busqueda
- [x] Auto-indexacion al iniciar el servidor
- [x] Extraccion automatica de decisiones
- [x] Resumen de sesiones
- [x] Recolector de Cursor IDE
- [x] Busqueda por palabras clave BM25 + busqueda hibrida
- [x] Vigilancia de archivos en tiempo real (watchdog)
- [x] Multiples estrategias de fragmentacion (token, turn, recursive)
- [x] Extension VS Code
- [ ] Recolector de Copilot
- [ ] Sincronizacion en la nube (Pro)
- [ ] Memoria de equipo (Team)

## Extension VS Code

MemoTrail funciona directamente en VS Code. Usa los siguientes comandos desde la paleta de comandos:

- **MemoTrail: Buscar conversaciones** -- busqueda semantica en sesiones pasadas
- **MemoTrail: Busqueda por palabras clave** -- busqueda por palabras clave BM25
- **MemoTrail: Sesiones recientes** -- ver sesiones de codigo recientes
- **MemoTrail: Indexar sesiones ahora** -- indexar sesiones inmediatamente
- **MemoTrail: Mostrar estadisticas** -- ver estadisticas de indexacion

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
