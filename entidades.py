"""
Clases abstractas y entidades base del sistema Software FJ.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime


class Entidad(ABC):
    """Clase abstracta que representa entidades generales del sistema."""

    def __init__(self, identificador: str) -> None:
        if not identificador or not str(identificador).strip():
            raise ValueError("El identificador de la entidad es obligatorio.")
        self._id = str(identificador).strip()
        self._creado_en = datetime.now()

    @property
    def id(self) -> str:
        return self._id

    @property
    def creado_en(self) -> datetime:
        return self._creado_en

    @abstractmethod
    def describir(self) -> str:
        """Retorna una descripción legible de la entidad."""

    def __str__(self) -> str:
        return self.describir()
