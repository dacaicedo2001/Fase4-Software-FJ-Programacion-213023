"""
Punto de entrada: simula al menos 10 operaciones (válidas e inválidas).
El sistema no se detiene ante errores; continúa y registra en logs.
"""

from __future__ import annotations

from cliente import Cliente
from excepciones import ClienteInvalidoError, ReservaInvalidaError
from logger_sistema import LOG_FILE, logger
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala
from sistema import SistemaGestion


def simular(numero: int, descripcion: str, accion) -> None:
    """Ejecuta una simulación aislada sin tumbar el proceso."""
    print(f"\n--- Simulación {numero}: {descripcion} ---")
    try:
        resultado = accion()
        print(f"Resultado: {resultado}")
        logger.info("SIM-%02d OK | %s | %s", numero, descripcion, resultado)
    except Exception as err:
        print(f"Controlado: {type(err).__name__}: {err}")
        logger.error("SIM-%02d ERROR | %s | %s", numero, descripcion, err)


def main() -> None:
    sistema = SistemaGestion("Software FJ")

    # Catálogo base de servicios (válidos)
    sistema.registrar_servicio(
        ReservaSala("SRV-SALA-01", "Sala Innovación", 80000, capacidad=12)
    )
    sistema.registrar_servicio(
        AlquilerEquipo("SRV-EQ-01", "Kit Proyección", 45000, deposito=100000)
    )
    sistema.registrar_servicio(
        AsesoriaEspecializada(
            "SRV-ASE-01", "Asesoría Arquitectura de Software", 120000, "Laura Méndez"
        )
    )
    # Servicio que luego se marcará no disponible
    sala_bloqueada = ReservaSala("SRV-SALA-02", "Sala Ejecutiva", 95000, capacidad=6)
    sistema.registrar_servicio(sala_bloqueada)

    # 1) Cliente válido
    simular(
        1,
        "Registro válido de cliente",
        lambda: sistema.registrar_cliente(
            identificador="CLI-001",
            nombre="Daniel Caicedo",
            correo="daniel.caicedo@email.com",
            telefono="3001234567",
            documento="1001001020",
        ),
    )

    # 2) Cliente inválido (correo)
    simular(
        2,
        "Registro inválido de cliente (correo)",
        lambda: sistema.registrar_cliente(
            identificador="CLI-002",
            nombre="Ana Ruiz",
            correo="correo-malo",
            telefono="3011112233",
            documento="1002003001",
        ),
    )

    # 3) Cliente inválido (nombre corto) — excepción directa encapsulada
    simular(
        3,
        "Intento directo de Cliente inválido",
        lambda: Cliente(
            "CLI-003", "Al", "al@mail.com", "3022223344", "1003004002"
        ),
    )

    # 4) Segundo cliente válido
    simular(
        4,
        "Registro válido de segundo cliente",
        lambda: sistema.registrar_cliente(
            identificador="CLI-004",
            nombre="María Fernanda López",
            correo="maria.lopez@email.com",
            telefono="3159876543",
            documento="1004005003",
        ),
    )

    # 5) Creación incorrecta de servicio (tarifa negativa)
    def servicio_malo():
        return AlquilerEquipo("SRV-EQ-BAD", "Equipo X", -10, deposito=50)

    simular(5, "Creación incorrecta de servicio (tarifa negativa)", servicio_malo)

    # 6) Reserva exitosa de sala
    simular(
        6,
        "Reserva exitosa de sala",
        lambda: sistema.crear_reserva(
            "CLI-001", "SRV-SALA-01", 3, impuesto=0.19, descuento=0.1, asistentes=8
        ),
    )

    # 7) Reserva de equipo exitosa
    simular(
        7,
        "Reserva exitosa de alquiler de equipo",
        lambda: sistema.crear_reserva(
            "CLI-004", "SRV-EQ-01", 5, impuesto=0.19, incluir_deposito=True
        ),
    )

    # 8) Reserva fallida: servicio no disponible
    sala_bloqueada.marcar_disponible(False)

    simular(
        8,
        "Reserva fallida por servicio no disponible",
        lambda: sistema.crear_reserva("CLI-001", "SRV-SALA-02", 2),
    )

    # 9) Reserva fallida: cliente inexistente
    simular(
        9,
        "Reserva fallida por cliente inexistente",
        lambda: sistema.crear_reserva("CLI-999", "SRV-ASE-01", 1.5),
    )

    # 10) Asesoría urgente + procesamiento
    def asesoria_y_proceso():
        r = sistema.crear_reserva(
            "CLI-004", "SRV-ASE-01", 2, urgencia=True, descuento_cliente=0.05
        )
        if r is None:
            raise ReservaInvalidaError("No se creó la asesoría.")
        sistema.procesar_reserva(r.codigo)
        return r

    simular(10, "Asesoría urgente confirmada y procesada", asesoria_y_proceso)

    # 11) Cancelación válida de una reserva pendiente/confirmada previa
    simular(
        11,
        "Cancelación de reserva existente",
        lambda: sistema.cancelar_reserva("RSV-0001", "Cambio de agenda"),
    )

    # 12) Operación no permitida: cancelar reserva ya procesada
    simular(
        12,
        "Cancelación inválida de reserva procesada",
        lambda: sistema.cancelar_reserva("RSV-0003", "Intento indebido"),
    )

    print("\n" + sistema.resumen())
    print(f"\nLog generado en: {LOG_FILE}")
    logger.info("Simulaciones finalizadas. Sistema estable.")


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        # Red de seguridad: la app no debe caerse
        logger.exception("Error no controlado en main: %s", err)
        print(f"La aplicación continúa tras error no controlado: {err}")
