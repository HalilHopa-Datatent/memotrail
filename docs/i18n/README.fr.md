<div align="center">

# MemoTrail

> 🌐 Ceci est une traduction automatique. Les corrections de la communauté sont les bienvenues ! · [English](../../README.md)

[🇨🇳 中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇵🇹 Português](README.pt.md) · [🇰🇷 한국어](README.ko.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇮🇱 עברית](README.he.md) · [🇸🇦 العربية](README.ar.md) · [🇷🇺 Русский](README.ru.md) · [🇵🇱 Polski](README.pl.md) · [🇨🇿 Čeština](README.cs.md) · [🇳🇱 Nederlands](README.nl.md) · [🇹🇷 Türkçe](README.tr.md) · [🇺🇦 Українська](README.uk.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Indonesia](README.id.md) · [🇹🇭 ไทย](README.th.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇧🇩 বাংলা](README.bn.md) · [🇵🇰 اردو](README.ur.md) · [🇷🇴 Română](README.ro.md) · [🇸🇪 Svenska](README.sv.md) · [🇮🇹 Italiano](README.it.md) · [🇬🇷 Ελληνικά](README.el.md) · [🇭🇺 Magyar](README.hu.md) · [🇫🇮 Suomi](README.fi.md) · [🇩🇰 Dansk](README.da.md) · [🇳🇴 Norsk](README.no.md)

**Votre assistant de code AI oublie tout. MemoTrail résout ce problème.**

[![PyPI version](https://img.shields.io/pypi/v/memotrail?color=blue)](https://pypi.org/project/memotrail/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/HalilHopa-Datatent/memotrail?style=social)](https://github.com/HalilHopa-Datatent/memotrail)

Une couche de mémoire persistante pour les assistants de code AI.
Chaque session enregistrée, chaque décision recherchable, chaque contexte mémorisé.

[Démarrage Rapide](#démarrage-rapide) · [Comment ça Marche](#comment-ça-marche) · [Outils Disponibles](#outils-disponibles) · [Roadmap](#roadmap)

</div>

---

## Le Problème

Chaque nouvelle session Claude Code commence à zéro. Votre AI ne se souvient pas de la session de débogage de 3 heures d'hier, des décisions d'architecture de la semaine dernière, ni des approches qui ont déjà échoué.

**Sans MemoTrail :**
```
Vous : "Utilisons Redis pour le cache"
AI :   "Bien sûr, configurons Redis"
         ... 2 semaines plus tard, nouvelle session ...
Vous : "Pourquoi utilisons-nous Redis ?"
AI :   "Je n'ai pas de contexte sur cette décision"
```

**Avec MemoTrail :**
```
Vous : "Pourquoi utilisons-nous Redis ?"
AI :   "D'après la session du 15 janvier — vous avez évalué Redis vs Memcached.
        Redis a été choisi pour son support des structures de données et sa persistance.
        La discussion se trouve dans la session #42."
```

## Démarrage Rapide

```bash
# 1. Installer
pip install memotrail

# 2. Connecter à Claude Code
claude mcp add memotrail -- memotrail serve
```

C'est tout. MemoTrail indexe automatiquement votre historique au premier lancement.
Démarrez une nouvelle session et demandez : *"Sur quoi avons-nous travaillé la semaine dernière ?"*

## Comment ça Marche

| Étape | Ce qui se passe |
|:----:|:-------------|
| **1. Enregistrer** | MemoTrail indexe automatiquement les nouvelles sessions à chaque démarrage du serveur |
| **2. Découper** | Les conversations sont découpées en segments significatifs |
| **3. Incorporer** | Chaque segment est incorporé avec `all-MiniLM-L6-v2` (~80Mo, tourne sur CPU) |
| **4. Stocker** | Les vecteurs vont dans ChromaDB, les métadonnées dans SQLite — tout sous `~/.memotrail/` |
| **5. Chercher** | À la session suivante, Claude interroge tout votre historique sémantiquement |
| **6. Afficher** | Le contexte passé le plus pertinent apparaît quand vous en avez besoin |

> **100% local** — pas de cloud, pas de clés API, aucune donnée ne quitte votre machine.

## Outils Disponibles

Une fois connecté, Claude Code obtient ces outils MCP :

| Outil | Description |
|------|-------------|
| `search_chats` | Recherche sémantique dans toutes les conversations passées |
| `get_decisions` | Récupérer les décisions d'architecture enregistrées |
| `get_recent_sessions` | Lister les sessions récentes avec des résumés |
| `get_session_detail` | Explorer en détail le contenu d'une session spécifique |
| `save_memory` | Sauvegarder manuellement des faits ou décisions importants |
| `memory_stats` | Voir les statistiques d'indexation et l'utilisation du stockage |

## Commandes CLI

```bash
memotrail serve                          # Démarrer le serveur MCP (indexe automatiquement les nouvelles sessions)
memotrail search "redis caching decision"  # Chercher depuis le terminal
memotrail stats                          # Voir les statistiques d'indexation
memotrail index                          # Ré-indexer manuellement (optionnel)
```

## Architecture

```
~/.memotrail/
├── chroma/          # Embeddings vectoriels (ChromaDB)
└── memotrail.db     # Métadonnées de session (SQLite)
```

| Composant | Technologie | Détails |
|-----------|-----------|---------|
| Embeddings | `all-MiniLM-L6-v2` | ~80Mo, tourne sur CPU |
| BD Vectorielle | ChromaDB | Stockage local persistant |
| Métadonnées | SQLite | Base de données mono-fichier |
| Protocole | MCP | Model Context Protocol |

## Pourquoi MemoTrail ?

| | MemoTrail | CLAUDE.md / Fichiers de règles | Notes manuelles |
|---|---|---|---|
| Automatique | Oui — indexe à chaque démarrage de session | Non — vous l'écrivez | Non |
| Recherchable | Recherche sémantique | L'AI le lit, mais seulement ce que vous avez écrit | Seulement Ctrl+F |
| Évolutif | Des milliers de sessions | Fichier unique | Fichiers dispersés |
| Contextuel | Renvoie le contexte pertinent | Règles statiques | Recherche manuelle |
| Configuration | 5 minutes | Maintenance constante | Maintenance constante |

MemoTrail ne remplace pas `CLAUDE.md` — il le complète. Les fichiers de règles sont pour les instructions. MemoTrail est pour la mémoire.

## Roadmap

- [x] Indexation des sessions Claude Code
- [x] Recherche sémantique entre les conversations
- [x] Serveur MCP avec 6 outils
- [x] CLI pour l'indexation et la recherche
- [x] Auto-indexation au démarrage du serveur
- [ ] Extraction automatique des décisions
- [ ] Résumé de sessions
- [ ] Collecteur Cursor
- [ ] Collecteur Copilot
- [ ] Extension VS Code
- [ ] Synchronisation cloud (Pro)
- [ ] Mémoire d'équipe (Team)

## Développement

```bash
git clone https://github.com/HalilHopa-Datatent/memotrail.git
cd memotrail
pip install -e ".[dev]"
pytest
ruff check src/
```

## Contribuer

Les contributions sont les bienvenues ! Voir [CONTRIBUTING.md](../../docs/CONTRIBUTING.md) pour les directives.

## Licence

MIT — voir [LICENSE](../../LICENSE)

---

<div align="center">

**Créé par [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

Si MemoTrail vous aide, pensez à lui donner une étoile sur GitHub.

</div>
