"""
Registro de eventos y errores en archivo de logs (sin base de datos).
"""

from __future__ import annotations

import logging
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_FILE = LOG_DIR / "sistema_fj.log"


def configurar_logger(nombre: str = "software_fj") -> logging.Logger:
    """Configura un logger que escribe en consola y en archivo."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(nombre)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    archivo = logging.FileHandler(LOG_FILE, encoding="utf-8")
    archivo.setLevel(logging.DEBUG)
    archivo.setFormatter(formato)

    consola = logging.StreamHandler()
    consola.setLevel(logging.INFO)
    consola.setFormatter(formato)

    logger.addHandler(archivo)
    logger.addHandler(consola)
    return logger


logger = configurar_logger()
