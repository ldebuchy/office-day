"""
Point d'entrée principal pour A Day at the Office.
"""

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from src.core.app import Game  # noqa: E402  (logging doit être configuré avant)

logger = logging.getLogger(__name__)


def main():
    """Point d'entrée principal du jeu."""
    logger.info("Starting A Day at the Office")
    Game().run()


if __name__ == "__main__":
    main()
