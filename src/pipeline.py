from crear_tablas import crear_tablas
from ingesta import ejecutar_ingesta
from limpieza import limpiar_reservas
from validacion import validar_reservas
from carga import cargar_reservas
from utils import escribir_log


def ejecutar_pipeline():
    escribir_log("Inicio del pipeline completo TravelNow: MongoDB Atlas -> CSV -> Oracle Autonomous")

    try:
        crear_tablas()
    except Exception as error:
        escribir_log(f"No se pudieron crear las tablas en Oracle: {error}")
        escribir_log("Pipeline detenido antes de iniciar ingesta")
        return

    archivo_raw = ejecutar_ingesta()

    if archivo_raw is None:
        escribir_log("Pipeline detenido en etapa de ingesta")
        return

    archivo_limpio = limpiar_reservas()

    if archivo_limpio is None:
        escribir_log("Pipeline detenido en etapa de limpieza")
        return

    archivo_validado = validar_reservas()

    if archivo_validado is None:
        escribir_log("Pipeline detenido en etapa de validación")
        return

    cargar_reservas()

    escribir_log("Fin del pipeline completo TravelNow")


if __name__ == "__main__":
    ejecutar_pipeline()
