# A Day at the Office

Jeu en Python / Pygame réalisé pour une game jam.

## Installation

Prérequis : Python 3.12 (pygame 2.6.1 ne supporte pas encore les versions plus récentes que 3.13).

Avec [uv](https://docs.astral.sh/uv/) :

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv -r requirements.txt
```

Ou avec pip :

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
```

## Lancer le jeu

```bash
.venv\Scripts\python main.py      # Windows
.venv/bin/python main.py          # macOS / Linux
```

## Tests

```bash
.venv\Scripts\python -m pytest
```

## Structure

```
main.py          Point d'entrée
src/
  core/          Moteur : boucle de jeu, scènes, assets, audio, input, caméra
  scenes/        Écrans : avertissement, menu, gameplay, pause, résumé
  world/         Bâtiment, ascenseur, PNJ, tâches, déclencheurs
  ui/            HUD, dialogues, bulles, widgets
  data/          Contenu en JSON (étages, tâches, dialogues, textes, manifest des assets)
assets/          Images, sons, musiques, police
tools/           Scripts utilitaires (vérification des assets, upscale pixel art…)
tests/           Tests pytest
docs/            Guides sur les assets et les sprites
```

Les assets sont déclarés dans [src/data/assets_manifest.json](src/data/assets_manifest.json) ; voir [docs/ASSETS_GUIDE.md](docs/ASSETS_GUIDE.md).
