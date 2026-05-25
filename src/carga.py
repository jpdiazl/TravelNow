from pathlib import Path
import pandas as pd

from utils import escribir_log, guardar_log_db, conectar_db

BASE_DIR = Path(__file__).resolve().parent.parent
VALID_DIR = BASE_DIR / "data" / "valid"


def obtener_ultimo_validado():
    archivos = list(VALID_DIR.glob("reservas_validas_*.csv"))
    if not archivos:
        return None
    return max(archivos, key=lambda x: x.stat().st_mtime)


def cargar_reservas():
    escribir_log("Semana 4 - Inicio de carga a Oracle Autonomous Database")

    try:
        archivo_validado = obtener_ultimo_validado()

        if archivo_validado is None:
            mensaje = "No existen archivos válidos para cargar"
            escribir_log(mensaje)
            guardar_log_db("Carga", "sin_archivo", 0, "ERROR", mensaje)
            return

        df = pd.read_csv(archivo_validado)
        df["fecha_viaje"] = pd.to_datetime(df["fecha_viaje"], errors="coerce").dt.date
        df["id_reserva"] = df["id_reserva"].astype(int)

        conexion = conectar_db()
        cursor = conexion.cursor()

        insertados = 0

        for _, fila in df.iterrows():
            cursor.execute("""
                MERGE INTO reservas r
                USING (
                    SELECT :1 AS id_reserva,
                           :2 AS nombre_cliente,
                           :3 AS destino,
                           :4 AS fecha_viaje,
                           :5 AS correo,
                           :6 AS plataforma
                    FROM dual
                ) src
                ON (r.id_reserva = src.id_reserva)
                WHEN NOT MATCHED THEN
                    INSERT (id_reserva, nombre_cliente, destino, fecha_viaje, correo, plataforma)
                    VALUES (src.id_reserva, src.nombre_cliente, src.destino, src.fecha_viaje, src.correo, src.plataforma)
            """, (
                int(fila["id_reserva"]),
                fila["nombre_cliente"],
                fila["destino"],
                fila["fecha_viaje"],
                fila["correo"],
                fila["plataforma"]
            ))

            if cursor.rowcount > 0:
                insertados += 1

        conexion.commit()
        cursor.close()
        conexion.close()

        mensaje = f"Carga finalizada en Oracle. Registros insertados o procesados: {insertados}"
        escribir_log(mensaje)
        guardar_log_db("Carga", archivo_validado.name, insertados, "OK", mensaje)
        escribir_log("Semana 4 - Fin de carga")

    except Exception as error:
        mensaje = f"Error en carga a Oracle: {error}"
        escribir_log(mensaje)
        guardar_log_db("Carga", "reservas", 0, "ERROR", mensaje)


if __name__ == "__main__":
    cargar_reservas()
