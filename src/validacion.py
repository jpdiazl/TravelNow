from pathlib import Path
from datetime import datetime
import pandas as pd
import re

from utils import escribir_log, guardar_log_db

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
VALID_DIR = BASE_DIR / "data" / "valid"
INVALID_DIR = BASE_DIR / "data" / "invalid"


def obtener_ultimo_procesado():
    archivos = list(PROCESSED_DIR.glob("reservas_limpias_*.csv"))
    if not archivos:
        return None
    return max(archivos, key=lambda x: x.stat().st_mtime)


def correo_valido(correo):
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(patron, str(correo)))


def validar_reservas():
    escribir_log("Semana 3 - Inicio de validación estructural y semántica")

    try:
        archivo_procesado = obtener_ultimo_procesado()

        if archivo_procesado is None:
            mensaje = "No existen archivos procesados para validar"
            escribir_log(mensaje)
            guardar_log_db("Validación", "sin_archivo", 0, "ERROR", mensaje)
            return None

        df = pd.read_csv(archivo_procesado)
        df["fecha_viaje"] = pd.to_datetime(df["fecha_viaje"], errors="coerce")

        errores = []

        for _, fila in df.iterrows():
            motivos = []

            if pd.isna(fila["id_reserva"]) or str(fila["id_reserva"]).strip() == "":
                motivos.append("id_reserva vacío")

            if pd.isna(fila["nombre_cliente"]) or str(fila["nombre_cliente"]).strip() == "":
                motivos.append("nombre_cliente vacío")

            if pd.isna(fila["destino"]) or str(fila["destino"]).strip() == "":
                motivos.append("destino vacío")

            if pd.isna(fila["fecha_viaje"]):
                motivos.append("fecha_viaje inválida")



            if not correo_valido(fila["correo"]):
                motivos.append("correo inválido")

            errores.append("; ".join(motivos))

        df["errores"] = errores

        validos = df[df["errores"] == ""].copy()
        invalidos = df[df["errores"] != ""].copy()

        VALID_DIR.mkdir(parents=True, exist_ok=True)
        INVALID_DIR.mkdir(parents=True, exist_ok=True)

        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo_validos = VALID_DIR / f"reservas_validas_{fecha}.csv"
        archivo_invalidos = INVALID_DIR / f"reservas_invalidas_{fecha}.csv"

        validos.drop(columns=["errores"]).to_csv(archivo_validos, index=False, encoding="utf-8-sig")
        invalidos.to_csv(archivo_invalidos, index=False, encoding="utf-8-sig")

        mensaje = f"Validación terminada. Válidos: {len(validos)} | Inválidos: {len(invalidos)}"
        escribir_log(mensaje)
        guardar_log_db("Validación", archivo_validos.name, len(validos), "OK", mensaje)
        escribir_log("Semana 3 - Fin de validación")

        return archivo_validos

    except Exception as error:
        mensaje = f"Error en validación: {error}"
        escribir_log(mensaje)
        guardar_log_db("Validación", "reservas_validacion", 0, "ERROR", mensaje)
        return None


if __name__ == "__main__":
    validar_reservas()
