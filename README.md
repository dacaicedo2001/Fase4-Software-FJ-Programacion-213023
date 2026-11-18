# Software FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas

**Curso:** Programación (213023) – UNAD  
**Actividad:** Fase 4 – Componente práctico (Prácticas simuladas)  
**Estudiante:** Daniel Caicedo Murillo  
**Grupo académico:** 213023_341  

## Aclaración sobre el desarrollo individual

Por motivos de **flexibilidad en mis tiempos de trabajo, estudio y actividades personales**, no me fue posible ajustarme a los horarios de coordinación del resto del equipo. Ante la ausencia de avances compartidos y para garantizar el cumplimiento académico en la fecha establecida, **decidí desarrollar esta fase de forma individual**, asumiendo la implementación completa del sistema, la documentación y la evidencia en este repositorio.

Esta decisión no desconoce el carácter colaborativo de la guía; responde a una necesidad práctica de responsabilidad académica y entrega oportuna.

## Descripción

Aplicación orientada a objetos (sin bases de datos) para la empresa **Software FJ**, que ofrece:

- Reserva de salas
- Alquiler de equipos
- Asesorías especializadas

El sistema implementa abstracción, herencia, polimorfismo, encapsulación y **manejo avanzado de excepciones**, registrando eventos y errores en un archivo de logs.

## Estructura del proyecto

```
Fase4_Software_FJ/
|-- main.py              # Simulaciones (>=10 operaciones válidas e inválidas)
|-- sistema.py           # Orquestación con listas internas
|-- entidades.py         # Clase abstracta Entidad
|-- cliente.py           # Cliente con validaciones y encapsulación
|-- servicios.py         # Servicio + ReservaSala, AlquilerEquipo, AsesoriaEspecializada
|-- reserva.py           # Confirmación, cancelación y procesamiento
|-- excepciones.py       # Excepciones personalizadas + encadenamiento
|-- logger_sistema.py    # Logging a archivo y consola
|-- logs/                # Archivo sistema_fj.log (se genera al ejecutar)
|-- evidencias/          # PDF/DOCX de entrega
|-- README.md
```

## Requisitos

- Python 3.10+ (solo biblioteca estándar)

## Ejecución

```bash
python main.py
```

Al finalizar verá el resumen del sistema y la ruta del log en `logs/sistema_fj.log`.

## Conceptos aplicados

| Concepto | Dónde se evidencia |
|----------|--------------------|
| Clase abstracta | `Entidad`, `Servicio` |
| Herencia / polimorfismo | `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| Encapsulación | atributos privados y propiedades en `Cliente` / `Reserva` |
| Sobrecarga lógica de costos | parámetros opcionales en `calcular_costo` |
| Excepciones personalizadas | módulo `excepciones.py` |
| try/except/else/finally | `SistemaGestion.registrar_cliente` y `crear_reserva` |
| Encadenamiento | `encadenar()` y `raise ... from err` |
| Logs | `logger_sistema.py` -> `logs/sistema_fj.log` |

## Simulaciones incluidas

El `main.py` ejecuta operaciones válidas e inválidas (clientes, servicios, reservas, servicio no disponible, cancelaciones indebidas) **sin detener** la aplicación ante errores.

## Autor

Daniel Caicedo Murillo – Ingeniería de Sistemas, UNAD.

## Seguimiento en GitHub

- Issue asignado: [#1 Documentación: desarrollo individual de la Fase 4](https://github.com/dacaicedo2001/Fase4-Software-FJ-Programacion-213023/issues/1)
