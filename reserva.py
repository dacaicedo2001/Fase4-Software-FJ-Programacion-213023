"""
Clase Reserva: integra cliente, servicio, duración y estado.
"""

from __future__ import annotations

from cliente import Cliente
from excepciones import ReservaInvalidaError, encadenar
from logger_sistema import logger
from servicios import Servicio


class Reserva:
    """Gestiona el ciclo de vida de una reserva."""

    ESTADOS = {"pendiente", "confirmada", "cancelada", "procesada"}

    def __init__(
        self,
        codigo: str,
        cliente: Cliente,
        servicio: Servicio,
        duracion_horas: float,
    ) -> None:
        if not codigo or not str(codigo).strip():
            raise ReservaInvalidaError("El código de reserva es obligatorio.")
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("Se requiere un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("Se requiere un servicio válido.")
        if not cliente.activo:
            raise ReservaInvalidaError("No se puede reservar con un cliente inactivo.")
        if float(duracion_horas) <= 0:
            raise ReservaInvalidaError("La duración de la reserva debe ser positiva.")

        self._codigo = codigo.strip()
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = float(duracion_horas)
        self._estado = "pendiente"
        self._costo = 0.0
        logger.info("Reserva creada %s (pendiente)", self._codigo)

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo(self) -> float:
        return self._costo

    def confirmar(self, **kwargs_costo) -> float:
        """Confirma la reserva calculando el costo del servicio."""
        try:
            if self._estado != "pendiente":
                raise ReservaInvalidaError(
                    f"Solo se confirman reservas pendientes (actual: {self._estado})."
                )
            self._costo = self._servicio.calcular_costo(self._duracion, **kwargs_costo)
            self._estado = "confirmada"
            logger.info(
                "Reserva %s confirmada. Costo=$%.2f", self._codigo, self._costo
            )
            return self._costo
        except ReservaInvalidaError:
            logger.error("Confirmación inválida %s", self._codigo)
            raise
        except Exception as err:
            logger.exception("Error al confirmar reserva %s", self._codigo)
            raise encadenar(f"No se pudo confirmar la reserva {self._codigo}", err)

    def cancelar(self, motivo: str = "Sin motivo") -> None:
        try:
            if self._estado == "cancelada":
                raise ReservaInvalidaError("La reserva ya está cancelada.")
            if self._estado == "procesada":
                raise ReservaInvalidaError("No se puede cancelar una reserva procesada.")
            self._estado = "cancelada"
            logger.info("Reserva %s cancelada. Motivo: %s", self._codigo, motivo)
        except ReservaInvalidaError:
            logger.error("Cancelación inválida %s: %s", self._codigo, motivo)
            raise
        except Exception as err:
            raise encadenar(f"Fallo al cancelar {self._codigo}", err)

    def procesar(self) -> None:
        """Marca la reserva confirmada como procesada (servicio prestado)."""
        try:
            if self._estado != "confirmada":
                raise ReservaInvalidaError(
                    "Solo se procesan reservas confirmadas."
                )
            self._estado = "procesada"
            logger.info("Reserva %s procesada correctamente", self._codigo)
        except ReservaInvalidaError:
            logger.error("Procesamiento inválido %s", self._codigo)
            raise
        except Exception as err:
            raise encadenar(f"Fallo al procesar {self._codigo}", err)

    def describir(self) -> str:
        return (
            f"Reserva[{self._codigo}] estado={self._estado} "
            f"cliente={self._cliente.nombre} servicio={self._servicio.nombre} "
            f"duracion={self._duracion}h costo=${self._costo:.2f}"
        )

    def __str__(self) -> str:
        return self.describir()
