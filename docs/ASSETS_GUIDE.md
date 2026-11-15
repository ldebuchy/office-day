# Guide des Assets - Office Day

Ce guide explique l'organisation des assets, les conventions, et comment ajouter de nouveaux éléments au jeu.

## 📁 Arborescence des Assets

```
assets/                     # Dossier principal des assets
├── sprites/               # Sprites des entités et objets
│   ├── player_idle.png   # Joueur au repos
│   ├── player_walk.png   # Animation de marche
│   ├── elevator_*.png    # Ascenseur (open / close / used)
│   ├── employee_*.png    # Employés (PNJ)
│   ├── boss.png, receptionist.png, npc_generic.png
│   └── desk.png, plant.png, printer.png, ... # Objets interactifs
├── backgrounds/          # Arrière-plans des étages
│   ├── floor_90.png, floor_95.png, floor_96.png
│   ├── floor_default.png
│   └── floor.jpg
├── images/
│   └── menu_background.png  # Fond du menu / pause / crédits
├── fonts/
│   └── Pixellari.ttf     # Police principale
├── sfx/                  # Effets sonores (.wav / .mp3)
└── music/                # Musiques
    └── Lobby Time.mp3    # Musique de jeu

aassets/                   # Dossier alternatif (optionnel)
└── (même structure)      # Assets de remplacement ou additionnels
```

## 🎨 Conventions Visuelles

### Dimensions Standard

- **Sprites de personnages** : 32x48 pixels
- **Tuiles de décor** : 32x32 pixels
- **Objets interactifs** : 16x16 à 48x32 pixels
- **UI panels** : Multiples de 32 pixels
- **Ascenseur** : 64x128 pixels

### Spritesheets

Les animations utilisent des spritesheets horizontales :

```
player_walk.png : [Frame1][Frame2][Frame3][Frame4]
                  32x48   32x48   32x48   32x48
```

**Paramètres dans le manifest :**
```json
"player_walk": {
  "path": "sprites/player_walk.png",
  "frame_w": 32,
  "frame_h": 48,
  "fps": 8,
  "frames": 4
}
```

### Palette de Couleurs

Le jeu utilise un style pixel art avec une palette limitée :

- **Couleurs principales** : Tons de bureau (beiges, gris, bleus)
- **Couleurs d'accent** : Rouge pour les éléments importants
- **Transparence** : Utiliser des PNG avec canal alpha

## 🔧 Formats Supportés

### Images
- **Format** : PNG (recommandé) ou JPG
- **Transparence** : PNG avec canal alpha
- **Compression** : Optimisée pour les petites tailles

### Audio
- **SFX** : WAV ou OGG (16-bit, 44.1kHz)
- **Musique** : OGG Vorbis (qualité ~128 kbps)
- **Normalisation** : ~-12 LUFS pour une expérience cohérente

### Polices
- **Format** : TTF ou OTF
- **Style** : Pixel art ou lisible à petite taille

## 📝 Manifest des Assets

Le fichier `src/data/assets_manifest.json` définit tous les assets :

```json
{
  "version": 1,
  "description": "Manifest des assets pour Office Day",
  "images": {
    "player_idle": {
      "path": "sprites/player_idle.png",
      "frame_w": 32,
      "frame_h": 48,
      "description": "Joueur au repos"
    }
  },
  "spritesheets": {
    "player_walk": {
      "path": "sprites/player_walk.png",
      "frame_w": 32,
      "frame_h": 48,
      "fps": 8,
      "frames": 4,
      "description": "Animation marche du joueur"
    }
  },
  "audio": {
    "sfx": {
      "elevator_ding": {
        "path": "sfx/ding.wav",
        "volume": 0.7,
        "description": "Son ding d'ascenseur"
      }
    }
  }
}
```

## ➕ Ajouter un Nouvel Asset

### 1. Créer le Fichier

Placez votre asset dans le dossier approprié sous `assets/`.

### 2. Ajouter au Manifest

Éditez `src/data/assets_manifest.json` :

```json
"mon_nouveau_sprite": {
  "path": "sprites/mon_sprite.png",
  "frame_w": 32,
  "frame_h": 32,
  "description": "Description de mon sprite"
}
```

### 3. Utiliser dans le Code

```python
from src.core.assets import asset_manager

# Charger l'asset
sprite = asset_manager.get_image("mon_nouveau_sprite")

# Dessiner
screen.blit(sprite, (x, y))
```

### 4. Vérifier

Exécutez l'outil de vérification :

```bash
python tools/asset_check.py
```

## 🔍 Outils de Développement

### Asset Checker

Vérifie que tous les assets du manifest existent :

```bash
# Vérification simple
python tools/asset_check.py

# Avec rapport détaillé
python tools/asset_check.py --report
```

### Hot-Reload

En mode développement, appuyez sur **F5** pour recharger les assets sans redémarrer le jeu.

## 📦 Système de Fallback

Si un asset est manquant, le système génère automatiquement un placeholder :

- **Images** : Surface damier gris avec le nom de l'asset
- **Spritesheets** : Plusieurs frames avec variations de couleur
- **Sons** : Silence ou son minimal
- **Polices** : Police système par défaut

## 🔄 Asset Discovery

Le système recherche automatiquement les assets dans cet ordre :

1. **assets/** (dossier principal)
2. **aassets/** (dossier alternatif, si présent)
3. **Placeholder** (généré automatiquement)

Cela permet d'avoir des assets de remplacement ou de test dans `aassets/` sans modifier le manifest.

## 📏 Optimisation

### Tailles Recommandées

- **Sprites** : Puissances de 2 quand possible (32, 64, 128...)
- **Backgrounds** : Adaptés à la résolution 1200x600
- **UI** : Multiples de la taille de base (16px)

### Performance

- **Grouper** les petits sprites en spritesheets
- **Optimiser** les PNG (outils comme OptiPNG)
- **Limiter** les grandes images de fond
- **Précharger** les assets critiques

## 🎵 Audio

### Effets Sonores

- **Durée** : Courts (< 2 secondes généralement)
- **Format** : WAV pour la qualité, OGG pour la taille
- **Volume** : Normalisé dans le manifest

### Musiques

- **Boucles** : Parfaites pour les ambiances
- **Format** : OGG Vorbis exclusivement
- **Taille** : Optimisée (éviter les fichiers > 5MB)

## 🐛 Dépannage

### Asset non trouvé

1. Vérifiez le chemin dans le manifest
2. Vérifiez que le fichier existe
3. Vérifiez les permissions de lecture
4. Exécutez `asset_check.py` pour un diagnostic

### Performance lente

1. Vérifiez la taille des assets
2. Activez le cache des assets
3. Optimisez les images
4. Réduisez le nombre d'assets simultanés

### Placeholder affiché

1. L'asset est manquant ou mal référencé
2. Erreur dans le manifest (syntaxe JSON)
3. Permissions de fichier incorrectes

## 📚 Ressources

- **Éditeur de sprites** : Aseprite, GIMP, Photoshop
- **Audio** : Audacity, FL Studio, Reaper
- **Optimisation PNG** : OptiPNG, TinyPNG
- **Validation JSON** : jsonlint.com

---

Pour plus d'informations, consultez le code source dans `src/core/assets.py` ou contactez l'équipe de développement.
