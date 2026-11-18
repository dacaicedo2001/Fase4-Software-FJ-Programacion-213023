"""
Clase Cliente con encapsulación y validaciones robustas.
"""

from __future__ import annotations

import re

from entidades import Entidad
from excepciones import ClienteInvalidoError
from logger_sistema import logger


class Cliente(Entidad):
    """Representa un cliente de Software FJ."""

    def __init__(
        self,
        identificador: str,
        nombre: str,
        correo: str,
        telefono: str,
        documento: str,
    ) -> None:
        try:
            super().__init__(identificador)
            self._nombre = self._validar_nombre(nombre)
            self._correo = self._validar_correo(correo)
            self._telefono = self._validar_telefono(telefono)
            self._documento = self._validar_documento(documento)
            self._activo = True
            logger.info("Cliente registrado: %s (%s)", self._nombre, self._id)
        except ClienteInvalidoError:
            raise
        except Exception as err:
            logger.error("Error al crear cliente: %s", err)
            raise ClienteInvalidoError(f"No se pudo crear el cliente: {err}") from err

    # ---- encapsulación ----
    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def correo(self) -> str:
        return self._correo

    @property
    def telefono(self) -> str:
        return self._telefono

    @property
    def documento(self) -> str:
        return self._documento

    @property
    def activo(self) -> bool:
        return self._activo

    def desactivar(self) -> None:
        self._activo = False
        logger.info("Cliente desactivado: %s", self._id)

    def describir(self) -> str:
        estado = "activo" if self._activo else "inactivo"
        return f"Cliente[{self._id}] {self._nombre} <{self._correo}> ({estado})"

    # ---- validaciones ----
    @staticmethod
    def _validar_nombre(nombre: str) -> str:
        if not nombre or len(nombre.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")
        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$", nombre.strip()):
            raise ClienteInvalidoError("El nombre solo puede contener letras y espacios.")
        return nombre.strip().title()

    @staticmethod
    def _validar_correo(correo: str) -> str:
        if not correo or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", correo.strip()):
            raise ClienteInvalidoError("El correo electrónico no es válido.")
        return correo.strip().lower()

    @staticmethod
    def _validar_telefono(telefono: str) -> str:
        limpio = re.sub(r"\D", "", str(telefono))
        if len(limpio) < 7 or len(limpio) > 15:
            raise ClienteInvalidoError("El teléfono debe tener entre 7 y 15 dígitos.")
        return limpio

    @staticmethod
    def _validar_documento(documento: str) -> str:
        limpio = re.sub(r"\D", "", str(documento))
        if len(limpio) < 5:
            raise ClienteInvalidoError("El documento debe tener al menos 5 dígitos.")
        return limpio
