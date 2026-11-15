#!/usr/bin/env python3
"""
Outil de test pour le placement et dimensionnement des sprites.
Permet de visualiser rapidement les changements sans relancer le jeu complet.
"""

import sys
from pathlib import Path

# Ajouter le dossier racine au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pygame
import json
from src.core.assets import asset_manager
from src.settings import WIDTH, HEIGHT

def load_test_data():
    """Charge les données de test depuis les fichiers JSON."""
    try:
        # Charger le manifest
        manifest_path = Path("src/data/assets_manifest.json")
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        # Charger les étages
        floors_path = Path("src/data/floors.json")
        with open(floors_path, 'r', encoding='utf-8') as f:
            floors = json.load(f)
        
        return manifest, floors
    except Exception as e:
        print(f"Erreur chargement données: {e}")
        return None, None

def draw_test_floor(screen, floor_data, floor_num, y_pos):
    """Dessine un étage de test avec ses objets."""
    floor_height = HEIGHT // 3
    world_width = WIDTH - 150
    world_x = 120
    
    # Fond d'étage
    floor_rect = pygame.Rect(world_x, y_pos, world_width, floor_height - 10)
    color = (240, 240, 240)
    pygame.draw.rect(screen, color, floor_rect)
    pygame.draw.rect(screen, (100, 100, 100), floor_rect, 2)
    
    # Titre de l'étage
    font = pygame.font.SysFont(None, 24)
    title = f"Étage {floor_num} - {floor_data.get('name', 'Test')}"
    text_surface = font.render(title, True, (0, 0, 0))
    screen.blit(text_surface, (10, y_pos + 10))
    
    # Ascenseur
    elevator_rect = pygame.Rect(30, y_pos + 5, 80, floor_height - 20)
    pygame.draw.rect(screen, (150, 150, 150), elevator_rect)
    pygame.draw.rect(screen, (100, 100, 100), elevator_rect, 2)
    
    # Objets
    objects = floor_data.get('objects', [])
    for obj_data in objects:
        kind = obj_data.get('kind', 'unknown')
        obj_x = obj_data.get('x', 0)
        
        # Position à l'écran
        screen_x = world_x + obj_x
        screen_y = y_pos + floor_height - 40  # Au sol
        
        # Couleur selon le type
        colors = {
            'npc': (255, 100, 100),      # Rouge
            'plant': (100, 255, 100),    # Vert
            'papers': (255, 255, 100),   # Jaune
            'printer': (100, 100, 255),  # Bleu
            'decoration': (200, 100, 200) # Violet
        }
        color = colors.get(kind, (128, 128, 128))
        
        # Taille selon le type
        sizes = {
            'npc': (32, 48),
            'plant': (24, 32),
            'papers': (16, 16),
            'printer': (48, 32),
            'decoration': (20, 20)
        }
        width, height = sizes.get(kind, (20, 20))
        
        # Dessiner l'objet
        obj_rect = pygame.Rect(screen_x - width//2, screen_y - height, width, height)
        pygame.draw.rect(screen, color, obj_rect)
        pygame.draw.rect(screen, (0, 0, 0), obj_rect, 1)
        
        # ID de l'objet
        id_text = obj_data.get('id', 'unknown')
        small_font = pygame.font.SysFont(None, 16)
        id_surface = small_font.render(id_text, True, (0, 0, 0))
        screen.blit(id_surface, (screen_x - id_surface.get_width()//2, screen_y + 5))

def main():
    """Fonction principale du testeur de sprites."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sprite Tester - Office Day")
    clock = pygame.time.Clock()
    
    print("🎨 Sprite Tester - Office Day")
    print("=====================================")
    print("Contrôles :")
    print("  F5 : Recharger les données")
    print("  ESC : Quitter")
    print("  Clic : Afficher coordonnées")
    print()
    
    # Charger les données
    manifest, floors_data = load_test_data()
    if not manifest or not floors_data:
        print("❌ Impossible de charger les données")
        return
    
    # Charger l'asset manager
    asset_manager.load_manifest()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_F5:
                    print("🔄 Rechargement des données...")
                    manifest, floors_data = load_test_data()
                    asset_manager.reload_manifest()
                    print("✅ Données rechargées")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Convertir en coordonnées de jeu
                    world_x = 120
                    if mouse_x >= world_x:
                        game_x = mouse_x - world_x
                        floor_index = mouse_y // (HEIGHT // 3)
                        print(f"📍 Clic : X={game_x}, Étage={floor_index}, Écran=({mouse_x}, {mouse_y})")
        
        # Fond
        screen.fill((100, 150, 200))
        
        # Dessiner les étages de test
        if floors_data:
            floors = floors_data.get('floors', {})
            floor_numbers = sorted([int(k) for k in floors.keys()])
            
            # Afficher 3 étages (les 3 premiers pour le test)
            test_floors = floor_numbers[:3]
            
            for i, floor_num in enumerate(reversed(test_floors)):
                floor_data = floors[str(floor_num)]
                y_pos = i * (HEIGHT // 3)
                draw_test_floor(screen, floor_data, floor_num, y_pos)
        
        # Instructions
        font = pygame.font.SysFont(None, 20)
        instructions = [
            "F5: Recharger | ESC: Quitter | Clic: Coordonnées",
            f"Zone de jeu: X=0 à X=1050 (écran X=120 à X=1170)",
            "Modifiez floors.json puis F5 pour voir les changements"
        ]
        
        for i, instruction in enumerate(instructions):
            text_surface = font.render(instruction, True, (255, 255, 255))
            screen.blit(text_surface, (10, HEIGHT - 60 + i * 20))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("👋 Sprite Tester fermé")

if __name__ == "__main__":
    main()
