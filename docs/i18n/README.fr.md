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

## Nouveautes de la v0.3.0

- **Resume automatique des sessions** -- chaque session recoit un resume genere par l'IA (aucune cle API necessaire)
- **Extraction automatique des decisions** -- les decisions architecturales sont detectees dans les conversations par correspondance de motifs
- **Recherche par mots-cles BM25** -- nouvel outil `search_keyword` pour les termes exacts, messages d'erreur, noms de fonctions
- **Recherche hybride** -- combine les resultats semantiques + mots-cles via la fusion de rangs reciproques
- **Support Cursor IDE** -- indexe l'historique des chats Cursor depuis les fichiers `state.vscdb`
- **Surveillance de fichiers en temps reel** -- les nouvelles sessions sont indexees instantanement via watchdog (pas de redemarrage necessaire)
- **Strategies de decoupage** -- choix entre decoupage par tokens, par tours ou recursif
- **Extension VS Code** -- recherche, indexation et statistiques directement depuis VS Code
- **69 tests** -- couverture de tests complete sur tous les modules

---

## Le Probleme

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


<div align="center">
<img src="../../demo.gif" alt="MemoTrail Demo" width="800">
<br>
<sub>Install → Connect → See stats → Search past sessions → Save memory → Duplicate &amp; contradiction detection</sub>
</div>

## Comment ça Marche

| Etape | Ce qui se passe |
|:----:|:-------------|
| **1. Enregistrer** | MemoTrail indexe automatiquement les nouvelles sessions au demarrage + surveille les nouveaux fichiers en temps reel |
| **2. Decouper** | Les conversations sont decoupees avec des strategies par tokens, par tours ou recursives |
| **3. Incorporer** | Chaque segment est incorpore avec `all-MiniLM-L6-v2` (~80Mo, tourne sur CPU) |
| **4. Extraire** | Les resumes et decisions architecturales sont automatiquement extraits |
| **5. Stocker** | Les vecteurs vont dans ChromaDB, les metadonnees dans SQLite -- tout sous `~/.memotrail/` |
| **6. Chercher** | Recherche semantique + BM25 par mots-cles sur tout votre historique |
| **7. Afficher** | Le contexte passe le plus pertinent apparait quand vous en avez besoin |

> **100% local** -- pas de cloud, pas de cles API, aucune donnee ne quitte votre machine.

> **Multi-plateforme** -- supporte Claude Code et Cursor IDE, d'autres arrivent bientot.

## Outils Disponibles

Une fois connecté, Claude Code obtient ces outils MCP :

| Outil | Description |
|------|-------------|
| `search_chats` | Recherche semantique dans toutes les conversations passees |
| `search_keyword` | Recherche par mots-cles BM25 -- ideal pour les termes exacts, noms de fonctions, messages d'erreur |
| `get_decisions` | Recuperer les decisions d'architecture enregistrees (extraites automatiquement + manuelles) |
| `get_recent_sessions` | Lister les sessions recentes avec des resumes generes par l'IA |
| `get_session_detail` | Explorer en detail le contenu d'une session specifique |
| `save_memory` | Sauvegarder manuellement des faits ou decisions importants |
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

| Composant | Technologie | Details |
|-----------|-----------|---------|
| Embeddings | `all-MiniLM-L6-v2` | ~80Mo, tourne sur CPU |
| BD Vectorielle | ChromaDB | Stockage local persistant |
| Recherche par mots-cles | BM25 | Python pur, aucune dependance supplementaire |
| Metadonnees | SQLite | Base de donnees mono-fichier |
| Surveillance de fichiers | watchdog | Detection de sessions en temps reel |
| Protocole | MCP | Model Context Protocol |

#### Plateformes supportees

| Plateforme | Statut | Details |
|------------|--------|---------|
| Claude Code | Supporte | Fichiers de session JSONL |
| Cursor IDE | Supporte | state.vscdb (SQLite) |
| GitHub Copilot | Prevu | -- |

#### Strategies de decoupage

| Strategie | Cas d'utilisation |
|-----------|------------------|
| `token` (par defaut) | Usage general -- regroupe les messages jusqu'a la limite de tokens |
| `turn` | Axe conversation -- regroupe les paires utilisateur+assistant |
| `recursive` | Contenu long -- decoupe par paragraphes, phrases, mots |

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
- [x] Recherche semantique entre les conversations
- [x] Serveur MCP avec 7 outils
- [x] CLI pour l'indexation et la recherche
- [x] Auto-indexation au demarrage du serveur
- [x] Extraction automatique des decisions
- [x] Resume de sessions
- [x] Collecteur Cursor IDE
- [x] Recherche par mots-cles BM25 + recherche hybride
- [x] Surveillance de fichiers en temps reel (watchdog)
- [x] Strategies de decoupage multiples (token, turn, recursive)
- [x] Extension VS Code
- [ ] Collecteur Copilot
- [ ] Synchronisation cloud (Pro)
- [ ] Memoire d'equipe (Team)

## Extension VS Code

MemoTrail fonctionne directement dans VS Code. Utilisez les commandes suivantes depuis la palette de commandes :

- **MemoTrail: Rechercher des conversations** -- recherche semantique dans les sessions passees
- **MemoTrail: Recherche par mots-cles** -- recherche par mots-cles BM25
- **MemoTrail: Sessions recentes** -- voir les sessions de codage recentes
- **MemoTrail: Indexer les sessions maintenant** -- indexer les sessions immediatement
- **MemoTrail: Afficher les statistiques** -- voir les statistiques d'indexation

## Developpement

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
