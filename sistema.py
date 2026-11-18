"""
Sistema integral de gestión (listas internas, sin base de datos).
"""

from __future__ import annotations

from cliente import Cliente
from excepciones import (
    ClienteInvalidoError,
    DatosInvalidosError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
)
from logger_sistema import logger
from reserva import Reserva
from servicios import Servicio


class SistemaGestion:
    """Orquesta clientes, servicios y reservas en memoria."""

    def __init__(self, nombre_empresa: str = "Software FJ") -> None:
        self.nombre_empresa = nombre_empresa
        self._clientes: list[Cliente] = []
        self._servicios: list[Servicio] = []
        self._reservas: list[Reserva] = []
        self._contador_reservas = 0
        logger.info("Sistema iniciado: %s", self.nombre_empresa)

    # ---- clientes ----
    def registrar_cliente(self, **kwargs) -> Cliente | None:
        try:
            cliente = Cliente(**kwargs)
            if any(c.documento == cliente.documento for c in self._clientes):
                raise ClienteInvalidoError(
                    f"Ya existe un cliente con documento {cliente.documento}."
                )
            self._clientes.append(cliente)
            return cliente
        except ClienteInvalidoError as err:
            logger.error("Registro de cliente fallido: %s", err)
            return None
        except Exception as err:
            logger.exception("Error inesperado registrando cliente: %s", err)
            return None
        else:
            logger.debug("Flujo else: cliente OK en lista (%s)", len(self._clientes))
        finally:
            logger.debug("Finally: intento de registro de cliente finalizado")

    def buscar_cliente(self, identificador: str) -> Cliente:
        for cliente in self._clientes:
            if cliente.id == identificador:
                return cliente
        raise DatosInvalidosError(f"Cliente '{identificador}' no encontrado.")

    # ---- servicios ----
    def registrar_servicio(self, servicio: Servicio) -> Servicio | None:
        try:
            if not isinstance(servicio, Servicio):
                raise DatosInvalidosError("Objeto de servicio inválido.")
            if any(s.id == servicio.id for s in self._servicios):
                raise DatosInvalidosError(f"Servicio duplicado: {servicio.id}")
            self._servicios.append(servicio)
            logger.info("Servicio registrado: %s", servicio.id)
            return servicio
        except (DatosInvalidosError, Exception) as err:
            logger.error("No se registró el servicio: %s", err)
            return None
        finally:
            logger.debug("Finally: intento de registro de servicio finalizado")

    def obtener_servicio(self, identificador: str) -> Servicio:
        for servicio in self._servicios:
            if servicio.id == identificador:
                if not servicio.disponible:
                    raise ServicioNoDisponibleError(
                        f"Servicio '{identificador}' no disponible."
                    )
                return servicio
        raise ServicioNoDisponibleError(f"Servicio '{identificador}' no existe.")

    # ---- reservas ----
    def crear_reserva(
        self,
        id_cliente: str,
        id_servicio: str,
        duracion_horas: float,
        confirmar: bool = True,
        **kwargs_costo,
    ) -> Reserva | None:
        reserva = None
        try:
            cliente = self.buscar_cliente(id_cliente)
            servicio = self.obtener_servicio(id_servicio)
            self._contador_reservas += 1
            codigo = f"RSV-{self._contador_reservas:04d}"
            reserva = Reserva(codigo, cliente, servicio, duracion_horas)
            if confirmar:
                reserva.confirmar(**kwargs_costo)
            self._reservas.append(reserva)
            return reserva
        except (
            DatosInvalidosError,
            ServicioNoDisponibleError,
            ReservaInvalidaError,
        ) as err:
            logger.error("Reserva fallida: %s", err)
            return None
        except Exception as err:
            logger.exception("Error inesperado en reserva: %s", err)
            return None
        else:
            logger.debug("Else: reserva creada %s", reserva.codigo if reserva else "-")
        finally:
            logger.debug("Finally: operación de reserva cerrada")

    def cancelar_reserva(self, codigo: str, motivo: str = "Solicitud del cliente") -> bool:
        try:
            reserva = self._buscar_reserva(codigo)
            reserva.cancelar(motivo)
            return True
        except Exception as err:
            logger.error("No se canceló %s: %s", codigo, err)
            return False

    def procesar_reserva(self, codigo: str) -> bool:
        try:
            reserva = self._buscar_reserva(codigo)
            reserva.procesar()
            return True
        except Exception as err:
            logger.error("No se procesó %s: %s", codigo, err)
            return False

    def _buscar_reserva(self, codigo: str) -> Reserva:
        for reserva in self._reservas:
            if reserva.codigo == codigo:
                return reserva
        raise ReservaInvalidaError(f"Reserva '{codigo}' no encontrada.")

    def resumen(self) -> str:
        lineas = [
            f"=== {self.nombre_empresa} ===",
            f"Clientes: {len(self._clientes)}",
            f"Servicios: {len(self._servicios)}",
            f"Reservas: {len(self._reservas)}",
        ]
        for r in self._reservas:
            lineas.append(f"  - {r}")
        return "\n".join(lineas)
