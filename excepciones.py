"""
Excepciones personalizadas del sistema Software FJ.
Clasifican errores de dominio y permiten encadenamiento con causas originales.
"""

from __future__ import annotations


class SoftwareFJError(Exception):
    """Excepción base del dominio Software FJ."""

    def __init__(self, mensaje: str) -> None:
        self.mensaje = mensaje
        super().__init__(mensaje)


class DatosInvalidosError(SoftwareFJError):
    """Datos de entrada inválidos o incompletos."""


class ClienteInvalidoError(DatosInvalidosError):
    """Fallo en validación de un cliente."""


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio solicitado no está disponible o no existe."""


class ReservaInvalidaError(SoftwareFJError):
    """Operación de reserva no permitida o inconsistente."""


class CalculoInconsistenteError(SoftwareFJError):
    """Cálculo de costos o parámetros inconsistentes."""


def encadenar(mensaje: str, causa: BaseException) -> SoftwareFJError:
    """
    Construye una excepción de dominio encadenada a la causa original.
    Ejemplo: raise encadenar("No se pudo confirmar", err)
    """
    error = SoftwareFJError(mensaje)
    error.__cause__ = causa
    return error
