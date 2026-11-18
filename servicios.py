"""
Jerarquía de servicios con herencia, polimorfismo y sobrecarga de costos.
"""

from __future__ import annotations

from abc import abstractmethod

from entidades import Entidad
from excepciones import CalculoInconsistenteError, DatosInvalidosError, ServicioNoDisponibleError
from logger_sistema import logger


class Servicio(Entidad):
    """Clase abstracta de servicio ofrecido por Software FJ."""

    def __init__(
        self,
        identificador: str,
        nombre: str,
        tarifa_base: float,
        disponible: bool = True,
    ) -> None:
        super().__init__(identificador)
        if not nombre or len(nombre.strip()) < 3:
            raise DatosInvalidosError("El nombre del servicio es inválido.")
        if tarifa_base <= 0:
            raise CalculoInconsistenteError("La tarifa base debe ser mayor que cero.")
        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    def marcar_disponible(self, estado: bool) -> None:
        self._disponible = estado
        logger.info("Servicio %s disponible=%s", self._id, estado)

    def validar_parametros(self, duracion_horas: float) -> None:
        """Validación genérica; las clases hijas pueden sobrescribir."""
        if duracion_horas is None or float(duracion_horas) <= 0:
            raise DatosInvalidosError("La duración debe ser un número positivo.")
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self._nombre}' no está disponible."
            )

    @abstractmethod
    def calcular_costo(self, duracion_horas: float, *args, **kwargs) -> float:
        """Cálculo polimórfico del costo del servicio."""

    def describir(self) -> str:
        estado = "disponible" if self._disponible else "no disponible"
        return f"Servicio[{self._id}] {self._nombre} (${self._tarifa_base:.0f}/h) - {estado}"


class ReservaSala(Servicio):
    """Servicio de reserva de salas."""

    def __init__(
        self,
        identificador: str,
        nombre: str,
        tarifa_base: float,
        capacidad: int,
        disponible: bool = True,
    ) -> None:
        super().__init__(identificador, nombre, tarifa_base, disponible)
        if capacidad < 1:
            raise DatosInvalidosError("La capacidad de la sala debe ser >= 1.")
        self._capacidad = capacidad

    def validar_parametros(self, duracion_horas: float, asistentes: int | None = None) -> None:
        super().validar_parametros(duracion_horas)
        if asistentes is not None and asistentes > self._capacidad:
            raise DatosInvalidosError(
                f"La sala admite máximo {self._capacidad} asistentes."
            )

    def calcular_costo(
        self,
        duracion_horas: float,
        impuesto: float = 0.19,
        descuento: float = 0.0,
        asistentes: int | None = None,
    ) -> float:
        """
        Sobrecarga lógica vía parámetros opcionales:
        - solo duración
        - duración + impuesto
        - duración + impuesto + descuento
        - + validación de asistentes
        """
        try:
            self.validar_parametros(duracion_horas, asistentes)
            if impuesto < 0 or descuento < 0 or descuento > 1:
                raise CalculoInconsistenteError("Impuesto/descuento inconsistente.")
            bruto = self._tarifa_base * float(duracion_horas)
            con_impuesto = bruto * (1 + impuesto)
            neto = con_impuesto * (1 - descuento)
            if neto < 0:
                raise CalculoInconsistenteError("El costo neto no puede ser negativo.")
            return round(neto, 2)
        except (DatosInvalidosError, ServicioNoDisponibleError, CalculoInconsistenteError):
            raise
        except Exception as err:
            raise CalculoInconsistenteError("Fallo al calcular costo de sala.") from err

    def describir(self) -> str:
        return f"{super().describir()} | capacidad={self._capacidad}"


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos."""

    def __init__(
        self,
        identificador: str,
        nombre: str,
        tarifa_base: float,
        deposito: float,
        disponible: bool = True,
    ) -> None:
        super().__init__(identificador, nombre, tarifa_base, disponible)
        if deposito < 0:
            raise CalculoInconsistenteError("El depósito no puede ser negativo.")
        self._deposito = float(deposito)

    def calcular_costo(
        self,
        duracion_horas: float,
        impuesto: float = 0.19,
        incluir_deposito: bool = True,
    ) -> float:
        try:
            self.validar_parametros(duracion_horas)
            bruto = self._tarifa_base * float(duracion_horas)
            total = bruto * (1 + impuesto)
            if incluir_deposito:
                total += self._deposito
            return round(total, 2)
        except (DatosInvalidosError, ServicioNoDisponibleError):
            raise
        except Exception as err:
            raise CalculoInconsistenteError("Fallo al calcular costo de equipo.") from err

    def describir(self) -> str:
        return f"{super().describir()} | depósito=${self._deposito:.0f}"


class AsesoriaEspecializada(Servicio):
    """Servicio de asesorías especializadas."""

    def __init__(
        self,
        identificador: str,
        nombre: str,
        tarifa_base: float,
        especialista: str,
        disponible: bool = True,
    ) -> None:
        super().__init__(identificador, nombre, tarifa_base, disponible)
        if not especialista or len(especialista.strip()) < 3:
            raise DatosInvalidosError("Debe indicar el especialista.")
        self._especialista = especialista.strip().title()

    def calcular_costo(
        self,
        duracion_horas: float,
        urgencia: bool = False,
        descuento_cliente: float = 0.0,
    ) -> float:
        try:
            self.validar_parametros(duracion_horas)
            if descuento_cliente < 0 or descuento_cliente > 0.5:
                raise CalculoInconsistenteError("Descuento de cliente fuera de rango (0-50%).")
            bruto = self._tarifa_base * float(duracion_horas)
            if urgencia:
                bruto *= 1.35
            neto = bruto * (1 - descuento_cliente)
            return round(neto, 2)
        except (DatosInvalidosError, ServicioNoDisponibleError, CalculoInconsistenteError):
            raise
        except Exception as err:
            raise CalculoInconsistenteError("Fallo al calcular costo de asesoría.") from err

    def describir(self) -> str:
        return f"{super().describir()} | especialista={self._especialista}"
